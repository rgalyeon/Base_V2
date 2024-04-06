from loguru import logger
from settings import RETRY_COUNT
from utils.sleeping import sleep
from functools import wraps


def retry(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        retries = 0
        while retries <= RETRY_COUNT:
            try:
                result = await func(*args, **kwargs)
                return result
            except Exception as e:
                import traceback

                traceback.print_exc()
                logger.error(f"Error | {e}")
                await sleep(10, 20)
                retries += 1

    return wrapper
