from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, String, Integer, Float


class BasePayment(DeclarativeBase):
    pass


class PaymentScheme(BasePayment):
    __tablename__ = "Payments"

    id = Column(Integer(), primary_key=True)

    username = Column(String())

    buyerCard = Column(String())
    buyerCardDate = Column(String())
    buyerCardCVV = Column(String())

    cartProducts = Column(String())
    price = Column(Float())

    hashPayment = Column(String())

    date = Column(String())

    def __repr__(self) -> str:
        return f""" id={self.id},
                    username={self.username},
                    buyerCard={self.buyerCard},
                    buyerCardDate={self.buyerCardDate},
                    buyerCardCVV={self.buyerCardCVV},
                    cartProducts={self.cartProducts},
                    price={self.price},
                    hashPayment={self.hashPayment},
                    date={self.date} """
