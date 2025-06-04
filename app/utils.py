import logging
from fastapi import HTTPException

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

import aiofiles

from database.db import sessionUsers

from schemas.User import UserScheme


LOG = logging.getLogger(__name__)
logging.basicConfig(filename="./logs.log", level=logging.INFO)


async def check_token(token: str, dbUsers: sessionUsers):
    try:
        account = (
            await dbUsers.execute(
                select(UserScheme).where(UserScheme.jwtToken == token)
            )
        ).scalar_one_or_none()
        if account == None:
            raise HTTPException(
                status_code=401,
                detail="Authorize the account again because your token will expire.",
            )

        return account
    except NoResultFound:
        raise HTTPException(
            status_code=401,
            detail="Authorize the account again because your token will expire.",
        )


async def get_image_bytes(path: str) -> bytes:
    async with aiofiles.open(path, mode="rb") as f:
        imageInBytes = await f.read()
    return imageInBytes
