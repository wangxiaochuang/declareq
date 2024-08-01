import functools
from typing import Dict, List

from declareq import interfaces
from declareq.commands import Builder
import toolz

from declareq.exceptions import ExtractFail


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
    def get_in(self, keys: str | List = [], default=None, raise_exception=True, ex=None):
        if isinstance(keys, str):
            keys = [keys]
        assert len(keys) > 0

        def func(_, raw):
            try:
                return toolz.get_in(keys, raw, no_default=True)
            except KeyError as e:
                if raise_exception:
                    if ex is not None:
                        raise ex(raw) from e
                    raise ExtractFail(f"extract {keys} fail") from e
                return default
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
    def __call__(self, _timeout):
        return functools.partial(
            Timeout(_timeout),
        )


class Timeout(object):
    def __init__(self, _timeout):
        self._timeout = _timeout

    def __call__(self, builder):
        if not isinstance(builder, interfaces.Builder):
            builder = Builder(builder)
        builder.set_timeout(self._timeout)
        return builder


timeout = TimeoutFactory()


class ProxiesFactory(object):
    def __call__(self, _proxies):
        return functools.partial(
            Proxies(_proxies),
        )


class Proxies(object):
    def __init__(self, _proxies):
        assert isinstance(_proxies, dict)
        self._proxies = _proxies

    def __call__(self, builder):
        if not isinstance(builder, interfaces.Builder):
            builder = Builder(builder)
        builder.proxies = self._proxies
        return builder


proxies = ProxiesFactory()


class HttpMethodFactory(object):
    def __init__(self, method):
        self._method = method

    def __call__(self, path=None):
        return functools.partial(
            HttpMethod(self._method, path),
        )


class HttpMethod(object):
    def __init__(self, method, path=None):
        self._method = method
        self._path = path

    def __call__(self, builder):
        if not isinstance(builder, interfaces.Builder):
            builder = Builder(builder)

        builder.path = self._path
        builder.method = self._method

        return builder


get = HttpMethodFactory("GET").__call__
post = HttpMethodFactory("POST").__call__
