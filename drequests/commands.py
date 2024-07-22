import functools
from typing import Any
import requests
import uritemplate

from drequests import utils, interfaces


class Request():
    def __init__(self, method, url, headers, query, body):
        self.method = method
        self.url = url
        self.query = query
        self.session = requests.Session()
        self.body = body
        self.headers = headers

    def execute(self, consumer):
        query = {k: v(consumer) if callable(
            v) else v for k, v in self.query.items()}
        headers = {k: v(consumer) if callable(
            v) else v for k, v in self.headers.items()}
        return self.session.request(self.method, self.url, params=query, headers=headers, json=self.body, proxies={"http": None, "https": None})


class Empty():
    def __init__(self, default=None):
        self._default = default

    def default(self):
        return self._default


empty_method = Empty()
empty_path = Empty()
empty_spec = Empty()
empty_url_prefix = Empty()
empty_url = Empty()


def is_empty(obj):
    return isinstance(obj, Empty)


class RequestDefinitionBuilder(interfaces.RequestDefinitionBuilder):
    def __init__(self, func):
        self._spec = utils.get_arg_spec(func)
        self._func = func
        self._method = empty_method
        self._url_prefix = empty_url_prefix
        self._path = empty_path
        self._url = empty_url
        self._path_vars = {}
        self._body = {}
        self._query = {}
        self._query_auth = {}
        self._headers = {}
        self._headers_auth = {}
        self._params = {}

    @property
    def spec(self):
        return self._spec

    @property
    def method(self):
        return self._method

    @method.setter
    def method(self, method):
        if not method:
            raise ValueError("method cannot be empty")
        if self._method is not empty_method:
            raise ValueError("Method already set")
        self._method = method

    @property
    def url_prefix(self):
        return self._url_prefix

    @url_prefix.setter
    def url_prefix(self, prefix):
        if not prefix:
            raise ValueError("base url cannot be empty")
        if self._url_prefix is not empty_url_prefix:
            raise ValueError("base url already set")
        self._url_prefix = prefix

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, path):
        if not path:
            raise ValueError("path cannot be empty")
        if self._path is not empty_path:
            raise ValueError("path already set")
        self._path = uritemplate.URITemplate(path)

    def add_path_var(self, key, val):
        self._path_vars[key] = val

    def add_body(self, key, val):
        self._body[key] = val

    def add_query(self, key, val):
        self._query[key] = val

    def add_query_auth(self, key, val):
        self._query_auth[key] = val

    def add_header(self, key, val):
        self._headers[key] = val

    def add_header_auth(self, key, val):
        self._headers_auth[key] = val

    @property
    def url(self):
        return self.url_prefix + self._path.expand(self._path_vars)

    @property
    def body(self):
        return self._body

    @property
    def headers(self):
        return self._headers

    def _merge_url(self, global_builder):
        if not is_empty(self._url):
            return self._url
        if not is_empty(global_builder._url):
            return global_builder._url

        if not is_empty(self._url_prefix):
            prefix = self._url_prefix
        elif not is_empty(global_builder._url_prefix):
            prefix = global_builder._url_prefix
        else:
            raise Exception("need url")

        if not is_empty(self._path):
            path = self._path
        elif not is_empty(global_builder._path):
            path = global_builder._path
        else:
            path = uritemplate.URITemplate("/")
        return prefix + path.expand({**self._path_vars, **global_builder._path_vars})

    def _merge_headers(self, global_builder):
        headers_auth = {**global_builder._headers_auth, **self._headers_auth}
        return {**global_builder._headers, **self._headers, **headers_auth}

    def _merge_query(self, global_builder):
        query_auth = {**global_builder._query_auth, **self._query_auth}
        return {**global_builder._query, **self._query, **query_auth}

    def build(self, global_builder) -> Request:
        url = self._merge_url(global_builder)
        headers = self._merge_headers(global_builder)
        query = self._merge_query(global_builder)
        return Request(self.method, url, headers, query, self.body)

    def __repr__(self):
        return f"builder({self.method})"


class HttpMethodFactory(object):
    def __init__(self, method):
        self._method = method

    def __call__(self, path=None) -> Any:
        return functools.partial(
            HttpMethod(self._method, path),
        )


class HttpMethod(object):
    def __init__(self, method, path=None):
        self._method = method
        self._path = path

    def __call__(self, builder):
        if not isinstance(builder, interfaces.RequestDefinitionBuilder):
            builder = RequestDefinitionBuilder(builder)

        builder.path = self._path
        builder.method = self._method

        return builder


get = HttpMethodFactory("GET").__call__
post = HttpMethodFactory("POST").__call__
