from operator import methodcaller
from declareq import interfaces
from declareq.commands import Builder


class Header(interfaces.Argument):
    def build(self, consumer, builder: Builder, arg_key, arg_val):
        builder.add_header(self.get_key(arg_key), arg_val)


class HeaderMap(interfaces.Argument):
    def build(self, consumer, builder: Builder, arg_key, arg_val):
        for (k, v) in arg_val.items():
            builder.add_header(k, v)


HeaderKw = HeaderMap


class Path(interfaces.Argument):
    def build(self, consumer, builder: Builder, arg_key, arg_val):
        builder.add_path_var(self.get_key(arg_key), arg_val)


class PathMap(interfaces.Argument):
    def build(self, consumer, builder: Builder, arg_key, arg_val):
        for (k, v) in arg_val.items():
            builder.add_path_var(k, v)


PathKw = PathMap


class Body(interfaces.Argument):
    def build(self, consumer, builder: Builder, arg_key, arg_val):
        builder.add_body(self.get_key(arg_key), arg_val)


class BodyMap(interfaces.Argument):
    def build(self, consumer, builder: Builder, _, arg_val):
        for (k, v) in arg_val.items():
            builder.add_body(k, v)


class Query(interfaces.Argument):
    def build(self, consumer, builder: Builder, arg_key, arg_val):
        builder.add_query(self.get_key(arg_key), arg_val)


class QueryMap(interfaces.Argument):
    def build(self, consumer, builder: Builder, _, arg_val):
        for (k, v) in arg_val.items():
            builder.add_query(k, v)


QueryKw = QueryMap


class UrlPrefix(interfaces.Argument):
    def build(self, consumer, builder: Builder, _, arg_val):
        builder.url_prefix = arg_val


class QueryAuthToken(interfaces.Argument):
    '''set query auth token'''

    def build(self, consumer, builder: Builder, arg_key, arg_val):
        proxy_val = arg_val
        if call := self.kwargs.get("call"):
            def _arg_val(_):
                return methodcaller(call)(arg_val)
            proxy_val = _arg_val
        builder.add_query_auth(self.get_key(arg_key), proxy_val)


class HeaderAuthToken(interfaces.Argument):
    '''set query auth token'''

    def build(self, consumer, builder: Builder, arg_key, arg_val):
        if call := self.kwargs.get("call"):
            def _arg_val(_):
                return methodcaller(call)(arg_val)
        builder.add_header_auth(self.get_key(arg_key), _arg_val)


class Session(interfaces.Argument):
    def build(self, consumer, builder: Builder, _, arg_val):
        builder.client = arg_val
