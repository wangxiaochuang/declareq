'''uplink'''
from drequests.arguments import BodyKw, HeaderAuthToken, Path, Query, UrlPrefix, QueryAuthToken
from drequests.builder import Consumer
from drequests.commands import post
from drequests.annotations import headers, returns


def print_status(response):
    '''print status'''
    print(f'Google response status:{response.status_code}')
    return response


def handle_error(exc_type, _exc_val, _exc_tb):
    '''handle error'''
    print(
        f'Error encountered. Exception will be raised. Exception Type:{exc_type}')


class Result():
    def __init__(self, raw):
        self.raw = raw
    
    def __repr__(self):
        return f'Result:{self.raw}'

class Google(Consumer):
    @headers({"User-Agent": "test-Sample-App"})
    @returns.get_in(["data"])
    def __init__(self, _: UrlPrefix, access_token: HeaderAuthToken("X-Api-Token", call="get")):
        pass

    '''google'''
    @post("/ws/{id}")
    @headers({"User-Agent": "drequests-Sample-App"})
    @returns.get_in(["name"])
    def homepage(self, _id: Path, _: Query("kw"), **_info: BodyKw) -> Result:
        '''homepage'''
        print('google home page')


class MyToken():
    def get(self):
        return "xxxxx"


google = Google("http://127.0.0.1:5000", MyToken())
res = google.homepage(123, "jack", a=1, b=2)
print(res)
