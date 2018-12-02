import multiprocessing
from pipeproxy.lib.proxy_messages.reply_message import ReplyMessage


class ProxyListenerMessageSender:

    def __init__(self, pipe_connection):
        # type: (multiprocessing.Connection) -> None
        self.conn = pipe_connection

    def send(self, message):
        # type: (ReplyMessage) -> None
        self.conn.send(message)

