from typing import List

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status
from starlette.middleware.cors import CORSMiddleware

import crud
from database import SessionLocal
from models import UserModel
from schemas import User, Token, UserLogin, Member, TokenData


def getDb():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        print(e)
        return None
    finally:
        db.close()


app = FastAPI()

# origins = [
#     "http://localhost.tiangolo.com",
#     "https://localhost.tiangolo.com",
#     "http://localhost",
#     "http://localhost:8000",
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def getUser(db: Session, userName: str):
    try:
        user = db.query(UserModel).filter(UserModel.userName == userName).first()
        if user:
            return user
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail={"message": "Common Unexpected Error"})


async def getCurrentUser(token: str = Depends(oauth2_scheme), db: Session = Depends(getDb)):
    try:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, crud.SECRET_KEY, algorithms=[crud.ALGORITHM])
            userName: str = payload.get("sub")
            if userName is None:
                raise credentials_exception
            token_data = TokenData(userName=userName)
        except JWTError:
            raise credentials_exception
        user = getUser(db=db, userName=token_data.userName)
        if user is None:
            raise credentials_exception
        return user
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail={"message": "Invalid Credentials"})


async def getCurrentActiveUser(current_user: User = Depends(getCurrentUser)):
    try:
        return current_user
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail={"message": "Invalid Credentials"})






@app.post("/user/signup", response_model=User)
async def sign_up(user: User, db: Session = Depends(getDb)):
    return crud.sign_up(schemaObject=user, db=db)


@app.post("/user/login", response_model=Token)
async def login(user: UserLogin, db: Session = Depends(getDb)):
    userObj = crud.authenticateUser(db, userName=user.userName, password=user.password)
    return crud.validateUser(userObj)


@app.get("/member/list/{cardNumber}", response_model=List[Member])
async def member_details(cardNumber: int, db: Session = Depends(getDb),
                         current_user: User = Depends(getCurrentActiveUser)):
    return crud.members(cardNumber=cardNumber, db=db, current_user=current_user)


@app.post("/eligibility/check/{memberId}/{landRequested}/{isAgriculturalLand}")
async def elegibility_check(memberId: int, landRequested: float, isAgriculturalLand: bool, db: Session = Depends(getDb),
                            current_user: User = Depends(getCurrentActiveUser)):
    return crud.check_elegibility(memberId=memberId, landRequested=landRequested, isAgriculturalLand=isAgriculturalLand,
                                  db=db, current_user=current_user)

