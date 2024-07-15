import json
from functools import wraps
from app.extensions.diskcache import cache
from fastapi.exceptions import RequestValidationError, ResponseValidationError

import requests


async def save_cache(cache_key, func, *args, cache_time, **kwargs):
    data = await func(*args, **kwargs)
    if data:
        cache.set(cache_key, data, cache_time)
    else:
        cache.set(cache_key, {"message": "查询失败，请1分钟后再次尝试"}, 60)


def check_valid(url, proxy_server):
    try:
        requests.get(url, timeout=5, proxies={"http": proxy_server})
    except Exception as e:
        print(str(e))
        raise RequestValidationError({"message": "请检查代理地址跟目标地址是否可用"})

    return


def cache_route(cache_time=600):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, background_tasks, **kwargs):
            check_valid(kwargs["query_params"].url, kwargs["query_params"].proxy_server)
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
