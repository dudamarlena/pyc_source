# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rd/Work/Edgy/workflow/.virtualenv-python/lib/python2.7/site-packages/edgy/workflow/transition.py
# Compiled at: 2016-02-21 07:40:05
"""
The smallest atom of ``edgy.workflow`` is a ``Transition``, which basically is a regular python
callable with additional metadata to make the system aware of when it can be applied.

"""
from __future__ import absolute_import, print_function, unicode_literals
import functools
from edgy.workflow.constants import WILDCARD
from edgy.workflow.utils import issequence

class Transition(object):
    """
    Defines when and how to go from one state to another, eventually applying a user-defined
    side-effect while being applied.

    Example::

        >>> t = Transition(name='sleep', source='awake', target='asleep')

        >>> class Person(object):
        ...     state = 'awake'

        >>> me = Person()
        >>> t(me)
        >>> me.state
        'asleep'

    This class can also be used as a decorator::

        >>> @Transition(source='asleep', target='awake')

        >>> def wakeup(self, subject):
        ...     print('HEY!')

        >>> wakeup(me)
        >>> me.state
        'awake'

    A special wildcard source can make transitions work from any state. Just specify "*" as a
    transition source and you'll be able to transition from any state.

    """

    def __new__(cls, handler=None, **kwargs):
        if handler:
            return super(Transition, cls).__new__(cls)

        @functools.wraps(Transition)
        def decorator(handler):
            return Transition(handler=handler, **kwargs)

        return decorator

    def __init__(self, handler=None, name=None, source=None, target=None):
        self.source = tuple(source if issequence(source) else (source,))
        self.target = target
        self._name = name
        if handler:
            self.handler = handler or self.handler

    def __call__(self, subject, *args, **kwargs):
        if WILDCARD not in self.source and subject.state not in self.source:
            raise RuntimeError((b'This transition cannot be executed on a subject in "{}" state, authorized source states are {}.').format(subject.state, (b', ').join([ (b'"{}"').format(state) for state in self.source ])))
        try:
            retval = self.handler(self, subject, *args, **kwargs)
            subject.state = self.target
        except Exception as e:
            raise

        return retval

    @property
    def __name__(self):
        return self._name or self.handler.__name__

    name = __name__

    def __repr__(self):
        return (b'<{}.{} object "{}" ({} to {}) at {}>').format(type(self).__module__, type(self).__name__, self.__name__, (b'/').join(self.source), self.target, hex(id(self)))

    def handler(self, subject, *args, **kwargs):
        """
        Default handler do not apply any side effect. Either implement it in a subclass or pass a
        callable to the constructor to define your transition behavior.

        :param subject:
        :param args:
        :param kwargs:

        """
        pass