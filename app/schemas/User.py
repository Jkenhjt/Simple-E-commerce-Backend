from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, String, Integer, Boolean, LargeBinary


class BaseUser(DeclarativeBase):
    pass


class UserScheme(BaseUser):
    __tablename__ = "Users"

    id = Column(Integer(), primary_key=True)

    username = Column(String())
    password = Column(LargeBinary())

    jwtToken = Column(String())

    isAdmin = Column(Boolean())

    def __repr__(self) -> str:
        return f""" id={self.id},
                    username={self.username},
                    password={self.password},
                    jwtToken={self.jwtToken},
                    isAdmin={self.isAdmin} """
