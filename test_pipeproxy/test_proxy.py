import time
import unittest
from multiprocessing import Process
from pipeproxy.lib.proxyListener.proxyListener import ProxyListener
from pipeproxy import create_proxy
from pipeproxy.lib.objectProxy.objectProxy import ObjectProxy
from testObject import TestObject, UnpickleableTestObject


def set_parameter_test(test_object_look_alike):
    # type: (TestObject) -> None
    test_object_look_alike.setParameter(5)


def get_parameter_test(test_object_look_alike):
    assert test_object_look_alike.getParameter() == 1


class ProxyTest(unittest.TestCase):

    def test_proxyCreate(self):
        test_object = TestObject()
        test_object_proxy, test_object_proxy_listener = create_proxy(test_object)

        assert isinstance(test_object_proxy, ObjectProxy)
        assert isinstance(test_object_proxy_listener, ProxyListener)

    def test_proxySetParameter(self):
        test_object = TestObject()
        test_object_proxy, test_object_proxy_listener = create_proxy(test_object)
        p = Process(target=set_parameter_test, args=(test_object_proxy,))
        p.start()
        time.sleep(1)
        test_object_proxy_listener.listen()
        assert test_object.getParameter() == 5

    def test_proxyGetParameter(self):
        test_object = TestObject()
        test_object_proxy, test_object_proxy_listener = create_proxy(test_object)
        p = Process(target=get_parameter_test, args=(test_object_proxy,))
        p.start()
        test_object.setParameter(1)
        while test_object_proxy_listener.listen():
            pass

    def test_unpickleableObjectMethodCall(self):
        test_object = UnpickleableTestObject()
        test_object_proxy, test_object_proxy_listener = create_proxy(test_object)
        p = Process(target=test_object_proxy.startTimer)
        p.start()
        test_object_proxy_listener.listen()

        assert 1

    def test_methodCallWithMissingArgs(self):
        test_object = TestObject()
        test_object_proxy, test_object_proxy_listener = create_proxy(test_object)
        test_object_proxy.setParameter()
        from pipeproxy.lib.proxyListener.proxyListenerMessageHandler import WrongArgumentsError
        with self.assertRaises(WrongArgumentsError):
            test_object_proxy_listener.listen()

    def test_methodCallWithWrongArgs(self):
        test_object = TestObject()
        test_object_proxy, test_object_proxy_listener = create_proxy(test_object)
        test_object_proxy.setParameter(1, 'a')
        from pipeproxy.lib.proxyListener.proxyListenerMessageHandler import WrongArgumentsError
        with self.assertRaises(WrongArgumentsError):
            test_object_proxy_listener.listen()


if __name__ == '__main__':
    unittest.main()
