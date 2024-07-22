import collections
from inspect import signature
import inspect


Signature = collections.namedtuple(
    "Signature", "args annotations return_annotation"
)

Request = collections.namedtuple("Request", "method uri info return_type")


def get_arg_spec(f) -> Signature:
    sig = signature(f)
    parameters = sig.parameters
    args = []
    annotations = collections.OrderedDict()
    has_return_type = sig.return_annotation is not sig.empty
    return_type = sig.return_annotation if has_return_type else None
    for p in parameters:
        if parameters[p].annotation is not sig.empty:
            annotations[p] = parameters[p].annotation
        args.append(p)
    return Signature(args, annotations, return_type)


def get_call_args(f, *args, **kwargs):
    sig = signature(f)
    arguments = sig.bind(*args, **kwargs).arguments
    # apply defaults:
    new_arguments = []
    for name, param in sig.parameters.items():
        try:
            new_arguments.append((name, arguments[name]))
        except KeyError:
            if param.default is not param.empty:
                val = param.default
            elif param.kind is param.VAR_POSITIONAL:
                val = ()
            elif param.kind is param.VAR_KEYWORD:
                val = {}
            else:
                continue
            new_arguments.append((name, val))
    return collections.OrderedDict(new_arguments)
