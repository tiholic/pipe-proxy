from multiprocessing import Process
from multiprocessing.managers import BaseManager
import time
from .realThing import RealThing, RealThingUnpickleable
from .realThingProxy import RealThingProxy, RealThingUnpickleableProxy
import unittest


class MyManager(BaseManager):
    pass


def getAndSetValue(realThingProxy):
    # type: (RealThing) -> None

    if realThingProxy.get_value() == 5:
        print("Reseting value of realThing via Proxy")
        realThingProxy.set_value(0)


def someFunc():
    pass


class MultiprocessingProxyTest(unittest.TestCase):
    def test_regular(self):
        MyManager.register('RealThing', RealThing, RealThingProxy)
        manager = MyManager()
        manager.start()
        realThing = manager.RealThing()
        p1 = Process(target=getAndSetValue, args=[realThing])

        print("------regular-----------",
              "Calling function from main process: ")
        realThing.my_func()
        print("Setting value to '5' from main process")
        realThing.set_value(5)
        print("Getting value from main process: ",
              realThing.get_value(),
              "-----------------")

        p1.start()
        time.sleep(1)
        print("Value of realThing was changed in a different process: " + str(realThing.myValue))

        assert realThing.get_value() == 0

    def test_setUnpicklableAttribute(self):
        MyManager.register('RealThing', RealThingUnpickleable, RealThingUnpickleableProxy)
        manager = MyManager()
        manager.start()
        real_thing = manager.RealThing()

        from threading import Timer
        real_thing.timer = Timer(2, someFunc)

        assert 1


if __name__ == '__main__':
    unittest.main()
