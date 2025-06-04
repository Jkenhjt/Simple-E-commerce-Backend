from pydantic import BaseModel


class PaymentModel(BaseModel):
    cardNumber: str
    cardDate: str
    cardCVV: str
