from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, String, Integer, Float


class BaseProduct(DeclarativeBase):
    pass


class ProductScheme(BaseProduct):
    __tablename__ = "Products"

    id = Column(Integer(), primary_key=True)

    name = Column(String())
    description = Column(String())
    price = Column(Float())

    quantity = Column(Integer())

    category = Column(String())

    imageName = Column(String())

    def __repr__(self) -> str:
        return f""" id={self.id},
                    name={self.name},
                    description={self.description},
                    price={self.price},
                    quantity={self.quantity},
                    category={self.category},
                    imageName={self.imageName} """
