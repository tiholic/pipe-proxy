import multiprocessing
import pickle
from ...proxy_messages.reply_message import *
from ...proxy_messages.request_message import *


class ProxyMessageTransmitter:

    def __init__(self, pipe_connection):
        # type: (multiprocessing.Connection) -> None
        self.conn = pipe_connection

    def send_message(self, request: RequestMessage) -> ReplyMessage:
        """Sends a request message threw the pipe and immediately expects a response with a 2s timeout"""
        ProxyMessageTransmitter._try_to_pickle(request)  # object being sent threw pipe connection must be pickle-able
        self.conn.send(request)
        # always receive reply
        if self.conn.poll(2):
            reply = self.conn.recv()
            assert isinstance(reply, ReplyMessage)
            return reply
        else:
            print("Warning: no reply received for request (" + str(request) + ")")
            return NullReplyMessage()

    @staticmethod
    def _try_to_pickle(obj):
        """Raises exception if not pickle-able"""
        pickle.dumps(obj)
