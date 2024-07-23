'''init import *'''

from declareq.__about__ import __version__
from declareq.exceptions import (
    DeclareQException,
    ExtractFail,
    NeedRetry
)
from declareq.builder import Consumer
from declareq.annotations import (
    headers,
    returns,
    retry,
    timeout,
    proxies,
    get,
    post
)
from declareq.arguments import (
    Session,
    UrlPrefix,
    Path,
    PathMap,
    Query,
    QueryMap,
    QueryAuthToken,
    Header,
    HeaderMap,
    HeaderAuthToken,
    Body,
    BodyMap,
)

BodyKw = BodyMap
QueryKw = QueryMap
HeaderKw = HeaderMap

__all__ = [
    "__version__",
    "DeclareQException",
    "ExtractFail",
    "NeedRetry",
    "Consumer",
    "headers",
    "returns",
    "retry",
    "timeout",
    "proxies",
    "get",
    "post",
    "Session",
    "UrlPrefix",
    "Path",
    "PathMap",
    "Query",
    "QueryMap",
    "QueryAuthToken",
    "QueryKw",
    "Header",
    "HeaderMap",
    "HeaderAuthToken",
    "HeaderKw",
    "Body",
    "BodyMap",
    "BodyKw"
]
