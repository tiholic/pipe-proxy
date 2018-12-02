import multiprocessing

from pipeproxy.lib.proxy_messages.request_message import RequestMessage, NullRequestMessage


class ProxyListenerMessageReceiver:

    def __init__(self, pipe_connection):
        # type: (multiprocessing.Connection) -> None
        self.conn = pipe_connection

    def receive(self):
        # type: () -> RequestMessage
        if self.conn.poll(0.2):
            message = self.conn.recv()
            assert isinstance(message, RequestMessage)
            return message
        return NullRequestMessage()




