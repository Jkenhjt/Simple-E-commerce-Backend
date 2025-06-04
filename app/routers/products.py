from fastapi import APIRouter, Request, Response, HTTPException
from fastapi.responses import FileResponse

from sqlalchemy import select, insert, delete, update, func
from sqlalchemy.exc import (
    NoResultFound,
    DBAPIError,
    SQLAlchemyError,
    IntegrityError,
    DataError,
)

from asyncpg.exceptions import DataError

from slowapi import Limiter
from slowapi.util import get_remote_address

from database.db import sessionProducts, sessionUsers

from models.Product import ProductModel
from models.Product import ProductDeleteModel

from schemas.Product import ProductScheme

from utils import LOG, check_token

import datetime


limiter = Limiter(key_func=get_remote_address)
routerProduct = APIRouter()


# Admin Panel
@routerProduct.post("/admin/add_product", tags=["Admin"])
async def add_product(
    product: ProductModel,
    request: Request,
    dbUsers: sessionUsers,
    dbProducts: sessionProducts,
):
    account = await check_token(request.cookies.get("session"), dbUsers)
    if account.isAdmin == False:
        raise HTTPException(status_code=404)

    try:
        await dbProducts.execute(
            insert(ProductScheme).values(
                name=product.name,
                description=product.description,
                price=float("{:.2f}".format(product.price)),
                quantity=product.quantity,
                category=product.category,
                imageName=product.imageName,
            )
        )
        await dbProducts.commit()

        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} added product {product.name}"
        )
        LOG.info(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} added product {product.name}"
        )

        return Response(status_code=200)
    except DBAPIError as e:
        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to add product {product.name}"
        )
        LOG.error(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to add product {product.name}"
        )

        print(f"Error: {e}")

        await dbUsers.rollback()
        await dbProducts.rollback()

        raise HTTPException(status_code=503, detail="Server connection error")
    except DataError as e:
        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to add product {product.name}"
        )
        LOG.error(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to add product {product.name}"
        )

        print(f"Error: {e}")

        await dbUsers.rollback()
        await dbProducts.rollback()

        raise HTTPException(status_code=400, detail="Error input data")
    except IntegrityError as e:
        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to add product {product.name}"
        )
        LOG.error(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to add product {product.name}"
        )

        print(f"Error: {e}")

        await dbUsers.rollback()
        await dbProducts.rollback()

        raise HTTPException(status_code=400, detail="Error input data")
    except NoResultFound as e:
        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to add product {product.name}"
        )
        LOG.error(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to add product {product.name}"
        )

        print(f"Error: {e}")

        await dbUsers.rollback()
        await dbProducts.rollback()

        raise HTTPException(status_code=404, detail="Not found")
    except SQLAlchemyError as e:
        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to add product {product.name}"
        )
        LOG.error(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to add product {product.name}"
        )

        print(f"Error: {e}")

        await dbUsers.rollback()
        await dbProducts.rollback()

        raise HTTPException(status_code=500, detail="Error server")


