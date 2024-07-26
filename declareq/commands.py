'''commands'''
import inspect
import uritemplate

from declareq import utils, interfaces
from declareq import request


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
empty_timeout = Empty()


def is_empty(obj):
    return isinstance(obj, Empty)


class Builder(interfaces.Builder):
    def __init__(self, func):
        self._spec = utils.get_arg_spec(func)
        self._func = func
        self._method = empty_method
        # init can be set
        self._url_prefix = empty_url_prefix
        self._path = empty_path
        # init can be set
        self._url = empty_url
        # init can be set
        self._path_vars = {}
        # init can be set
        self._body = {}
        # init can be set
        self._query = {}
        # init can be set
        self._query_auth = {}
        # init can be set
        self._headers = {}
        # init can be set
        self._headers_auth = {}
        # init can be set
        self._returns = []
        # init can be set
        self._retry = {
            "retry_on_exception": request.retry_if_need,
            "stop_max_attempt_number": 2,
            "wait_random_min": 1000,
            "wait_random_max": 3000}
        # init can be set
        self._timeout = empty_timeout
        self._client = None
        self._proxies = {}

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
    def client(self):
        return self._client

    @client.setter
    def client(self, client):
        if not client:
            raise ValueError("client cannot be empty")
        if self._client is not None:
            raise ValueError("client already set")
        self._client = client

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

    @property
    def proxies(self):
        return self._proxies

    @proxies.setter
    def proxies(self, proxies):
        if not proxies:
            raise ValueError("proxies cannot be empty")
        if self._proxies:
            raise ValueError("proxies already set")
        self._proxies = proxies

    def set_timeout(self, timeout):
        if not timeout:
            raise ValueError("timeout cannot be empty")
        if self._timeout is not empty_timeout:
            raise ValueError("timeout already set")
        self._timeout = timeout

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

    def add_return(self, func):
        self._returns.append(func)

    def add_retry(self, kwargs):
        self._retry.update(kwargs)

    @property
    def url(self):
        return self.url_prefix + self._path.expand(self._path_vars)

    @property
    def body(self):
        return self._body

    @property
    def headers(self):
        return self._headers

    def _merge_url(self, init_builder):
        if not is_empty(self._url):
            return self._url
        if not is_empty(init_builder._url):
            return init_builder._url

        if not is_empty(self._url_prefix):
            prefix = self._url_prefix
        elif not is_empty(init_builder._url_prefix):
            prefix = init_builder._url_prefix
        else:
            raise Exception("need url")

        if not is_empty(self._path):
            path = self._path
        elif not is_empty(init_builder._path):
            path = init_builder._path
        else:
            path = uritemplate.URITemplate("/")
        return prefix + path.expand({**self._path_vars, **init_builder._path_vars})

    def _merge_headers(self, init_builder):
        headers_auth = {**init_builder._headers_auth, **self._headers_auth}
        return {**init_builder._headers, **self._headers, **headers_auth}

    def _merge_query(self, init_builder):
        query_auth = {**init_builder._query_auth, **self._query_auth}
        return {**init_builder._query, **self._query, **query_auth}

    def _merge_return(self, init_builder):
        def ret_func(_, raw):
            return raw
        # 返回值可调用说明是类或者函数
        if callable(self.spec.return_annotation):
            def _ret_func(consumer, raw):
                # 如果是类，就接受返回数据
                if inspect.isclass(self.spec.return_annotation):
                    return self.spec.return_annotation(raw)
                # 如果是函数，接受consumer和返回数据
                return self.spec.return_annotation(consumer, raw)
            ret_func = _ret_func

        return [*init_builder._returns, *self._returns, ret_func]

    def _merge_retry(self, init_builder):
        return {**init_builder._retry, **self._retry}

    def _merge_timeout(self, init_builder):
        if not is_empty(self._timeout):
            return self._timeout
        if not is_empty(init_builder._timeout):
            return init_builder._timeout
        return 5000

    def _merge_client(self, init_builder):
        return self._client or init_builder._client

    def _merge_proxies(self, init_builder):
        '''子类的优先'''
        return {**init_builder._proxies, **self._proxies}

    def build(self, init_builder) -> request.Request:
        '''实际执行请求的时候会 merge init 的相关配置'''
        url = self._merge_url(init_builder)
        headers = self._merge_headers(init_builder)
        query = self._merge_query(init_builder)
        ret_funcs = self._merge_return(init_builder)
        retry_kwargs = self._merge_retry(init_builder)
        timeout = self._merge_timeout(init_builder)
        client = self._merge_client(init_builder)
        proxies = self._merge_proxies(init_builder)
        return request.Request(client, self.method, url, headers, query, self.body, ret_funcs, retry_kwargs, timeout, proxies)

    def merge_parent(self, builder) -> interfaces.Builder:
        '''类初始化的时候，__init__的 merge'''
        # 自己没有才是用父类存在的
        if is_empty(self._url_prefix) and (not is_empty(builder._url_prefix)):
            self._url_prefix = builder._url_prefix
        if is_empty(self._url) and (not is_empty(builder._url)):
            self._url = builder._url
        if is_empty(self._timeout) and (not is_empty(builder._timeout)):
            self._timeout = builder._timeout
        # 父类的优先
        self._returns = {*builder._returns, *self._returns}
        # 子类的优先
        self._path_vars = {**builder._path_vars, **self._path_vars}
        self._body = {**builder._body, **self._body}
        self._query = {**builder._query, **self._query}
        self._query_auth = {**builder._query_auth, **self._query_auth}
        self._headers = {**builder._headers, **self._headers}
        self._retry = {**builder._retry, **self._retry}
        self._client = self._client or builder._client
        self._proxies = {**builder._proxies, **self._proxies}
        return self

    def __repr__(self):
        return f"builder({self.url_prefix})"
