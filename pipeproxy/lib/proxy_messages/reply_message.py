class ReplyMessage:

    def __init__(self, content):
        self.content = content

    def has_content(self):
        if self.content is not None:
            return True
        else:
            return False

    def get_content(self):
        return self.content

    def __str__(self):
        return "content: " + str(self.content)

    def __eq__(self, other):
        # type: (ReplyMessage) -> bool
        if self.content == other.content:
            return True
        else:
            return False


class NullReplyMessage(ReplyMessage):

    def __init__(self):
        ReplyMessage.__init__(self, None)


class ErrorReplyMessage(ReplyMessage):

    def __init__(self, error_message):
        ReplyMessage.__init__(self, error_message)
