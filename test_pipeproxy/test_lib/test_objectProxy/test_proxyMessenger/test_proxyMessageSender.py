import multiprocessing
import time
import unittest
from pipeproxy.lib.proxy_messages.reply_message import *
from pipeproxy.lib.proxy_messages.request_message import *
from pipeproxy.lib.object_proxy.object_proxyMaker import ProxyMessageTransmitter


class ProxyMessageTransmitterTest(unittest.TestCase):
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
        messageSender = ProxyMessageTransmitter(parentConnection)

        assert messageSender.send_message(RequestMessage("request")) == NullReplyMessage()

    def test_sendingMessage(self):
        parentConnection, childConnection = multiprocessing.Pipe()
        messageSender = ProxyMessageTransmitter(parentConnection)
        messageSender.send_message(RequestMessage("request"))

        assert self.receiveMessageFromPipe(childConnection) == RequestMessage("request")

    def method(self):
        pass

    def test_passingUnpickleableParameter(self):
        from threading import Timer
        parentConnection, childConnection = multiprocessing.Pipe()
        messageSender = ProxyMessageTransmitter(parentConnection)
        unpickleableAttribute = Timer(1, self.method)

        with self.assertRaises(TypeError):
            messageSender.send_message(RequestMessage("request", args=unpickleableAttribute))

    def test_sendAndReceiveMessage(self):
        parentConnection, childConnection = multiprocessing.Pipe()
        messageSender = ProxyMessageTransmitter(parentConnection)

        p = multiprocessing.Process(target=self.sendMessageToPipe, args=[childConnection, 'reply'])
        p.start()

        assert messageSender.send_message(RequestMessage("request")) == ReplyMessage("reply")
