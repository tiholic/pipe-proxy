import multiprocessing
import time
import unittest
from pipeproxy.lib.proxyMessages.replyMessage import *
from pipeproxy.lib.proxyMessages.requestMessage import *
from pipeproxy.lib.objectProxy.objectProxyMaker import ProxyMessageSender


class ProxyMessageSenderTest(unittest.TestCase):
    def sendMessageToPipe(self, conn, message):
        # type: (multiprocessing.Connection, str) -> None
        time.sleep(0.1)
        reply = ReplyMessage(message)
        conn.send(reply)

    def receiveMessageFromPipe(self, conn):
        # type: (multiprocessing.Connection) -> RequestMessage
        request = conn.recv()
        return request

    def test_noResponseTimeout(self):
        parentConnection, childConnection = multiprocessing.Pipe()
        messageSender = ProxyMessageSender(parentConnection)

        assert messageSender.send_message(RequestMessage("request")) == NullReplyMessage()

    def test_sendingMessage(self):
        parentConnection, childConnection = multiprocessing.Pipe()
        messageSender = ProxyMessageSender(parentConnection)
        messageSender.send_message(RequestMessage("request"))

        assert self.receiveMessageFromPipe(childConnection) == RequestMessage("request")

    def method(self):
        pass

    def test_passingUnpickleableParameter(self):
        from threading import Timer
        parentConnection, childConnection = multiprocessing.Pipe()
        messageSender = ProxyMessageSender(parentConnection)
        unpickleableAttribute = Timer(1, self.method)

        with self.assertRaises(TypeError):
            messageSender.send_message(RequestMessage("request", args=unpickleableAttribute))

    def test_sendAndReceiveMessage(self):
        parentConnection, childConnection = multiprocessing.Pipe()
        messageSender = ProxyMessageSender(parentConnection)

        p = multiprocessing.Process(target=self.sendMessageToPipe, args=[childConnection, 'reply'])
        p.start()

        assert messageSender.send_message(RequestMessage("request")) == ReplyMessage("reply")



