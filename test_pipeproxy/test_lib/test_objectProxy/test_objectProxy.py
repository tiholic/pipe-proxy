import multiprocessing
import time
import unittest
from pipeproxy.lib.proxy_messages.reply_message import *
from pipeproxy.lib.proxy_messages.request_message import RequestMessage
from pipeproxy.lib.object_proxy.object_proxy import ObjectProxy
from pipeproxy.lib.object_proxy.proxy_messenger.proxy_message_transmitter import ProxyMessageTransmitter


class ObjectProxyTest(unittest.TestCase):

    def send_message_to_pipe(self, conn, message):
        # type: (multiprocessing.Connection, str) -> None
        time.sleep(0.1)
        reply = ReplyMessage(message)
        conn.send(reply)

    def receiveMessageFromPipe(self, conn):
        # type: (multiprocessing.Connection) -> RequestMessage
        request = conn.recv()
        return request

    def test_noReplyTimeout(self):
        parent_connection, child_connection = multiprocessing.Pipe()
        object_proxy = ObjectProxy(ProxyMessageTransmitter(parent_connection))

        assert object_proxy.send_message('someFunction', ()) == NullReplyMessage().get_content()

    def test_sendMessageNoArgs(self):
        parent_connection, child_connection = multiprocessing.Pipe()
        object_proxy = ObjectProxy(ProxyMessageTransmitter(parent_connection))
        object_proxy.send_message('someFunction', ())

        assert self.receiveMessageFromPipe(child_connection) == RequestMessage("someFunction")

    def test_sendMessageWithArgs(self):
        parent_connection, child_connection = multiprocessing.Pipe()
        object_proxy = ObjectProxy(ProxyMessageTransmitter(parent_connection))
        object_proxy.send_message('someFunction', tuple([1, 2]))

        assert self.receiveMessageFromPipe(child_connection) == RequestMessage("someFunction", tuple([1, 2]))

    def test_sendAndReceiveMessage(self):
        parent_connection, child_connection = multiprocessing.Pipe()
        object_proxy = ObjectProxy(ProxyMessageTransmitter(parent_connection))
        p = multiprocessing.Process(target=self.send_message_to_pipe, args=[child_connection, 'reply'])
        p.start()

        assert object_proxy.send_message('someFunction', ()) == ReplyMessage("reply").get_content()

    def method_for_testing(self):
        print("I am a test method")

    def test_addMethod(self):
        parent_connection, child_connection = multiprocessing.Pipe()
        object_proxy = ObjectProxy(ProxyMessageTransmitter(parent_connection))
        object_proxy.add_method(self.method_for_testing, "testMe")
        object_proxy.testMe()
