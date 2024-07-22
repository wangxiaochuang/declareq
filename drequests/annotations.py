import functools
from typing import Dict

from drequests import interfaces
from drequests.commands import RequestDefinitionBuilder


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
