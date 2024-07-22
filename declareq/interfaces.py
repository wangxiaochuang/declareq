class Consumer(object):
    pass


class Builder(object):
    @property
    def method(self):
        raise NotImplementedError

    @method.setter
    def method(self, method):
        raise NotImplementedError

    @property
    def path(self):
        raise NotImplementedError

    @path.setter
    def path(self, path):
        raise NotImplementedError

    def build(self, global_builder):
        raise NotImplementedError


class Argument(object):
    def __init__(self, name: str = None, **kwargs):
        self.name = name
        self.kwargs = kwargs

    def get_key(self, key: str) -> str:
        if self.name is not None:
            return self.name
        if key.startswith("_"):
            return key[1:]
        return key

    def build(self, consumer, builder: Builder, arg_key, arg_val):
        pass
