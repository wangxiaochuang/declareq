import requests
from retrying import retry

from declareq.exceptions import NeedRetry, RequestFail


def retry_if_need(e):
    return isinstance(e, NeedRetry)


def _is_application_json(resp):
    return "application/json" in resp.headers.get("content-type", "")


class Request():
    def __init__(self, client, method, url, headers, query, body, ret_funcs, retry_kwargs, timeout, proxies):
        self.method = method
        self.url = url
        self.query = query
        self.session = client or requests.Session()
        self.body = body
        self.headers = headers
        self.ret_funcs = ret_funcs
        self.retry_kwargs = retry_kwargs
        self.timeout = timeout
        self.proxies = proxies or {"http": None, "https": None}

    def execute(self, consumer):
        ''' execute network request '''
        def run():
            query = {k: v(consumer) if callable(
                v) else v for k, v in self.query.items()}
            headers = {k: v(consumer) if callable(
                v) else v for k, v in self.headers.items()}
            try:
                resp = self.session.request(self.method,
                                            self.url,
                                            params=query,
                                            headers=headers,
                                            json=self.body,
                                            proxies=self.proxies,
                                            timeout=self.timeout / 1000)
            except requests.exceptions.Timeout as e:
                raise NeedRetry("timeout") from e
            except Exception as e:
                raise RequestFail() from e
            res = resp.json() if _is_application_json(resp) else resp.text
            for func in self.ret_funcs:
                res = func(consumer, res)
                if res is None:
                    break
            return res

        run = retry(**self.retry_kwargs)(run)

        return run()
