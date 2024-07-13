import json
from functools import wraps
from app.extensions.diskcache import cache


async def save_cache(cache_key, func, *args, cache_time, **kwargs):
    data = await func(*args, **kwargs)
    cache.set(cache_key, data, cache_time)


def cache_route(cache_time=600):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, background_tasks, **kwargs):
            # 生成缓存的键
            args_key = ".".join([str(k) for k in args])
            cache_key = "func:{}:{}-{}".format(func.__name__, args_key, json.dumps(kwargs, default=str))
            # print("cache_key", cache_key)
            data = cache.get(cache_key)
            if data:
                return data
            data = {"message": "正在解密 cloudflare 5s 盾，请继续轮询"}
            cache.set(cache_key, data, expire=60)
            background_tasks.add_task(
                save_cache, cache_key, func, *args, background_tasks=background_tasks, cache_time=cache_time, **kwargs
            )
            return data

        return wrapper

    return decorator
