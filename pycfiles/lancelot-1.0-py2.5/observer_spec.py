# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/lancelot/examples/observer_spec.py
# Compiled at: 2009-02-16 14:47:09
"""
Some example Specs to illustrate usage scenarios with collaborations
"""
import lancelot

class Observer(object):
    """ Simple observer class """

    def notify(self, observable):
        """ Receive a notification from something observable """
        pass


class Observable(object):
    """ Simple observable class that sends notifications to its observers """

    def __init__(self):
        """ No observers at instantiation """
        self.observers = []

    def add_observer(self, observer):
        """ Add an observer """
        self.observers.append(observer)

    def send_notification(self):
        """ Send notifications to all observers """
        for observer in self.observers:
            observer.notify(self)


@lancelot.verifiable
def observable_observer_behaviour():
    """ Illustrate how Spec.should_collaborate_with() and MockSpec interact.
    Note how a new MockSpec is required for each should...() specification """
    observer = lancelot.MockSpec()
    observable = Observable()
    spec = lancelot.Spec(observable)
    spec.send_notification().should_collaborate_with()
    observer = lancelot.MockSpec()
    observable = Observable()
    spec = lancelot.Spec(observable)
    spec.when(spec.add_observer(observer))
    spec.then(spec.send_notification())
    spec.should_collaborate_with(observer.notify(observable))
    observer = lancelot.MockSpec()
    observable = Observable()
    spec = lancelot.Spec(observable)
    spec.when(spec.add_observer(observer), spec.add_observer(observer))
    spec.then(spec.send_notification())
    spec.should_collaborate_with(observer.notify(observable).twice())


if __name__ == '__main__':
    lancelot.verify()