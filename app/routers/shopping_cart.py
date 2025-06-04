from fastapi import APIRouter, Request, Response, HTTPException

from sqlalchemy import select, insert, delete
from sqlalchemy.exc import (
    NoResultFound,
    SQLAlchemyError,
    DataError,
    IntegrityError,
    DBAPIError,
)

from slowapi import Limiter
from slowapi.util import get_remote_address

import datetime

from database.db import sessionUsers, sessionShoppingCart, sessionProducts

from schemas.ShoppingCart import ShoppingCartScheme
from schemas.Product import ProductScheme

from utils import check_token, LOG


limiter = Limiter(key_func=get_remote_address)
routerShoppingCart = APIRouter()


@routerShoppingCart.get("/cart", tags=["Shopping cart"])
@limiter.limit("100/minute")
async def get_products_from_cart(
    request: Request,
    dbUser: sessionUsers,
    dbShoppingCart: sessionShoppingCart,
    dbProduct: sessionProducts,
):
    account = await check_token(request.cookies.get("session"), dbUser)

    try:
        cart = (
            await dbShoppingCart.execute(
                select(ShoppingCartScheme).where(
                    ShoppingCartScheme.username == account.username
                )
            )
        ).all()
        print(f"Length of finded products: {len(cart)}")

        productJson = []
        forLogs = []
        for product in cart:
            temp_json: dict[str] = {
                "id": product.tuple()[0].productId,
                "name": product.tuple()[0].productName,
                "price": product.tuple()[0].price,
            }
            productJson.append(temp_json)

            forLogs.append(
                f"name: {product.tuple()[0].productName}, price:{product.tuple()[0].price}, "
            )
            print(f"Product: {product}")
        forLogs = forLogs[-1][:-2]

        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} gets products: {''.join([string for string in forLogs])}"
        )
        LOG.info(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} gets products: {''.join([string for string in forLogs])}"
        )

        return productJson
    except DBAPIError as e:
        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to gets finded products: {''.join([string for string in forLogs])}"
        )
        LOG.error(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to gets finded products: {''.join([string for string in forLogs])}"
        )

        print(f"Error: {e}")

        await dbUser.rollback()
        await dbProduct.rollback()
        await dbShoppingCart.rollback()

        raise HTTPException(status_code=503, detail="Server connection error")
    except DataError as e:
        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to gets finded products: {''.join([string for string in forLogs])}"
        )
        LOG.error(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to gets finded products: {''.join([string for string in forLogs])}"
        )

        print(f"Error: {e}")

        await dbUser.rollback()
        await dbProduct.rollback()
        await dbShoppingCart.rollback()

        raise HTTPException(status_code=400, detail="Error input data")
    except IntegrityError as e:
        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to gets finded products: {''.join([string for string in forLogs])}"
        )
        LOG.error(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to gets finded products: {''.join([string for string in forLogs])}"
        )

        print(f"Error: {e}")

        await dbUser.rollback()
        await dbProduct.rollback()
        await dbShoppingCart.rollback()

        raise HTTPException(status_code=400, detail="Error input data")
    except NoResultFound as e:
        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to gets finded products: {''.join([string for string in forLogs])}"
        )
        LOG.error(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to gets finded products: {''.join([string for string in forLogs])}"
        )

        print(f"Error: {e}")

        await dbUser.rollback()
        await dbProduct.rollback()
        await dbShoppingCart.rollback()

        raise HTTPException(status_code=404, detail="Not found")
    except SQLAlchemyError as e:
        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to gets finded products: {''.join([string for string in forLogs])}"
        )
        LOG.error(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to gets finded products: {''.join([string for string in forLogs])}"
        )

        print(f"Error: {e}")

        await dbUser.rollback()
        await dbProduct.rollback()
        await dbShoppingCart.rollback()

        raise HTTPException(status_code=500, detail="Error server")


