from multiprocessing import Pipe

from .lib.proxy_listener.proxy_listener import ProxyListener

from .lib.object_proxy.object_proxy_maker import ObjectProxyMaker


def create_proxy(obj):
    """ Create a multiprocessing Pipe connection ends. Create Proxy and ProxyListener connecting threw the Pipe"""
    parent_connection, child_connection = Pipe()

    object_proxy = ObjectProxyMaker(obj, child_connection).make()
    proxy_listener = ProxyListener(parent_connection, obj)

    return object_proxy, proxy_listener
