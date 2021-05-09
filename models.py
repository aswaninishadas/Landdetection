from sqlalchemy import Column, Integer, String, Boolean, Float

from database import Base


class UserModel(Base):
    __tablename__ = "user"

    userId = Column(Integer, primary_key=True, index=True, autoincrement=True)
    firstName = Column(String, index=True)
    lastName = Column(String, index=True)
    userName = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    phoneNumber = Column(Integer, unique=True, index=True)
    password = Column(String, index=True)


# class RationCardModel(Base):
#     __tablename__ = "rationCard"
#
#     cardId = Column(Integer, primary_key=True, index=True, autoincrement=True)
#     cardNumber = Column(Integer, unique=True, index=True)
#     ownerName = Column(String, index=True)
#     houseName = Column(String, index=True)
#     houseNumber = Column(Integer, index=True)
#     place = Column(String, index=True)
#     thaluk = Column(String, index=True)


class MemberDetailsModel(Base):
    __tablename__ = "memberDetails"

    memberId = Column(Integer, primary_key=True, index=True, autoincrement=True)
    firstName = Column(String, index=True)
    lastName = Column(String, index=True)
    age = Column(Integer, index=True)
    maritalStatus = Column(Boolean, index=True)
    spouse = Column(Integer, index=True)
    # landOwnedInAcres = Column(Integer, index=True)
    landOwnedInCent = Column(Float, index=True)
    cardNumber = Column(Integer, index=True)