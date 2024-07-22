'''uplink'''
from drequests.arguments import BodyKw, Path, Query, UrlPrefix, QueryAuthToken
from drequests.builder import Consumer
from drequests.commands import post
from drequests.annotations import headers


def print_status(response):
    '''print status'''
    print(f'Google response status:{response.status_code}')
    return response


def handle_error(exc_type, _exc_val, _exc_tb):
    '''handle error'''
    print(
        f'Error encountered. Exception will be raised. Exception Type:{exc_type}')


class Google(Consumer):
    @headers({"User-Agent": "test-Sample-App"})
    def __init__(self, _: UrlPrefix, access_token: QueryAuthToken("token", call="get")):
        pass

    '''google'''
    @post(path="/ws/{id}")
    @headers({"User-Agent": "drequests-Sample-App"})
    def homepage(self, _id: Path, _: Query("kw"), **info: BodyKw) -> str:
        '''homepage'''
        print('google home page')


class MyToken():
    def get(self):
        return "xxxxx"


google = Google("http://127.0.0.1:5000", MyToken())
res = google.homepage(123, "jack", a=1, b=2)
print(res)