@routerProduct.post("/admin/update_product/{id}", tags=["Admin"])
async def update_product(
    product: ProductModel,
    id: int,
    request: Request,
    dbUsers: sessionUsers,
    dbProducts: sessionProducts,
):
    account = await check_token(request.cookies.get("session"), dbUsers)
    if account.isAdmin == False:
        raise HTTPException(status_code=404)

    try:
        await dbProducts.execute(
            update(ProductScheme)
            .where(ProductScheme.id == id)
            .values(
                name=product.name,
                description=product.description,
                price=product.price,
                quantity=product.quantity,
                category=product.category,
                imageName=product.imageName,
            )
        )
        await dbProducts.commit()

        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} update product {str(id)}"
        )
        LOG.info(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} update product {str(id)}"
        )

        return Response(status_code=200)
    except DBAPIError as e:
        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to update product {str(id)}"
        )
        LOG.error(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to update product {str(id)}"
        )

        await dbUsers.rollback()
        await dbProducts.rollback()

        raise HTTPException(status_code=503, detail="Server connection error")
    except DataError as e:
        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to update product {str(id)}"
        )
        LOG.error(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to update product {str(id)}"
        )

        await dbUsers.rollback()
        await dbProducts.rollback()

        raise HTTPException(status_code=400, detail="Error input data")
    except IntegrityError as e:
        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to update product {str(id)}"
        )
        LOG.error(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to update product {str(id)}"
        )

        await dbUsers.rollback()
        await dbProducts.rollback()

        raise HTTPException(status_code=400, detail="Error input data")
    except NoResultFound as e:
        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to update product {str(id)}"
        )
        LOG.error(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to update product {str(id)}"
        )

        print(f"Error: {e}")

        await dbUsers.rollback()
        await dbProducts.rollback()

        raise HTTPException(status_code=404, detail="Not found")
    except SQLAlchemyError as e:
        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to update product {str(id)}"
        )
        LOG.error(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to update product {str(id)}"
        )

        await dbUsers.rollback()
        await dbProducts.rollback()

        raise HTTPException(status_code=500, detail="Error server")


@routerProduct.delete("/admin/delete_product", tags=["Admin"])
async def delete_product(
    product: ProductDeleteModel,
    request: Request,
    dbUsers: sessionUsers,
    dbProducts: sessionProducts,
):
    account = await check_token(request.cookies.get("session"), dbUsers)
    if account.isAdmin == False:
        raise HTTPException(status_code=404)

    try:
        await dbProducts.execute(
            delete(ProductScheme).where(ProductScheme.id == product.id)
        )
        await dbProducts.commit()

        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} delete product {str(product.id)}"
        )
        LOG.info(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} delete product {str(product.id)}"
        )

        return Response(status_code=200)
    except DBAPIError as e:
        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to delete product {str(product.id)}"
        )
        LOG.error(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to delete product {str(product.id)}"
        )

        print(f"Error: {e}")

        await dbUsers.rollback()
        await dbProducts.rollback()

        raise HTTPException(status_code=503, detail="Server connection error")
    except DataError as e:
        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to delete product {str(product.id)}"
        )
        LOG.error(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to delete product {str(product.id)}"
        )

        print(f"Error: {e}")

        await dbUsers.rollback()
        await dbProducts.rollback()

        raise HTTPException(status_code=400, detail="Error input data")
    except IntegrityError as e:
        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to delete product {str(product.id)}"
        )
        LOG.error(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to delete product {str(product.id)}"
        )

        print(f"Error: {e}")

        await dbUsers.rollback()
        await dbProducts.rollback()

        raise HTTPException(status_code=400, detail="Error input data")
    except NoResultFound as e:
        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to delete product {str(product.id)}"
        )
        LOG.error(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to delete product {str(product.id)}"
        )

        print(f"Error: {e}")

        await dbUsers.rollback()
        await dbProducts.rollback()

        raise HTTPException(status_code=404, detail="Not found")
    except SQLAlchemyError as e:
        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to delete product {str(product.id)}"
        )
        LOG.error(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to delete product {str(product.id)}"
        )

        print(f"Error: {e}")

        await dbUsers.rollback()
        await dbProducts.rollback()

        raise HTTPException(status_code=500, detail="Error server")


