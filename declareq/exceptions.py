class DeclareQException(Exception):
    pass


class RequestFail(DeclareQException):
    pass


class ExtractFail(DeclareQException):
    pass


class NeedRetry(DeclareQException):
    pass
