# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rd/Work/Edgy/workflow/.virtualenv-python/lib/python2.7/site-packages/edgy/workflow/stateful.py
# Compiled at: 2016-02-21 07:39:59
"""
For now, a "stateful object" is, to this library, anything that as a "state" attribute that can
be read. If it quacks, then it's a duck.

However, as an helper class to demonstrate how a workflow can be bound to an object, we provide
``StatefulObject`` as an example implementation that you can use.

"""
from __future__ import absolute_import, print_function, unicode_literals
import functools

class StatefulObject(object):
    """
    Example stateful object.

    To use it, subclass me and set the workflow attribute to a ``edgy.workflow.Workflow`` instance.

    .. attribute:: workflow

        A workflow instance, setting the system in which the instances of this object live.

    .. attribute:: initial_state

        The default initial state of this object.

    .. attribute:: current_state

        The current state of this object.

    """
    workflow = None
    initial_state = None
    current_state = None

    @property
    def available_transitions(self):
        return self.workflow.get_available_transitions_for(self)

    def __new__(cls, *args, **kwargs):
        if not cls.workflow:
            raise RuntimeError(b'It is not possible to instanciate a StatefulObject without a workflow.')
        state = kwargs.pop(b'state', None)
        instance = super(StatefulObject, cls).__new__(cls)
        if state:
            instance.current_state = state
        return instance

    def __repr__(self):
        return (b'<{}.{} object with {} "{}" at {}>').format(type(self).__module__, type(self).__name__, b'state' if self.state in self.workflow.states else b'unknown state', self.state, hex(id(self)))

    def __getattr__(self, attr):
        if attr in self.workflow:
            return functools.partial(self.workflow[attr], subject=self)
        raise AttributeError(b'%r object has no attribute %r' % (self.__class__, attr))

    def _get_state(self):
        return self.current_state or self.initial_state

    def _set_state(self, state):
        self.current_state = state

    state = property(fget=_get_state, fset=_set_state, doc=b'\n    Helper for getting the actual state of an object. You should use this instead of\n    ``initial_state`` and ``current_state`` if your only aim is to read or write a new state to\n    this object.\n\n    Beware though, the setter of this property will override the state, without going through the\n    transitions. If you wanna run the transitions (and in 95% of the cases, you should, otherwise\n    this library is a pretty bad choice for you), then a proxy attribute exist on the object\n    for each transition name, and you should just call it (for example, if a transition is named\n    ``wakeup``, you can just call ``instance.wakeup()``).\n    ')