# User usage
@routerProduct.get("/", tags=["Products"])
@limiter.limit("100/minute")
async def index(request: Request, dbUsers: sessionUsers, dbProducts: sessionProducts):
    try:
        products = await dbProducts.execute(
            select(ProductScheme).order_by(func.random()).limit(20)
        )

        ids: str = ""
        for i in products.all():
            ids += str(i.tuple()[0].id) + ", "
            print(i.tuple()[0].id)
        ids = ids[:-2]

        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host} gets products from index {ids}"
        )
        LOG.info(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host} gets products from index {ids}"
        )

        return "".join(products.all())
    except DBAPIError as e:
        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host} tries to get products from index {ids}"
        )
        LOG.error(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host} tries to get products from index {ids}"
        )

        print(f"Error: {e}")

        await dbUsers.rollback()
        await dbProducts.rollback()

        raise HTTPException(status_code=503, detail="Server connection error")
    except DataError as e:
        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host} tries to get products from index {ids}"
        )
        LOG.error(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host} tries to get products from index {ids}"
        )

        print(f"Error: {e}")

        await dbUsers.rollback()
        await dbProducts.rollback()

        raise HTTPException(status_code=400, detail="Error input data")
    except IntegrityError as e:
        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host} tries to get products from index {ids}"
        )
        LOG.error(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host} tries to get products from index {ids}"
        )

        print(f"Error: {e}")

        await dbUsers.rollback()
        await dbProducts.rollback()

        raise HTTPException(status_code=400, detail="Error input data")
    except SQLAlchemyError as e:
        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host} tries to get products from index {ids}"
        )
        LOG.error(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host} tries to get products from index {ids}"
        )

        print(f"Error: {e}")

        await dbUsers.rollback()
        await dbProducts.rollback()

        raise HTTPException(status_code=500, detail="Error server")
    except SQLAlchemyError as e:
        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host} tries to get products from index {ids}"
        )
        LOG.error(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host} tries to get products from index {ids}"
        )

        print(f"Error: {e}")

        await dbUsers.rollback()
        await dbProducts.rollback()

        raise HTTPException(status_code=500, detail="Error server")


@routerProduct.get("/product", tags=["Products"])
@limiter.limit("100/minute")
async def product(
    id: int, request: Request, dbProducts: sessionProducts, dbUsers: sessionUsers
):
    if id >= 2147483647:
        raise HTTPException(status_code=400, detail="Bad id")

    redisResponse = await request.app.state.aioredis_session.hgetall((str(id)))
    if redisResponse != None and redisResponse != {}:
        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host} gets finded product: {redisResponse['name']}"
        )
        LOG.info(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host} gets finded product: {redisResponse['name']}"
        )

        return redisResponse

    try:
        productDb = (
            await dbProducts.execute(
                select(ProductScheme).where(ProductScheme.id == id)
            )
        ).scalar_one()

        await request.app.state.aioredis_session.hset(
            str(id),
            mapping={
                "name": productDb.name,
                "description": productDb.description,
                "price": productDb.price,
                "category": productDb.category,
                "quantity": productDb.quantity,
                "imageName": productDb.imageName,
            },
        )

        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host} gets finded product: {productDb.name}"
        )
        LOG.info(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host} gets finded product: {productDb.name}"
        )

        return {
            "name": productDb.name,
            "description": productDb.description,
            "price": productDb.price,
            "category": productDb.category,
            "quantity": productDb.quantity,
            "imageName": productDb.imageName,
        }
    except DBAPIError as e:
        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host} tries to get finded product"
        )
        LOG.error(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host} tries to get finded product"
        )

        print(f"Error: {e}")

        await dbUsers.rollback()
        await dbProducts.rollback()

        raise HTTPException(status_code=503, detail="Server connection error")
    except DataError as e:
        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host} tries to get finded product"
        )
        LOG.error(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host} tries to get finded product"
        )

        print(f"Error: {e}")

        await dbUsers.rollback()
        await dbProducts.rollback()

        raise HTTPException(status_code=400, detail="Error input data")
    except IntegrityError as e:
        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host} tries to get finded product"
        )
        LOG.error(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host} tries to get finded product"
        )

        print(f"Error: {e}")

        await dbUsers.rollback()
        await dbProducts.rollback()

        raise HTTPException(status_code=400, detail="Error input data")
    except NoResultFound as e:
        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host} tries to get finded product"
        )
        LOG.error(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host} tries to get finded product"
        )

        print(f"Error: {e}")

        await dbUsers.rollback()
        await dbProducts.rollback()

        raise HTTPException(status_code=404, detail="Not found")
    except SQLAlchemyError as e:
        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host} tries to get finded product"
        )
        LOG.error(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host} tries to get finded product"
        )

        print(f"Error: {e}")

        await dbUsers.rollback()
        await dbProducts.rollback()

        raise HTTPException(status_code=500, detail="Error server")


