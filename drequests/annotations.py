import functools
from typing import Dict, List

from drequests import interfaces
from drequests.commands import RequestDefinitionBuilder
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
        if not isinstance(builder, interfaces.RequestDefinitionBuilder):
            builder = RequestDefinitionBuilder(builder)

        for (key, val) in self._body.items():
            builder.add_header(key, val)

        return builder


headers = HeadersFactory().__call__

class ReturnsFactory(object):
    def __call__(self, keys: List = []):
        return functools.partial(
            Returns(keys),
        )


class Returns(object):
    def __init__(self, keys):
        self._keys = keys

    def __call__(self, builder):
        if not isinstance(builder, interfaces.RequestDefinitionBuilder):
            builder = RequestDefinitionBuilder(builder)

        def f(_, raw):
            return toolz.get_in(self._keys, raw)
        builder.add_return(f)

        return builder
    
returns = ReturnsFactory().__call__
