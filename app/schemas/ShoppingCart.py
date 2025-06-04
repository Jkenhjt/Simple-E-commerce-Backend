from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, String, Integer, Float


class BaseShoppingCart(DeclarativeBase):
    pass


class ShoppingCartScheme(BaseShoppingCart):
    __tablename__ = "ShoppingCart"

    id = Column(Integer(), primary_key=True)

    username = Column(String())

    productId = Column(Integer())
    productName = Column(String())

    price = Column(Float())

    def __repr__(self) -> str:
        return f""" id={self.id},
                    username={self.username},
                    productId={self.productId},
                    productName={self.productName},
                    price={self.price} """
