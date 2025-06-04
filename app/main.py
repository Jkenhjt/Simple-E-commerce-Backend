from fastapi import FastAPI, Response

from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.exc import IntegrityError


from database.db import (
    usersTableEngine,
    productsTableEngine,
    paymentsTableEngine,
    shoppingCartTableEngine,
)

from redis.aioredis import session_aioredis

from schemas.User import BaseUser
from schemas.Payment import BasePayment
from schemas.Product import BaseProduct
from schemas.ShoppingCart import BaseShoppingCart

from routers.users import routerUser
from routers.products import routerProduct
from routers.payment import routerPayment
from routers.shopping_cart import routerShoppingCart


tagsMetadata = [
    {
        "name": "Account",
        "description": "Endpoint for creating and logging into an account",
    },
    {"name": "Admin", "description": "Only for admin marked in db usage."},
    {"name": "Products", "description": "Endpoint for getting products data"},
    {"name": "Payment", "description": "Create receipt for the payment"},
    {"name": "Shopping cart", "description": "Your shopping cart"},
]

app = FastAPI(
    title="E-Commerce",
    description="#### Simple e-commerce backend",
    version="1.0.0",
    openapi_tags=tagsMetadata,
    contact={
        "name": None,
        "email": None,
        "url": "https://github.com/Jkenhjt",
    },
    terms_of_service="",
    license_info={"name": "MIT License", "url": "https://mit-license.org/"},
    docs_url="/docs",
    redoc_url=None,
)

app.add_middleware(GZipMiddleware, minimum_size=500, compresslevel=9)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routerUser)
app.include_router(routerProduct)
app.include_router(routerPayment)
app.include_router(routerShoppingCart)


@app.on_event("startup")
async def start():
    async with usersTableEngine.begin() as conn:
        try:
            await conn.run_sync(BaseUser.metadata.create_all)
        except IntegrityError:
            pass

    async with paymentsTableEngine.begin() as conn:
        try:
            await conn.run_sync(BasePayment.metadata.create_all)
        except IntegrityError:
            pass

    async with productsTableEngine.begin() as conn:
        try:
            await conn.run_sync(BaseProduct.metadata.create_all)
        except IntegrityError:
            pass

    async with shoppingCartTableEngine.begin() as conn:
        try:
            await conn.run_sync(BaseShoppingCart.metadata.create_all)
        except IntegrityError:
            pass

    app.state.aioredis_session = await session_aioredis()


@app.on_event("shutdown")
async def shutdown():
    await usersTableEngine.dispose()
    await productsTableEngine.dispose()
    await paymentsTableEngine.dispose()
    await shoppingCartTableEngine.dispose()

    await app.state.aioredis_session.close()
