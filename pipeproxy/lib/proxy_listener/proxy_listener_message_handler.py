import inspect

from pipeproxy.lib.proxy_messages.reply_message import *
from pipeproxy.lib.proxy_messages.request_message import *


class WrongArgumentsError(Exception):
    pass


class MissingFunctionError(Exception):
    pass


class ProxyListenerMessageHandler:

    def __init__(self, obj):
        self.obj = obj

    def handle_received_message(self, message):
        # type: (RequestMessage) -> ReplyMessage
        """
        Execute the method that corresponds with the function in the Request message.
        :return: Reply message containing return argument from the executed method.
        """
        assert isinstance(message, RequestMessage)
        fn = message.get_function()
        args = message.get_args()
        # execute method and get return argument
        try:
            reply = getattr(self.obj, fn)(*args)
            return ReplyMessage(reply)
        except AttributeError:
            raise MissingFunctionError("No function " + str(fn) + " found in " + str(self.obj.__class__.__name__))
        except TypeError:
            function_specs = inspect.getargspec(getattr(self.obj, fn)).args
            raise WrongArgumentsError(
                "Wrong arguments " + str(args) + " for '" + str(fn) + "' in " + str(
                    self.obj.__class__.__name__) + " expected: " + str(function_specs)
            )
