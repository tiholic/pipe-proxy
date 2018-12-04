import uuid
import inspect
import forge


mystical_fns = {

}


class FnMock:

    def __init__(self, fn: callable):
        self.name = uuid.uuid4().hex
        mystical_fns[self.name] = fn
        print("=+++++++++++++++++++++++++++", mystical_fns)
        self.signature = inspect.signature(fn)

    def call(self, *args, **kwargs):
        # TODO
        print("?/??????////////////////Here...", args, kwargs, mystical_fns)
        mystical_fns[self.name](*args, **kwargs)
        pass


class RequestMessage:

    FUNCTION_INDICATOR = "__pipe_proxy__:__function__"

    def __init__(self, fn: str, args: tuple=()):
        assert type(fn) is str
        self.function = fn
        self.args = args

    def get_function(self) -> str:
        return self.function

    def get_args(self) -> tuple:
        return self.args

    def __str__(self):
        return "function: " + self.function + ", args: " + str(self.args)

    def __eq__(self, other):
        # type: (RequestMessage) -> bool
        if self.function == other.function and self.args == other.args:
            return True
        else:
            return False

    def __getstate__(self):
        state = self.__dict__.copy()
        state['args'] = list(state['args'])
        for index, arg in enumerate(state['args']):
            if callable(arg):
                state['args'][index] = FnMock(state['args'][index])
        return state

    def __setstate__(self, state):
        for idx, arg in enumerate(state['args']):
            if isinstance(arg, FnMock):
                fn_arg = arg
                sign = fn_arg.signature
                forged_args = []
                for _param in sign.parameters:
                    parameter: inspect.Parameter = sign.parameters[_param]
                    # forged_args.append(parameter)
                    _d = {
                        'kind': parameter.kind,
                        'name': parameter.name
                    }
                    if parameter.default != parameter.empty:
                        _d['default'] = parameter.default

                    forged_args.append(forge.FParameter(**_d))
                print("FA>>>", forged_args)
                state['args'][idx] = forge.sign(*forged_args)(lambda *args, **kwargs:
                                                              self.handle_fn_call(fn_arg, *args, **kwargs))
        self.__dict__.update(state)
        return

    def handle_fn_call(self, fn: FnMock, *args, **kwargs):
        print('fn_called, now transmit to child process...=============>', fn, args, kwargs)

        fn.call(*args, **kwargs)


class NullRequestMessage(RequestMessage):
    def __init__(self):
        RequestMessage.__init__(self, "")

    def __str__(self):
        return "Null request message"
