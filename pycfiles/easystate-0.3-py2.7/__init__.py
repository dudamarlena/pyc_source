# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/easystate/__init__.py
# Compiled at: 2013-03-24 16:15:35
"""
Created on Mar 18, 2013

@author: vahid
"""
import abc
__version__ = '0.3'
__all__ = ['StateMachine', 'State', 'Event', '__version__']

class Context(object):
    pass


class StateMachine(object):

    def __init__(self, initialState=None, context=None):
        self.context = context if context else Context()
        self.state = None
        self.initialState = initialState
        self.states = {}
        return

    def appendStates(self, *states):
        for state in states:
            self.appendState(state)

    def appendState(self, state):
        if not isinstance(state, State):
            raise AssertionError('Invalid state object')
            self.initialState = len(self.states) or state.name
        state.register(self)
        self.states[state.name] = state

    def start(self, initialState=None):
        if initialState:
            self.initialState = initialState
        assert len(self.states), 'At least one state must be added to machine.'
        assert self.initialState != None, 'You must specify initialState'

        def _transition(state):
            self.state = self.states[state]
            self.state.doJob()
            if hasattr(self.state, 'nextState'):
                return self.state.nextState

        _nextState = self.initialState
        while True:
            assert isinstance(_nextState, basestring)
            _nextState = _transition(_nextState)
            if not _nextState:
                break

        return


class Event(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name


class State(object):
    __metaclass__ = abc.ABCMeta
    machine = None

    def __init__(self):
        self.events = []

    def register(self, machine):
        self.machine = machine

    def raiseEvent(self, e):
        if isinstance(e, basestring):
            e = Event(e)
        if hasattr(self, 'on_%s' % e.name):
            getattr(self, 'on_%s' % e.name)(e)

    def transition(self, state):
        if hasattr(self, 'nextState'):
            raise Exception('Transition has been already applied')
        self.nextState = state

    def doJob(self):
        if hasattr(self, 'nextState'):
            del self.nextState
        self.raiseEvent('start')
        self.eval()
        self.raiseEvent('finish')

    @property
    def context(self):
        return self.machine.context

    @abc.abstractmethod
    def eval(self):
        raise NotImplementedError()

    @property
    def name(self):
        return self.__class__.__name__


if __name__ == '__main__':
    import time
    SPEED = 0.01

    class Starting(State):

        def eval(self):
            print 'Starting'
            time.sleep(SPEED)

        def on_start(self, e):
            print 'Hello'

        def on_finish(self, e):
            self.transition('Listening')


    class Listening(State):

        def eval(self):
            print 'Listening'
            print self.context.i
            self.context.i += 1
            time.sleep(SPEED)
            self.raiseEvent('connect')

        def on_start(self, e):
            print 'Preparing for listening'

        def on_connect(self, e):
            self.transition('Negotiation')


    class Negotiation(State):

        def eval(self):
            print 'checking validity'
            time.sleep(SPEED)
            print 'authenticating'
            time.sleep(SPEED)
            print 'registering'
            self.transition('Connected')

        def on_start(self, e):
            print 'Negotiating'


    class Connected(State):

        def eval(self):
            print 'Connected'

        def on_finish(self, e):
            self.transition('Listening')


    ctx = Context()
    ctx.i = 0
    m = StateMachine(initialState='Starting', context=ctx)
    m.appendStates(Starting(), Listening(), Negotiation(), Connected())
    m.start()