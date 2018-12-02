class RequestMessage:
    def __init__(self, fn, args=()):
        # type: (str, tuple) -> None
        assert type(fn) is str
        self.function = fn
        self.args = args

    def get_function(self):
        # type: () -> str
        return self.function

    def get_args(self):
        # type: () -> tuple
        return self.args

    def __str__(self):
        return "function: " + self.function + ", args: " + str(self.args)

    def __eq__(self, other):
        # type: (RequestMessage) -> bool
        if self.function == other.function and self.args == other.args:
            return True
        else:
            return False


class NullRequestMessage(RequestMessage):
    def __init__(self):
        RequestMessage.__init__(self, "")

    def __str__(self):
        return "Null request message"
