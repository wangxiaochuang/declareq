import pytest
from declareq import Consumer
from declareq import Path, UrlPrefix, Session, QueryAuthToken
from declareq import returns, get, ExtractFail, proxies


class MockResponse():
    def __init__(self):
        self.headers = {
            "content-type": "application/json"
        }

    def json(self):
        return {
            "code": 0,
            "data": {"name": "declareq", "id": 0}
        }


class MockSession():
    def __init__(self):
        self.method = None
        self.url = None
        self.kwargs = {}

    def request(self, method, url, **kwargs):
        self.method = method
        self.url = url
        self.kwargs = kwargs
        return MockResponse()


class Repo():
    def __init__(self, raw):
        self.raw = raw

    @property
    def name(self):
        return self.raw["name"]


def test_base():
    session = MockSession()

    class MockService(Consumer):
        '''mock service'''

        @proxies({"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"})
        def __init__(self, _: UrlPrefix, _c: Session, access_token: QueryAuthToken):
            pass

        @returns.get_in(["data"])
        @get("/users/{user}/repos")
        def list_repos(self, user: Path) -> Repo:
            """List all public repositories for a specific user."""

    svc = MockService("mock://mock.org", session, "TOKEN_12345")
    repo = svc.list_repos("declareq")
    assert session.method == "GET"
    assert session.url == "mock://mock.org/users/declareq/repos"
    assert session.kwargs["params"]["access_token"] == "TOKEN_12345"
    assert session.kwargs["proxies"]["http"] == "http://127.0.0.1:8080"
    assert repo.name == "declareq"


def test_returns_extract_exception():
    session = MockSession()

    class MockService(Consumer):
        '''mock service'''

        def __init__(self, _: UrlPrefix, _c: Session, access_token: QueryAuthToken):
            pass

        @returns.get_in("none-exists")
        @get("/users/{user}/repos")
        def list_repos(self, user: Path) -> Repo:
            """List all public repositories for a specific user."""

    svc = MockService("mock://mock.org", session, "TOKEN_12345")
    with pytest.raises(ExtractFail, match=r".*none-exists.*"):
        svc.list_repos("declareq")
