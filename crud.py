from datetime import datetime
from typing import Optional

from fastapi import HTTPException
from pydantic.datetime_parse import timedelta
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse

from models import UserModel, MemberDetailsModel
from schemas import User
from passlib.context import CryptContext
from jose import jwt


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ACCESS_TOKEN_EXPIRE_MINUTES = 60
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"


def getPasswordHash(password):
    try:
        return pwd_context.hash(password)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail={"message": "Unexpected error occurred"})


def sign_up(schemaObject: User, db: Session):
    try:
        userObj = UserModel(
            firstName=schemaObject.firstName,
            lastName=schemaObject.lastName,
            userName=schemaObject.userName,
            email=schemaObject.email,
            phoneNumber=schemaObject.phoneNumber,
            password=getPasswordHash(schemaObject.password),
            )
        db.add(userObj)
        db.commit()
        return userObj
    except Exception as e:
        db.rollback()
        print(e)
        raise HTTPException(status_code=400, detail={"message": "Unexpected error occurred"})


def verifyPassword(plain_password, hashed_password):
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail={"message": "Unexpected Error Occured"})


def authenticateUser(db, userName: str, password: str):
    try:
        user = db.query(UserModel).filter(UserModel.userName == userName).first()
        if not user:
            return False
        if not verifyPassword(password, user.password):
            return False
        return user
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail={"message": "Unexpected Error Occured"})


def createAccessToken(data: dict, expires_delta: Optional[timedelta] = None):
    try:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail={"message": "Unexpected Error Occured"})


def validateUser(userObj: UserModel):
    if not userObj:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Invalid credentials"},
            headers={"WWW-Authenticate": "Bearer"},
        )
    else:
        try:
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = createAccessToken(
                data={"sub": userObj.userName}, expires_delta=access_token_expires
            )

            headers = {
                "access_token": access_token,
                "token_type": "bearer",
            }
            return JSONResponse(status_code=200, content=headers)
        except Exception as e:
            print(e)
            raise HTTPException(status_code=400, detail={"message": "Login Failed"})


def members(cardNumber: int, db: Session, current_user: User):
    try:
        result = db.query(MemberDetailsModel).filter(
            MemberDetailsModel.cardNumber == cardNumber
        ).all()
        return result
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail={"message": "Unexpected Error Occured"})


def check_elegibility(memberId: int, landRequested: float, isAgriculturalLand: bool, db: Session, current_user: User):
    try:
        message = ""
        status_code = 200
        member = db.query(MemberDetailsModel).filter(
            MemberDetailsModel.memberId == memberId
        ).first()

        members = db.query(MemberDetailsModel).filter(
            MemberDetailsModel.cardNumber == member.cardNumber
        ).all()

#-----------------CASE 1-------------------
        if isAgriculturalLand is False:
            if len(members) == 1:
                maxLand = 500

                if member.landOwnedInCent+landRequested > maxLand:
                    canBuy = maxLand - member.landOwnedInCent
                    status_code = 200
                    message = "{} is ineligible. Total land a person can hold is {} cents." \
                              " {} is eligible to buy only {} cents".format(member.firstName, maxLand,
                                                                            member.firstName, canBuy)
                else:
                    print(4)
                    status_code = 200
                    message = "{} is eligible for the purchase of {} cents".format(member.firstName, landRequested)
                    print(5)

    # -----------------END OF CASE 1-------------------

    # -----------------CASE 2-------------------
            elif 2 <= len(members) <= 5:
                maxLand = 500
                familyLimit = 1500
                totalLand = 0
                for i in members:
                    totalLand = totalLand + i.landOwnedInCent

                remainingFamilyLimit = familyLimit - totalLand
                remainingPersonalLimit = maxLand - member.landOwnedInCent

                if member.landOwnedInCent+landRequested < maxLand:
                    if totalLand+landRequested <= familyLimit:
                        status_code = 200
                        message = "{} is eligible for the land purchase of {} cent".format(member.firstName, landRequested)
                    else:
                        if remainingFamilyLimit < remainingPersonalLimit:
                            canBuy = remainingFamilyLimit
                        else:
                            canBuy =remainingPersonalLimit
                        print(totalLand)
                        status_code = 200
                        message = "{} is ineligible. Requested amount exceeds family limit of {} cent. " \
                                  "The person is eligible to buy {} cent".format(member.firstName, familyLimit, canBuy)

                else:
                    canBuy = maxLand - member.landOwnedInCent
                    status_code = 200
                    message = "{} is ineligible. Total amount of land the person can hold is {} cent." \
                              " The maximum land the person can buy is {} cent".format(member.firstName, maxLand, canBuy)
    # -----------------END OF CASE 2-------------------

    # -----------------CASE 3-------------------

            elif len(members) > 5:
                maxLand = 500
                familyLimit = 2000
                totalLand = 0
                for i in members:
                    totalLand = totalLand + i.landOwnedInCent

                remainingFamilyLimit = familyLimit - totalLand
                remainingPersonalLimit = maxLand - member.landOwnedInCent

                if member.landOwnedInCent + landRequested < maxLand:
                    if totalLand + landRequested <= familyLimit:
                        status_code = 200
                        message = "{} is eligible for the land purchase of {} cent".format(member.firstName, landRequested)
                    else:
                        if remainingFamilyLimit < remainingPersonalLimit:
                            canBuy = remainingFamilyLimit
                        else:
                            canBuy = remainingPersonalLimit
                        status_code = 200
                        message = "{} is ineligible. Requested amount exceeds family limit of {} cent. " \
                                  "The person is eligible to buy {} cent".format(member.firstName, familyLimit, canBuy)

                else:
                    canBuy = maxLand - member.landOwnedInCent
                    status_code = 200
                    message = "Ineligible. Total amount of land the person can hold is {} cent." \
                              " The maximum land the person can buy is {} cent".format(maxLand, canBuy)

# -----------------END OF CASE 3-------------------
        else:
            status_code = 200
            message = "{} is eligible for the purchase of {} cents".format(member.firstName, landRequested)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail={"message": "Unexpected Error Occured"})
    raise HTTPException(status_code=status_code, detail={"message": message})
