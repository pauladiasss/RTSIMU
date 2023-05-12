import asyncio
from functools import wraps
from typing import Awaitable, Callable, Any, List, Tuple


def run_async(*functions: Tuple[Callable, Tuple]) -> List[Any]:
    """
    Run a list of functions asynchronously
    :param functions: list of tuples containing an async function and its parameters.
    :return: list of results
    """
    async def _inner():
        return await asyncio.gather(*[fn(*params) for fn, params in functions])

    return asyncio.run(_inner())


def asynchronize(fn: Callable[..., Any]) -> Callable[..., Awaitable]:
    """
    Decorator to turn a function asynchronous
    :param fn: function to turn asynchronous
    :return: async function
    """
    @wraps(fn)
    async def wrapper(*args, **kwargs):
        return fn(*args, **kwargs)
    return wrapper