import multiprocessing
from pipeproxy.lib.proxy_messages.reply_message import *
from pipeproxy.lib.proxy_messages.request_message import *
from .proxy_listener_message_handler import ProxyListenerMessageHandler
from .proxy_listener_message_receiver import ProxyListenerMessageReceiver
from .proxy_listener_message_sender import ProxyListenerMessageSender


class ProxyListener:
    def __init__(self, pipe_connection, obj):
        # type: (multiprocessing.Connection, object) -> None
        self.messageReceiver = ProxyListenerMessageReceiver(pipe_connection)
        self.messageSender = ProxyListenerMessageSender(pipe_connection)
        self.functionHandler = ProxyListenerMessageHandler(obj)

    def listen(self):
        """Receive message request, handle and reply. NullRequestMessage means no message was received"""
        message = self.messageReceiver.receive()
        assert isinstance(message, RequestMessage)
        if not isinstance(message, NullRequestMessage):
            reply = self.functionHandler.handle_received_message(message)
            assert isinstance(reply, ReplyMessage)
            self.messageSender.send(reply)

    def send(self, fn, *args, **kwargs):
        self.messageSender.send(ReplyMessage({
            'fn': fn,
            'args': args,
            'kwargs': kwargs
        }))
