from pydantic import BaseModel


class ProductModel(BaseModel):
    name: str
    description: str
    price: float

    quantity: int

    category: str

    imageName: str


class ProductDeleteModel(BaseModel):
    id: int
