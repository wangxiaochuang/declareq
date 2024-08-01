import pytest
from declareq import Consumer
from declareq import Path, UrlPrefix, Session, QueryAuthToken
from declareq import returns, get, ExtractFail, proxies
from foxmock import Mock

class MyCustomError(Exception):
    pass

class Repo():
    def __init__(self, raw):
        self.raw = raw
    
    def name(self):
        return self.raw["name"]

def test_returns_extract_exception():
    resp = Mock()
    resp.call("json").ret({"data": {"name": "jack"}})
    resp.index("headers").ret({"content-type": "application/json"})

    session = Mock()
    session.call("request").ret(resp)


    class MockService(Consumer):
        '''mock service'''

        def __init__(self, _: UrlPrefix, _c: Session):
            pass

        @returns.get_in("none-exists", ex=MyCustomError)
        @get("/users/{user}/repos")
        def list_repos(self, user: Path) -> Repo:
            """List all public repositories for a specific user."""

    svc = MockService("mock://mock.org", session)
    with pytest.raises(MyCustomError, match=r"{'data': {'name': 'jack'}}"):
        svc.list_repos("declareq")

def test_returns_class():
    resp = Mock()
    resp.call("json").ret({"data": {"name": "jack"}})
    resp.index("headers").ret({"content-type": "application/json"})

    session = Mock()
    session.call("request").ret(resp)


    class MockService(Consumer):
        '''mock service'''

        def __init__(self, _: UrlPrefix, _c: Session):
            pass

        @returns.get_in("data", ex=MyCustomError)
        @get("/users/{user}/repos")
        def list_repos(self, user: Path) -> Repo:
            """List all public repositories for a specific user."""

    svc = MockService("mock://mock.org", session)
    repo = svc.list_repos("declareq")
    assert repo.name() == "jack"