import asyncio
import pytest

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

import bcrypt
import authlib


from database.db import (
    productsTableEngine,
    shoppingCartTableEngine,
    paymentsTableEngine,
    usersTableEngine,
)

from redis.aioredis import session_aioredis

from schemas.Product import ProductScheme
from schemas.ShoppingCart import ShoppingCartScheme
from schemas.Payment import PaymentScheme
from schemas.User import UserScheme

from security.bcrypt import gen_secured
from security.jwt import gen_jwt, key

from utils import get_image_bytes


# Testing db


class TestDB:
    @pytest.mark.asyncio
    async def test_products_table(self):
        async with AsyncSession(
            productsTableEngine, expire_on_commit=False
        ) as db_session:
            await db_session.execute(
                insert(ProductScheme).values(
                    id=10,
                    name="123",
                    description="123123",
                    price=12.34,
                    quantity=23,
                    category="temp product",
                    imageName="2.png",
                )
            )

            data = (
                await db_session.execute(
                    select(ProductScheme).where(ProductScheme.id == 10)
                )
            ).scalar_one_or_none()

            assert data != None
            assert data.name == "123"
            assert data.description == "123123"
            assert data.price == 12.34
            assert data.quantity == 23
            assert data.category == "temp product"
            assert data.imageName == "2.png"

    @pytest.mark.asyncio
    async def test_payment_table(self):
        async with AsyncSession(
            paymentsTableEngine, expire_on_commit=False
        ) as db_session:
            await db_session.execute(
                insert(PaymentScheme).values(
                    id=10,
                    username="123",
                    buyerCard="123123",
                    buyerCardDate="12.34",
                    buyerCardCVV="23",
                    cartProducts="temp product",
                    price=123.345,
                    hashPayment="skajdhasjkdha hash asjkdakhjsjkh",
                    date="98/76/5432",
                )
            )

            data = (
                await db_session.execute(
                    select(PaymentScheme).where(PaymentScheme.id == 10)
                )
            ).scalar_one_or_none()

            assert data != None
            assert data.username == "123"
            assert data.buyerCard == "123123"
            assert data.buyerCardDate == "12.34"
            assert data.buyerCardCVV == "23"
            assert data.cartProducts == "temp product"
            assert data.price == 123.345
            assert data.hashPayment == "skajdhasjkdha hash asjkdakhjsjkh"
            assert data.date == "98/76/5432"

    @pytest.mark.asyncio
    async def test_shopping_cart_table(self):
        async with AsyncSession(
            shoppingCartTableEngine, expire_on_commit=False
        ) as db_session:
            await db_session.execute(
                insert(ShoppingCartScheme).values(
                    id=10,
                    username="123",
                    productId=123123,
                    productName="12.34",
                    price=123.345,
                )
            )

            data = (
                await db_session.execute(
                    select(ShoppingCartScheme).where(ShoppingCartScheme.id == 10)
                )
            ).scalar_one_or_none()

            assert data != None
            assert data.username == "123"
            assert data.productId == 123123
            assert data.productName == "12.34"
            assert data.price == 123.345

    @pytest.mark.asyncio
    async def test_users_table(self):
        async with AsyncSession(usersTableEngine, expire_on_commit=False) as db_session:
            await db_session.execute(
                insert(UserScheme).values(
                    id=10,
                    username="123",
                    password=b"password",
                    jwtToken="tokentoken",
                    isAdmin=True,
                )
            )

            data = (
                await db_session.execute(select(UserScheme).where(UserScheme.id == 10))
            ).scalar_one_or_none()

            assert data != None
            assert data.username == "123"
            assert data.password == b"password"
            assert data.jwtToken == "tokentoken"
            assert data.isAdmin == True


# Testing aioredis


@pytest.mark.asyncio
async def test_session_aioredis():
    session_aioredis_ = await session_aioredis()

    await session_aioredis_.set("test_data", "test_response_from_aioredis")

    data = await session_aioredis_.get("test_data")

    assert data == "test_response_from_aioredis"


# Testing security


def test_bcrypt():
    password: str = "passwordtesting"

    hash_ = gen_secured(password)

    assert bcrypt.checkpw(password.encode(), hash_) == True


def test_jwt():
    id: int = 1234567890
    username: str = "username"

    jwt_token = authlib.jose.jwt.decode(gen_jwt(id, username), key)

    assert jwt_token["sub"] == 1234567890
    assert jwt_token["name"] == "username"


# Testing util's


def test_check_token():
    return


@pytest.mark.asyncio
async def test_get_image_bytes():
    data: bytes = await get_image_bytes("/fastapi/app/tests/2.png")

    assert len(data) != 0
