import unittest

from pipeproxy.lib.proxy_messages.request_message import *


class ReplyMessageTest(unittest.TestCase):

    def test_getFunction(self):
        request = RequestMessage('someFunction', (1, 2))
        assert request.get_function() == 'someFunction'

    def test_getArgs(self):
        request = RequestMessage('someFunction', (1, 2))
        assert request.get_args() == [1, 2]


class NullReplyMessageTest(unittest.TestCase):

    def test_getFunction(self):
        request = NullRequestMessage()
        assert request.get_function() == ''

    def test_getArgs(self):
        request = NullRequestMessage()
        assert request.get_args() == ()