@routerProduct.get("/image", tags=["Products"])
@limiter.limit("100/minute")
async def get_image(imageName: str, request: Request):
    if imageName.find("/") != -1:
        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host} tries to get image"
        )
        LOG.error(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host} tries to get image"
        )

        raise HTTPException(status_code=400, detail="Bad image name")

    print(
        f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
        f"{request.client.host} gets image: {imageName}"
    )
    LOG.info(
        f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
        f"{request.client.host} gets image: {imageName}"
    )

    return FileResponse("./images/" + imageName)


@routerProduct.get("/products", tags=["Products"])
@limiter.limit("100/minute")
async def products(
    limit: int = 10000,
    offset: int = 0,
    category: str = None,
    productName: str = None,
    request: Request = None,
    dbUsers: sessionUsers = None,
    dbProducts: sessionProducts = None,
):
    account = await check_token(request.cookies.get("session"), dbUsers)
    if limit > 10000:
        raise HTTPException(status_code=400, detail="Too large limit value")
    if offset > 10000:
        raise HTTPException(status_code=400, detail="Too large offset value")

    try:
        if category != None:
            if productName != None:
                results = await dbProducts.execute(
                    select(ProductScheme)
                    .where(ProductScheme.name == productName)
                    .offset(offset)
                    .limit(limit)
                    .filter_by(category=category)
                )
            else:
                results = await dbProducts.execute(
                    select(ProductScheme)
                    .offset(offset)
                    .limit(limit)
                    .filter_by(category=category)
                )
        else:
            if productName != None:
                results = await db_products.execute(
                    select(ProductScheme)
                    .where(ProductScheme.name == productName)
                    .offset(offset)
                    .limit(limit)
                )
            else:
                results = await db_products.execute(
                    select(ProductScheme).offset(offset).limit(limit)
                )

        ret: list[ProductScheme] = []
        for i in results.all():
            ret.append(i.tuple()[0])

        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} gets finded products: {''.join([i.tuple()[0].name for i in results.all()])}"
        )
        LOG.info(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} gets finded products: {''.join([i.tuple()[0].name for i in results.all()])}"
        )

        return ret
    except DBAPIError as e:
        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to gets finded products"
        )
        LOG.error(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to gets finded products"
        )

        print(f"Error: {e}")

        await dbUsers.rollback()
        await dbProducts.rollback()

        raise HTTPException(status_code=500, detail="Server connection error")
    except DataError as e:
        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to gets finded products"
        )
        LOG.error(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to gets finded products"
        )

        print(f"Error: {e}")

        await dbUsers.rollback()
        await dbProducts.rollback()

        raise HTTPException(status_code=400, detail="Data error")
    except IntegrityError as e:
        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to gets finded products"
        )
        LOG.error(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to gets finded products"
        )

        print(f"Error: {e}")

        await dbUsers.rollback()
        await dbProducts.rollback()

        raise HTTPException(status_code=400, detail="Too large value")
    except NoResultFound as e:
        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to gets finded products"
        )
        LOG.error(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to gets finded products"
        )

        print(f"Error: {e}")

        await dbUsers.rollback()
        await dbProducts.rollback()

        raise HTTPException(status_code=404, detail="Not found")
    except SQLAlchemyError as e:
        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to gets finded products"
        )
        LOG.error(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to gets finded products"
        )

        print(f"Error: {e}")

        await dbUsers.rollback()
        await dbProducts.rollback()

        raise HTTPException(status_code=503, detail="Error server")
