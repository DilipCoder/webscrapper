from utils.logger import logger
import asyncio
import inspect
import time

def retry_on_failure(retries=3):
    """
    Retries the function in case of failure.
    Args:
        retries (int): The number of retries to attempt.
    """
    def decorator(func):
        if inspect.iscoroutinefunction(func):
            async def async_wrapper(*args, **kwargs):
                for attempt in range(retries):
                    try:
                        return await func(*args, **kwargs)
                    except Exception as e:
                        logger.warning(f"Attempt {attempt + 1} failed: {e}")
                        await asyncio.sleep(2 ** attempt)
                raise Exception("All retries failed")
            return async_wrapper
        else:
            def sync_wrapper(*args, **kwargs):
                for attempt in range(retries):
                    try:
                        return func(*args, **kwargs)
                    except Exception as e:
                        logger.warning(f"Attempt {attempt + 1} failed: {e}")
                        time.sleep(2 ** attempt)
                raise Exception("All retries failed")
            return sync_wrapper
    return decorator