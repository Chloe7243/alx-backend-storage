#!/usr/bin/env python3
'''
    Redis Basics
'''
from typing import Callable
import redis
import requests
from functools import wraps


def track_requests(method: Callable) -> Callable:
    '''
        Decorator that counts the number of requests to a url
        and caches the responses for 10 seconds.
    '''

    @wraps(method)
    def wrapper(url: str) -> str:
        '''
            The wrapper function.
        '''
        cache = redis.Redis()
        cache.incr(f'count:{url}')
        cached_res = cache.get(f'cached:{url}')
        if cached_res:
            return cached_res.decode('utf-8')
        res = method(url)
        cache.set(f'cached:{url}', res, ex=10)
        return res
    return wrapper


@track_requests
def get_page(url: str) -> str:
    '''
        Gets a page content.
    '''
    return requests.get(url).text
