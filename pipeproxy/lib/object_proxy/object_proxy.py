from pipeproxy.lib.proxy_messages.request_message import RequestMessage
from pipeproxy.lib.proxy_messages.reply_message import ReplyMessage
from .proxy_messenger.proxy_message_transmitter import ProxyMessageTransmitter


class ObjectProxy:

    def __init__(self, proxy_message_transmitter):
        # type: (ProxyMessageTransmitter) -> None
        """
        Has all the methods like the object that it is a proxy of. This must be ensured by the proxy maker.
        Difference is that methods that are called don't get executed, rather sent using the message sender.
        It is then up to the proxy listener to receive these methods (in a form of request message) and
        execute them as well as to reply with whatever a method returns (in a form of a reply message).
        :param proxy_message_transmitter: Object that takes care of the communication part.
        """
        self.proxyMessageSender = proxy_message_transmitter

    def send_message(self, function_name, args):
        """Creates a Request and sends it. Always expects a reply"""
        request = RequestMessage(function_name, args)
        reply = self.proxyMessageSender.send_message(request)
        assert isinstance(reply, ReplyMessage)
        return reply.get_content()

    @classmethod
    def add_method(cls, method, name):
        assert callable(method)
        setattr(cls, name, method)
