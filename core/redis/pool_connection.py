from aioredis import Redis, from_url

from config import config

global_settings = config.Settings()


async def init_redis_pool() -> Redis:

    if global_settings.redis_password:
        redis = await from_url(
            global_settings.redis_url,
            password=global_settings.redis_password,
            decode_responses=True,
            db=global_settings.redis_db,
        )

    redis = await from_url(
        global_settings.redis_url,
        decode_responses=True,
        db=global_settings.redis_db,
    )

    return redis
