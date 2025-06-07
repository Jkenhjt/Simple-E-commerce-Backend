from fastapi import APIRouter, HTTPException, Request, Response

from sqlalchemy import select, insert, update
from sqlalchemy.exc import (
    NoResultFound,
    SQLAlchemyError,
    IntegrityError,
    DBAPIError,
    DataError,
)

import bcrypt

from database.db import sessionUsers

from models.User import UserModel

from schemas.User import UserScheme

from security.jwt import gen_jwt
from security.bcrypt import gen_secured

from slowapi import Limiter
from slowapi.util import get_remote_address

import datetime

import utils


limiter = Limiter(key_func=get_remote_address)
routerUser = APIRouter()


@routerUser.post("/register", tags=["Account"])
@limiter.limit("10/minute")
async def register(user: UserModel, request: Request, dbUsers: sessionUsers):
    try:
        result = await dbUsers.execute(
            select(UserScheme).where(UserScheme.username == user.username)
        )
        if result.scalar_one_or_none() != None:
            raise HTTPException(
                status_code=400, detail="This username is already registered"
            )
    except NoResultFound:
        pass

    try:
        await dbUsers.execute(
            insert(UserScheme).values(
                username=user.username,
                password=gen_secured(user.password),
                jwtToken="N/A",
                isAdmin=False,
                # isAdmin=True # enable it when testing
            )
        )
        await dbUsers.commit()

        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host} registered as {user.username}"
        )
        utils.LOG.info(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host} registered as {user.username}"
        )

        return Response(status_code=200)
    except DBAPIError as e:
        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host} tries register as {user.username}"
        )
        utils.LOG.error(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host} tries register as {user.username}"
        )

        print(f"Error: {e}")

        await dbUsers.rollback()

        raise HTTPException(status_code=503, detail="Server connection error")
    except DataError as e:
        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host} tries register as {user.username}"
        )
        utils.LOG.error(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host} tries register as {user.username}"
        )

        print(f"Error: {e}")

        await dbUsers.rollback()

        raise HTTPException(status_code=400, detail="Error input data")
    except IntegrityError as e:
        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host} tries register as {user.username}"
        )
        utils.LOG.error(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host} tries register as {user.username}"
        )

        print(f"Error: {e}")

        await dbUsers.rollback()

        raise HTTPException(status_code=400, detail="Error input data")
    except SQLAlchemyError as e:
        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host} tries register as {user.username}"
        )
        utils.LOG.error(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host} tries register as {user.username}"
        )

        print(f"Error: {e}")

        await dbUsers.rollback()

        raise HTTPException(status_code=500, detail="Error register account")


@routerUser.post("/login", tags=["Account"])
@limiter.limit("10/minute")
async def login(
    user: UserModel, request: Request, response: Response, dbUsers: sessionUsers
):
    isMatch: UserScheme = None
    try:
        isMatch = (
            await dbUsers.execute(
                select(UserScheme).where(UserScheme.username == user.username)
            )
        ).scalar_one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Error, check username or password")

    if not bcrypt.checkpw(user.password.encode(), isMatch.password):
        raise HTTPException(status_code=404, detail="Check username or password")

    try:
        if isMatch.jwtToken == "N/A":
            token: str = gen_jwt(isMatch.id, user.username)
            await dbUsers.execute(
                update(UserScheme)
                .where(UserScheme.id == isMatch.id)
                .values(jwtToken=token)
            )
            await dbUsers.commit()

            print(
                f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
                f"{request.client.host} loggined into {user.username}"
            )
            utils.LOG.info(
                f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
                f"{request.client.host} loggined into {user.username}"
            )

            response.status_code = 200
            response.set_cookie(key="session", value=token)
            return response
        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host} loggined into {user.username}"
        )
        utils.LOG.info(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host} loggined into {user.username}"
        )

        response.status_code = 200
        response.set_cookie(key="session", value=isMatch.jwtToken)
        return response
    except DBAPIError as e:
        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host} tries to loggin in as {user.username}"
        )
        utils.LOG.error(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host} tries to loggin in as {user.username}"
        )

        print(f"Error: {e}")

        await dbUsers.rollback()

        raise HTTPException(status_code=503, detail="Server connection error")
    except DataError as e:
        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host} tries to loggin in as {user.username}"
        )
        utils.LOG.error(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host} tries to loggin in as {user.username}"
        )

        print(f"Error: {e}")

        await dbUsers.rollback()

        raise HTTPException(status_code=400, detail="Error input data")
    except IntegrityError as e:
        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host} tries to loggin in as {user.username}"
        )
        utils.LOG.error(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host} tries to loggin in as {user.username}"
        )

        print(f"Error: {e}")

        await dbUsers.rollback()

        raise HTTPException(status_code=400, detail="Error input data")
    except NoResultFound as e:
        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host} tries to loggin in as {user.username}"
        )
        utils.LOG.error(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host} tries to loggin in as {user.username}"
        )

        print(f"Error: {e}")

        await dbUsers.rollback()

        raise HTTPException(status_code=404, detail="Error not found")
    except SQLAlchemyError as e:
        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host} tries to loggin in as {user.username}"
        )
        utils.LOG.error(
            f"[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] "
            f"{request.client.host} tries to loggin in as {user.username}"
        )

        print(f"Error: {e}")

        await dbUsers.rollback()

        raise HTTPException(status_code=500, detail="Error loggin in account")
