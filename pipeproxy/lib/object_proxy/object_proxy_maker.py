from .object_proxy import ObjectProxy
from .proxy_messenger.proxy_message_transmitter import ProxyMessageTransmitter
import multiprocessing


def proxy_function_decorator(fn):
    assert callable(fn)

    def wrapper(*args):
        instance = args[0]
        args_without_instance = args[1:]
        assert isinstance(instance, ObjectProxy)
        return instance.send_message(fn.__name__, args_without_instance)

    return wrapper


class ObjectProxyMaker:

    def __init__(self, obj: object, pipe_connection: multiprocessing.Pipe):
        self.obj = obj
        self.conn = pipe_connection

    def make(self) -> ObjectProxy:
        # get all methods from obj
        for methodName in dir(self.obj):
            if not methodName.startswith('__') and callable(getattr(self.obj, methodName)):
                # decorate each method and add to ProxyObject
                actual_object_method = getattr(self.obj, methodName)
                decorated_method = proxy_function_decorator(actual_object_method)
                ObjectProxy.add_method(decorated_method, methodName)

        return ObjectProxy(ProxyMessageTransmitter(self.conn))
