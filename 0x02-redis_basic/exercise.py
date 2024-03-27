#!/usr/bin/env pyhton3
"""
Module Docs
"""
import redis
from typing import Union, Callable, Optional
import uuid
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    count calls
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        wrapper
        """
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    
    return wrapper

def call_history(method: Callable) -> Callable:
    """
    call history
    """
    in_key = method.__qualname__ + ":inputs"
    out_key = method.__qualname__ + ":outputs"
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        wrapper
        """
        self._redis.rpush(in_key, str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(out_key, str(result))
        return result
    return wrapper

def replay(method: Callable) -> None:
    """
    replay
    """
    input_key = "{}:inputs".format(method.__qualname__)
    output_key = "{}:outputs".format(method.__qualname__)

    inputs = method.__self__._redis.lrange(input_key, 0, -1)
    outputs = method.__self__._redis.lrange(output_key, 0, -1)

    print("{} was called {} times:".format(method.__qualname__, len(inputs)))
    for inp, out in zip(inputs, outputs):
        print(
            "{}(*{}) -> {}".format(
                method.__qualname__, inp.decode("utf-8"), out.decode("utf-8")
            )
        )


class Cache:
    """
    Cache class
    """

    def __init__(self) -> None:
        """
        Instance of Cache
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        store method
        """
        rand_key = str(uuid.uuid4())
        self._redis.set(rand_key, data)
        return rand_key

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """
        converts data to desired format
        """
        value = self._redis.get(key)

        if fn:
            return fn(value)
        return value
    
    def get_str(self, key: str) -> str:
        """
        gets str value
        """
        return self.get(key, fn=str)
    
    def get_str(self, key: str) -> int:
        """
        gets int value
        """
        return self.get(key, fn=int)
