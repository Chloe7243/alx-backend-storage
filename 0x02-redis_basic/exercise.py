#!/usr/bin/env python3
'''
    Redis Basics
'''
from typing import Callable, Optional, Union
from uuid import uuid4
import redis
from functools import wraps


def count_calls(method: Callable) -> Callable:
    '''
        Decorator Function that counts the number of calls.
    '''

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        '''
            Wrapper function.
        '''
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    '''
        Decorator to store the history
        of inputs and outputs for a particular function.
    '''
    key = method.__qualname__
    inputs = key + ':inputs'
    outputs = key + ':outputs'
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        '''
            Wrapper function.
        '''
        self._redis.rpush(inputs, str(args))
        data = method(self, *args, **kwargs)
        self._redis.rpush(outputs, str(data))
        return data
    return wrapper


def replay(method: Callable) -> None:
    '''
        Display the history of calls of a particular function.
    '''
    cache = redis.Redis()
    key = method.__qualname__
    n_calls = cache.get(key).decode('utf-8')
    print(f'{key} was called {n_calls} times:')

    inputs = cache.lrange(key + ':inputs', 0, -1)
    outputs = cache.lrange(key + ':outputs', 0, -1)
    for i, o in zip(inputs, outputs):
        input = i.decode('utf-8')
        output = o.decode('utf-8')
        print(f'{key}(*{input}) -> {output}')


class Cache:
    ''' Cache class '''

    def __init__(self):
        '''
            Initialize cache data.
        '''
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''
            Store data in cache.
        '''
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        '''
            Get data from cache.
        '''
        data = self._redis.get(key)

        if fn:
            data = fn(data)

        return data

    def get_str(self, key: str) -> str:
        '''
            Get string from cache.
        '''
        return self._redis.get(key).decode('utf-8')

    def get_int(self, key: str) -> int:
        '''
            Get int from cache.
        '''
        data = self._redis.get(key)

        try:
            data = int(data.decode('utf-8'))
        except Exception:
            data = 0

        return data
