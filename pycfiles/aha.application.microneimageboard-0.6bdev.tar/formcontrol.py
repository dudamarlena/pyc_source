# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/aha/modelcontroller/formcontrol.py
# Compiled at: 2010-10-22 05:16:39
__doc__ = ' formcontrol.py - The helper class to control form transition\n                     and helper decorators\n\n$Id: formcontrol.py 639 2010-08-10 04:08:49Z ats $\n'
__author__ = 'Atsushi Shibata <shibata@webcore.co.jp>'
__docformat__ = 'plaintext'
__licence__ = 'BSD'
__all__ = ('FormControl', 'handle_state', 'validate')

class FormControl(object):
    """
    A class of from controller, managing the transition of the form.
    """
    INITIAL = 'initial'
    PROCESSING = 'processing'
    FAILURE = 'failure'
    SUCCESS = 'success'

    def __init__(self, states=None):
        """
        Initialize method, creating instance according to given arguments.
        states argument should be like:
            {STATE1:METHOD1,
             STATE2:(METHOD2, VALIDATOR2(opt.)),
            }
        """
        if states == None:
            states = {}
        if states != {} and self.INITIAL not in states:
            raise KeyError('The initial state needs for states.')
        self._states = states
        for (k, v) in self._states.items():
            cc = None
            if isinstance(v, tuple):
                cc = v[0]
            else:
                cc = v
            if not callable(cc):
                raise ValueError('The first tuple item for state %s should be method(callable)' % k)
            if not isinstance(v, tuple) or isinstance(v, tuple) and len(v) == 1:
                newv = (
                 cc, None)
                self._states[k] = newv
            elif not callable(v[1]):
                raise ValueError('The second tuple item for state %s should be method(callable)' % k)

        return

    def add_state(self, state, c, v=None):
        """
        A method to add state to FormControl instance.
        """
        if state in self._states:
            raise KeyError("A key '%s' is already defined" % state)
        if not callable(c):
            raise ValueError('The second argumentshould be method(callable)')
        self._states[state] = (c, v)

    def add_method(self, state, c):
        """
        A method to add method to state of FormControl instance.
        """
        if not callable(c):
            raise ValueError('The second argumentshould be method(callable)')
        if state not in self._states:
            self._states[state] = (c, None)
        else:
            self._states[state] = (
             c, self._states[state][1])
        return

    def add_validator(self, state, v):
        """
        A method to add method to state of FormControl instance.
        """
        if v is not None and not callable(v):
            raise ValueError('The second argumentshould be method(callable)')
        if state not in self._states:
            self._states[state] = (
             None, v)
        else:
            self._states[state] = (
             self._states[state][0], v)
        return

    def check_state(self, state):
        """
        A method to check if given state is available or not.
        """
        if state not in self.get_states():
            raise KeyError("The state '%s' is not available" % state)

    def get_states(self):
        """
        A method to obtain list of existing states.
        """
        return self._states.keys()

    def get_processor(self, state):
        """
        A method to obtain the callable for given state.
        """
        self.check_state(state)
        return self._states[state][0]

    def get_validator(self, state):
        """
        A method to obtain the callable for given state.
        """
        self.check_state(state)
        return self._states[state][1]

    def validate(self, state, *params, **kwd):
        """
        A method to process validation and obtain FormState object, and
          process form.
        """
        v = self.get_validator(state)
        if v == None:
            return state
        return v(state=state, *params, **kwd)

    def process(self, state, *params, **kwd):
        """
        A method to process job and obtain FormState object.
        """
        p = self.get_processor(state)
        return p(*params, **kwd)

    def handle_state(self, *states):

        def set_states(func):
            for s in states:
                self.add_method(s, func)

            return func

        return set_states

    def handle_validate(self, *states):

        def set_validators(func):
            for s in states:
                self.add_validator(s, func)

            return func

        return set_validators


class handle_state(object):

    def __init__(self, klass, state):
        self.klass = klass
        self.state = state

    def __call__(self, func):
        if isinstance(self.state, tuple):
            for s in self.state:
                self.klass.add_method(s, func)

        else:
            self.klass.add_method(self.state, func)
        return func


class validate(object):

    def __init__(self, klass, state):
        self.klass = klass
        self.state = state

    def __call__(self, func):
        if isinstance(self.state, tuple):
            for s in self.state:
                self.klass.add_validator(s, func)

        else:
            self.klass.add_validator(self.state, func)
        return func