@routerShoppingCart.post("/cart", tags=["Shopping cart"])
@limiter.limit("100/minute")
async def add_product_to_cart(
    productID: int,
    request: Request,
    response: Response,
    dbUser: sessionUsers,
    dbShoppingCart: sessionShoppingCart,
    dbProduct: sessionProducts,
):
    account = await check_token(request.cookies.get("session"), dbUser)

    try:
        productDb = (
            await dbProduct.execute(
                select(ProductScheme).where(ProductScheme.id == productID)
            )
        ).scalar_one_or_none()
        if productDb == None:
            raise HTTPException(status_code=404, detail="Product not found")
        if productDb.quantity == 0:
            raise HTTPException(status_code=400, detail="Out of order")

        await dbShoppingCart.execute(
            insert(ShoppingCartScheme).values(
                username=account.username,
                productId=productID,
                productName=productDb.name,
                price=productDb.price,
            )
        )
        await dbShoppingCart.commit()

        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} added product to cart: {str(productID)}, {str(productDb.price)}"
        )
        LOG.info(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} added product to cart: {str(productID)}, {str(productDb.price)}"
        )

        return Response(status_code=200)
    except DBAPIError as e:
        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to add product to cart: {str(productID)}, {str(productDb.price)}"
        )
        LOG.error(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to add product to cart: {str(productID)}, {str(productDb.price)}"
        )

        print(f"Error: {e}")

        await dbUser.rollback()
        await dbProduct.rollback()
        await dbShoppingCart.rollback()

        raise HTTPException(status_code=503, detail="Server connnection error")
    except DataError as e:
        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to add product to cart: {str(productID)}, {str(productDb.price)}"
        )
        LOG.error(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to add product to cart: {str(productID)}, {str(productDb.price)}"
        )

        print(f"Error: {e}")

        await dbUser.rollback()
        await dbProduct.rollback()
        await dbShoppingCart.rollback()

        raise HTTPException(status_code=400, detail="Error input data")
    except IntegrityError as e:
        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to add product to cart: {str(productID)}, {str(productDb.price)}"
        )
        LOG.error(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to add product to cart: {str(productID)}, {str(productDb.price)}"
        )

        print(f"Error: {e}")

        await dbUser.rollback()
        await dbProduct.rollback()
        await dbShoppingCart.rollback()

        raise HTTPException(status_code=400, detail="Error input data")
    except NoResultFound as e:
        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to add product to cart: {str(productID)}, {str(productDb.price)}"
        )
        LOG.error(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to add product to cart: {str(productID)}, {str(productDb.price)}"
        )

        print(f"Error: {e}")

        await dbUser.rollback()
        await dbProduct.rollback()
        await dbShoppingCart.rollback()

        raise HTTPException(status_code=404, detail="Not found")
    except SQLAlchemyError as e:
        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to add product to cart: {str(productID)}, {str(productDb.price)}"
        )
        LOG.error(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to add product to cart: {str(productID)}, {str(productDb.price)}"
        )

        print(f"Error: {e}")

        await dbUser.rollback()
        await dbProduct.rollback()
        await dbShoppingCart.rollback()

        raise HTTPException(status_code=500, detail="Error server")


@routerShoppingCart.delete("/cart", tags=["Shopping cart"])
@limiter.limit("100/minute")
async def delete_product_from_cart(
    productID: int,
    request: Request,
    response: Response,
    dbUser: sessionUsers,
    dbShoppingCart: sessionShoppingCart,
):
    account = await check_token(request.cookies.get("session"), dbUser)

    try:
        await dbShoppingCart.execute(
            delete(ShoppingCartScheme).where(ShoppingCartScheme.id == productID)
        )
        await dbShoppingCart.commit()

        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} deletes product from cart: {str(productID)}"
        )
        LOG.info(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} deletes product from cart: {str(productID)}"
        )

        return Response(status_code=200)
    except DBAPIError as e:
        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to delete product from cart: {str(productID)}"
        )
        LOG.error(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to delete product from cart: {str(productID)}"
        )

        print(f"Error: {e}")

        await dbUser.rollback()
        await dbShoppingCart.rollback()

        raise HTTPException(status_code=503, detail="Server connection error")
    except DataError as e:
        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to delete product from cart: {str(productID)}"
        )
        LOG.error(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to delete product from cart: {str(productID)}"
        )

        print(f"Error: {e}")

        await dbUser.rollback()
        await dbShoppingCart.rollback()

        raise HTTPException(status_code=400, detail="Error input data")
    except IntegrityError as e:
        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to delete product from cart: {str(productID)}"
        )
        LOG.error(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to delete product from cart: {str(productID)}"
        )

        print(f"Error: {e}")

        await dbUser.rollback()
        await dbShoppingCart.rollback()

        raise HTTPException(status_code=400, detail="Error input data")
    except NoResultFound as e:
        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to delete product from cart: {str(productID)}"
        )
        LOG.error(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to delete product from cart: {str(productID)}"
        )

        print(f"Error: {e}")

        await dbUser.rollback()
        await dbShoppingCart.rollback()

        raise HTTPException(status_code=404, detail="Not found")
    except SQLAlchemyError as e:
        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to delete product from cart: {str(productID)}"
        )
        LOG.error(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host}|{account.username} tries to delete product from cart: {str(productID)}"
        )

        print(f"Error: {e}")

        await dbUser.rollback()
        await dbShoppingCart.rollback()

        raise HTTPException(status_code=500, detail="Error server")
