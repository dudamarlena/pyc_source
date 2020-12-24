# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pystates/pystates.py
# Compiled at: 2009-10-15 15:40:50
"""
pystates - A simple and powerful python state machine framework using coroutines

Example:

  from pystates import StateMachine, State

  class MyMachine(StateMachine):
    def IDLE(self):
      while True:
        ev = yield
        if ev.type == pygame.KEYDOWN:
          self.transition("RUNNING", ev.key)

    class RUNNING(State):
      def eval(self, key):
        print "you pressed the %s key" % key
        while True:
          ev = yield
          if self.duration() > 5.0:
            self.transition("COUNTDOWN")

    class COUNTDOWN(State):
      def eval(self):
        i = 10
        while True:
          ev = yield
          print "i = %d" % i
          if i == 0:
            self.transition("IDLE")
          i -= 1

See the README for a details on how to implement your own StateMachines
"""
import time, logging
__all__ = [
 'StateMachine', 'Sequence', 'Parallel', 'LerpFunc', 'Func', 'Wait']

class StateMachine(object):
    """StateMachine
  Do not instantiate this class directly.  Instead, make a subclass.  Your
  subclass should contain nested subclasses of State that implement the states
  your machine can achieve.
  """

    def __init__(self, name=None, time=time.time, log=None):
        """
    Keyword arguments:
      name: The name by which your StateMachine is known. It defaults to the name of
            the class
      time: An alternative function used to tell time.  For example, sometimes with
            pygame its useful to use pygame.ticks for consistency.  It defaults to
            time.time()
      log:  If you supply a python logging object, your StateMachine will use it to
            log transitions.
    """
        self.name = name and name or str(self.__class__.__name__)
        self.time = time
        self.log = log and log.debug or (lambda *args: None)
        self.done = False
        self.in_state = False

    def handle(self, ev):
        """
    When you call this method, this machine's current state will resume with
    the supplied ev object.
    """
        if self.done:
            raise StopIteration
        try:
            self.in_state = True
            try:
                res = self.state_gen.send(ev)
            except TypeError:
                self.state_gen.next()
                res = self.state_gen.send(ev)

            self.in_state = False
            return res
        except StopIteration, exc:
            self.in_state = False
            self.state_gen = exc.args[0]

    def start(self, state_func, *state_args):
        """
    If this machine has a state named by the state_func argument, then the machine
    will activate the named state.  This is essentially a transition from a NULL
    state to the named state.

    Any args are passed to the eval method of the named state.
    """
        self.state_gen = self.activate_state(state_func, state_args)

    def transition(self, state_func, *state_args):
        """
    If this machine has a state named by the state_func argument, then the machine
    will transition to the named state.

    Any args are passed to the new state_func.
    """
        state_gen = self.activate_state(state_func, state_args)
        if self.in_state:
            raise StopIteration(state_gen)
        else:
            self.state_gen = state_gen

    def activate_state(self, state_func, state_args):
        self.log('%s activating state %s', str(self), state_func.__name__)
        self.state = state_func
        self.state_start_time = self.time()
        state_gen = state_func(*state_args)
        return state_gen

    def halt(self):
        self.done = True

    def duration(self):
        return self.time() - self.state_start_time

    def __str__(self):
        return '<StateMachine:%s>' % self.name


class Parallel(StateMachine):

    def __init__(self, *sequences):
        StateMachine.__init__(self, 'parallel')
        self.sequences = map(lambda s: isinstance(s, Sequence) and s or Sequence(s), sequences)

    def HEAD(self):
        """
    this is the master state for this parallel
    it calls "handles" each of its sequences sequentially
    until the last is done.
    """
        for sequence in self.sequences:
            sequence.start(sequence.HEAD)

        while len(self.sequences):
            for sequence in self.sequences:
                try:
                    sequence.handle(None)
                except StopIteration:
                    self.sequences.remove(sequence)

        self.halt()
        return


class Sequence(StateMachine):

    def __init__(self, *states):
        StateMachine.__init__(self, 'sequence')
        self.states = states
        self.state_idx = -1

    def HEAD(self):
        """
      this is the master state for this sequence
      it calls "handles" the states in self.states sequentially until
      the last is done.
      states in this sequence will transition back to this state when done
    """
        self.state_idx += 1
        while True:
            ev = yield
            try:
                next_state = self.states[self.state_idx]
                self.transition(lambda : next_state(self))
            except IndexError:
                self.halt()


def Wait(t):

    def STATE_Wait(machine):
        print 'wait duration(%f)' % t
        while True:
            ev = yield
            if machine.duration() > t:
                machine.transition(machine.HEAD)

    return STATE_Wait


def Func(f, *args, **kwargs):

    def STATE_Func(machine):
        while True:
            ev = yield
            f(*args, **kwargs)
            machine.transition(machine.HEAD)

    return STATE_Func


def LerpFunc(f, t, over=(0.0, 1.0), extraArgs=[]):

    def STATE_LerpFunc(machine):
        (fromData, toData) = over
        data = lambda duration: duration / t * (toData - fromData) + fromData
        while True:
            ev = yield
            if machine.duration() < t:
                f(data(machine.duration()), *extraArgs)
            else:
                machine.transition(machine.HEAD)

    return STATE_LerpFunc