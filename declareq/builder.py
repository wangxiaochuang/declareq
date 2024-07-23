import inspect
from declareq import interfaces, utils
from declareq.commands import Builder


def noops(*_arg, **_kwargs):
    '''no ops'''


class ConsumerMethod():
    ''' consumer method '''

    def __init__(self, builder: Builder):
        self.builder = builder

    def fill_args(self, consumer, *args, **kwargs):
        real_args = utils.get_call_args(
            self.builder._func, consumer, *args, **kwargs)
        for (arg, annotation) in self.builder.spec.annotations.items():
            if inspect.isclass(annotation) and issubclass(annotation, interfaces.Argument):
                annotation = annotation()
            if isinstance(annotation, interfaces.Argument):
                annotation.build(consumer, self.builder, arg, real_args[arg])

    def __call__(self, consumer, *args, **kwargs):
        # for real biz func
        self.fill_args(consumer, *args, **kwargs)
        request = self.builder.build(consumer._S_session)
        return request.execute(consumer)


class ConsumerMeta(type):
    @staticmethod
    def _wrap_init(cls_name, key, builder):
        if not isinstance(builder, interfaces.Builder):
            builder = Builder(builder)

        def wrap(consumer, *args, **kwargs):
            ConsumerMethod(builder).fill_args(consumer, *args, **kwargs)
            builder._func(consumer, *args, **kwargs)
            cls = type(consumer).__bases__[0]
            # 合并父类初始化方法的各个设置
            if session := getattr(cls, "_S_session", None):
                builder.merge_parent(session)

        return wrap, builder

    @staticmethod
    def _wrap_if_definition(cls_name, key, value):
        wrapped_value = value
        if isinstance(value, interfaces.Builder):
            builder = value

            def wrap(consumer, *args, **kwargs):
                return ConsumerMethod(builder)(consumer, *args, **kwargs)
            wrapped_value = wrap
        return wrapped_value

    def __new__(cls, name, bases, namespace):
        session = None
        for key, value in namespace.items():
            if key == "__init__":
                namespace["__init__"], session = cls._wrap_init(
                    name, key, value)
                continue
            namespace[key] = cls._wrap_if_definition(name, key, value)
        # 如果有初始化方法，就会有类属性session，就需要合并其父类的类属性session
        if session:
            if len(bases) > 0 and (parent := bases[0]) and (builder := getattr(parent, "_S_session", None)):
                session.merge_parent(builder)
            namespace["_S_session"] = session
        obj = super(ConsumerMeta, cls).__new__(cls, name, bases, namespace)
        return obj


_Consumer = ConsumerMeta("_Consumer", (), {})


class Consumer(interfaces.Consumer, _Consumer):
    '''consumer'''
