import pytest
from declareq import Consumer
from declareq import Path, UrlPrefix, Session, QueryAuthToken
from declareq import returns, get, proxies
from foxmock import Mock


def test_base():
    resp = Mock()
    resp.call("json").ret({"data": {"name": "declareq"}})
    resp.index("headers").ret({"content-type": "application/json"})
    session = Mock()
    session.call("request").ret(resp)

    class MockService(Consumer):
        '''mock service'''

        @proxies({"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"})
        def __init__(self, _: UrlPrefix, _c: Session, access_token: QueryAuthToken):
            pass

        @returns.get_in(["data"])
        @get("/users/{user}/repos")
        def list_repos(self, user: Path):
            """List all public repositories for a specific user."""

    svc = MockService("mock://mock.org", session, "TOKEN_12345")
    repo = svc.list_repos("declareq")
    req = session.request.history[0]
    method = req.args[0]
    url = req.args[1]
    query = req.kwargs["params"]
    _proxies = req.kwargs["proxies"]
    assert method == "GET"
    assert url == "mock://mock.org/users/declareq/repos"
    assert query["access_token"] == "TOKEN_12345"
    assert _proxies["http"] == "http://127.0.0.1:8080"
    assert repo['name'] == "declareq"


def test_auth_token_method_call_shoud_work():
    resp = Mock()
    resp.call("json").ret({"data": {"name": "declareq"}})
    resp.index("headers").ret({"content-type": "application/json"})
    session = Mock()
    session.call("request").ret(resp)

    token = Mock()
    token.call("get").ret( "TOKEN_12345")
        
    class MockService(Consumer):
        '''mock service'''

        def __init__(self, _: UrlPrefix, _c: Session, access_token: QueryAuthToken(call="get")):
            pass

        @get("/users/{user}/repos")
        def list_repos(self, user: Path):
            """List all public repositories for a specific user."""

    svc = MockService("mock://mock.org", session, token)
    svc.list_repos("declareq")
    assert session.request.history[0].kwargs["params"]['access_token'] == "TOKEN_12345"
