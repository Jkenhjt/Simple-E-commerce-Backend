from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from annotated_types import Annotated
from fastapi import Depends

import config

POSTGRESQL_URL = f"postgresql+asyncpg://{config.POSTGRESQL_USERNAME}:{config.POSTGRESQL_PASSWORD}@{config.POSTGRESQL_URL}:{config.POSTGRESQL_PORT}/{config.POSTGRESQL_DB_NAME}"
usersTableEngine = create_async_engine(POSTGRESQL_URL, echo=True, future=True)
productsTableEngine = create_async_engine(POSTGRESQL_URL, echo=True, future=True)
paymentsTableEngine = create_async_engine(POSTGRESQL_URL, echo=True, future=True)
shoppingCartTableEngine = create_async_engine(POSTGRESQL_URL, echo=True, future=True)


async def create_session_users():
    async with AsyncSession(usersTableEngine, expire_on_commit=False) as session:
        yield session


async def create_session_products():
    async with AsyncSession(productsTableEngine, expire_on_commit=False) as session:
        yield session


async def create_session_payments():
    async with AsyncSession(paymentsTableEngine, expire_on_commit=False) as session:
        yield session


async def create_session_shopping_cart():
    async with AsyncSession(shoppingCartTableEngine, expire_on_commit=False) as session:
        yield session


sessionUsers = Annotated[AsyncSession, Depends(create_session_users)]
sessionProducts = Annotated[AsyncSession, Depends(create_session_products)]
sessionPayments = Annotated[AsyncSession, Depends(create_session_payments)]
sessionShoppingCart = Annotated[AsyncSession, Depends(create_session_shopping_cart)]
