import multiprocessing
import unittest
from pipeproxy.lib.object_proxy.object_proxy_maker import ObjectProxyMaker
from test_pipeproxy.testObject import TestObject, UnpickleableTestObject


class ObjectProxyMakerTest(unittest.TestCase):

    def test_make(self):
        parent_connection, child_connection = multiprocessing.Pipe()
        test_object = TestObject()
        test_object_proxy = ObjectProxyMaker(test_object, parent_connection).make()

        assert hasattr(test_object_proxy, 'getParameter')
        assert hasattr(test_object_proxy, 'setParameter')

        assert callable(getattr(test_object_proxy, 'getParameter'))
        assert callable(getattr(test_object_proxy, 'setParameter'))

    def test_makeUnpickleableObject(self):
        parent_connection, child_connection = multiprocessing.Pipe()
        test_object = UnpickleableTestObject()
        test_object_proxy = ObjectProxyMaker(test_object, parent_connection).make()
        assert 1
