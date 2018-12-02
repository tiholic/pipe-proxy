from threading import Timer


class RealThing(object):
    def __init__(self):
        self.myValue = 0

    def my_func(self):
        print("realThing func")

    def set_value(self, value):
        self.myValue = value

    def get_value(self):
        return self.myValue


class RealThingUnpickleable(object):

    def __init__(self):
        self.myValue = 0
        self.timer = None
