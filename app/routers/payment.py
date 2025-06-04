from fastapi import APIRouter, Request, Response, HTTPException

from sqlalchemy import select, insert
from sqlalchemy.exc import (
    NoResultFound,
    SQLAlchemyError,
    DataError,
    IntegrityError,
    DBAPIError,
)

from database.db import sessionUsers, sessionPayments, sessionShoppingCart

from schemas.Payment import PaymentScheme
from schemas.ShoppingCart import ShoppingCartScheme

from models.Payment import PaymentModel

from security.bcrypt import gen_secured

from slowapi import Limiter
from slowapi.util import get_remote_address

from utils import check_token
import utils

import datetime
import hashlib


limiter = Limiter(key_func=get_remote_address)
routerPayment = APIRouter()


@routerPayment.post("/payment", tags=["Payment"])
@limiter.limit("5/minute")
async def payment(
    payment: PaymentModel,
    request: Request,
    dbUsers: sessionUsers,
    dbPayments: sessionPayments,
    dbShoppingCart: sessionShoppingCart,
):
    account = await check_token(request.cookies.get("session"), dbUsers)
    names: str = ""
    priceSum: float = 0.0

    if len(payment.cardNumber) != 16 or not payment.cardNumber.isnumeric():
        raise HTTPException(status_code=400, detail="Incorrect card number")
    if len(payment.cardDate) != 5 or payment.cardDate[2] != "/":
        raise HTTPException(status_code=400, detail="Incorrect date")
    if len(payment.cardCVV) > 4 or not payment.cardCVV.isnumeric():
        raise HTTPException(status_code=400, detail="Incorrect CVV")

    try:
        pricesDb = await dbShoppingCart.execute(
            select(ShoppingCartScheme).where(
                ShoppingCartScheme.username == account.username
            )
        )

        for i in pricesDb.all():
            priceSum += i.tuple()[0].price
            names += str(i.tuple()[0].id) + ", "
        names = names[:-2]
    except NoResultFound:
        raise HTTPException(status_code=503, detail="Server error, try later")

    try:
        hashPayment = hashlib.md5(
            gen_secured(account.username)
            + gen_secured(payment.cardNumber)
            + gen_secured(payment.cardDate)
            + gen_secured(payment.cardCVV)
            + gen_secured(datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
        )

        await dbPayments.execute(
            insert(PaymentScheme).values(
                username=account.username,
                buyerCard=payment.cardNumber,
                buyerCardCVV=payment.cardCVV,
                buyerCardDate=payment.cardDate,
                cartProducts=names,
                price=priceSum,
                hashPayment=hashPayment.hexdigest(),
                date=datetime.datetime.now().strftime("%H:%M:%S %d-%m-%Y"),
            )
        )
        await dbUsers.commit()

        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} gets finded products ids: {names}"
        )
        utils.LOG.info(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} gets finded products ids: {names}"
        )

        return Response(status_code=200)
    except DBAPIError as e:
        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to gets finded products ids: {names}"
        )
        utils.LOG.error(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to gets finded products ids: {names}"
        )

        print(f"Error: {e}")

        await dbUsers.rollback()
        await dbPayments.rollback()
        await dbShoppingCart.rollback()

        raise HTTPException(status_code=503, detail="Server connection error")
    except DataError as e:
        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to gets finded products ids: {names}"
        )
        utils.LOG.error(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to gets finded products ids: {names}"
        )

        print(f"Error: {e}")

        await dbUsers.rollback()
        await dbPayments.rollback()
        await dbShoppingCart.rollback()

        raise HTTPException(status_code=400, detail="Error input data")
    except IntegrityError as e:
        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to gets finded products ids: {names}"
        )
        utils.LOG.error(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to gets finded products ids: {names}"
        )

        print(f"Error: {e}")

        await dbUsers.rollback()
        await dbPayments.rollback()
        await dbShoppingCart.rollback()

        raise HTTPException(status_code=400, detail="Error input data")
    except NoResultFound as e:
        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to gets finded products ids: {names}"
        )
        utils.LOG.error(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to gets finded products ids: {names}"
        )

        print(f"Error: {e}")

        await dbUsers.rollback()
        await dbPayments.rollback()
        await dbShoppingCart.rollback()

        raise HTTPException(status_code=404, detail="Not found")
    except SQLAlchemyError as e:
        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to gets finded products ids: {names}"
        )
        utils.LOG.error(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to gets finded products ids: {names}"
        )

        print(f"Error: {e}")

        await dbUsers.rollback()
        await dbPayments.rollback()
        await dbShoppingCart.rollback()

        raise HTTPException(status_code=500, detail="Error server")
