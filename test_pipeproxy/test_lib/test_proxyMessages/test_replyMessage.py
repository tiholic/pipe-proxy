import unittest
from pipeproxy.lib.proxyMessages.replyMessage import *


class ReplyMessageTest(unittest.TestCase):
    def test_hasContent(self):
        reply = ReplyMessage(None)
        assert reply.has_content() is False

        reply = ReplyMessage(1)
        assert reply.has_content() is True

    def test_getContent(self):
        reply = ReplyMessage(1)
        assert reply.get_content() == 1


class NullReplyMessageTest(unittest.TestCase):
    def test_hasContent(self):
        reply = NullReplyMessage()
        assert reply.has_content() is False

    def test_getContent(self):
        reply = NullReplyMessage()
        assert reply.get_content() is None






