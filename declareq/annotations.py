import functools
from typing import Dict, List

from declareq import interfaces
from declareq.commands import Builder
import toolz


class HeadersFactory(object):
    def __call__(self, body: Dict):
        return functools.partial(
            Headers(body),
        )


class Headers(object):
    def __init__(self, body):
        self._body = body

    def __call__(self, builder):
        if not isinstance(builder, interfaces.Builder):
            builder = Builder(builder)

        for (key, val) in self._body.items():
            builder.add_header(key, val)

        return builder


headers = HeadersFactory().__call__


class ReturnsFactory(object):
    def get_in(self, keys: List = []):
        def func(_, raw):
            return toolz.get_in(keys, raw)
        return functools.partial(
            ReturnsFunc(func),
        )

    def __call__(self, func):
        return functools.partial(
            ReturnsFunc(func),
        )


class ReturnsFunc(object):
    def __init__(self, func):
        self._func = func

    def __call__(self, builder):
        if not isinstance(builder, interfaces.Builder):
            builder = Builder(builder)
        builder.add_return(self._func)
        return builder


returns = ReturnsFactory()


class RetryFactory(object):
    def __call__(self, **kwargs):
        return functools.partial(
            Retry(kwargs),
        )


class Retry(object):
    def __init__(self, kwargs):
        self._kwargs = kwargs

    def __call__(self, builder):
        if not isinstance(builder, interfaces.Builder):
            builder = Builder(builder)
        builder.add_retry(self._kwargs)
        return builder


retry = RetryFactory()


class TimeoutFactory(object):
    def __call__(self, timeout):
        return functools.partial(
            Timeout(timeout),
        )


class Timeout(object):
    def __init__(self, timeout):
        self._timeout = timeout

    def __call__(self, builder):
        if not isinstance(builder, interfaces.Builder):
            builder = Builder(builder)
        builder.set_timeout(self._timeout)
        return builder


timeout = TimeoutFactory()
