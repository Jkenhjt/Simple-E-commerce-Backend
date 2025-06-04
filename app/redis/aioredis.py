import aioredis

import config


async def session_aioredis():
    return await aioredis.from_url(
        config.REDIS_URL, decode_responses=True, health_check_interval=3
    )
