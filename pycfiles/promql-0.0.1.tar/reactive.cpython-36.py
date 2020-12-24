# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/prompt_tool_kit/reactive.py
# Compiled at: 2019-08-15 23:53:38
# Size of source mod 2**32: 1842 bytes
__doc__ = '\nprompt_tool_kit is designed a way that the amount of changing state is reduced\nto a minimum. Where possible, code is written in a pure functional way. In\ngeneral, this results in code where the flow is very easy to follow: the value\nof a variable can be deducted from its first assignment.\n\nHowever, often, practicality and performance beat purity and some classes still\nhave a changing state. In order to not having to care too much about\ntransferring states between several components we use some reactive\nprogramming. Actually some kind of data binding.\n\nWe introduce two types:\n\n- Filter: for binding a boolean state. They can be chained using & and |\n  operators. Have a look in the ``filters`` module. Resolving the actual value\n  of a filter happens by calling it.\n\n- Integer: for binding integer values. Reactive operations (like addition and\n  substraction) are not suppported. Resolving the actual value happens by\n  casting it to int, like  ``int(integer)``. This way, it is possible to use\n  normal integers as well for static values.\n'
from __future__ import unicode_literals
from abc import ABCMeta, abstractmethod
from six import with_metaclass

class Integer(with_metaclass(ABCMeta, object)):
    """Integer"""

    @abstractmethod
    def __int__(self):
        return 0

    @classmethod
    def from_callable(cls, func):
        """
        Create an Integer-like object that calls the given function when it is
        resolved to an int.
        """
        return _IntegerFromCallable(func)


Integer.register(int)

class _IntegerFromCallable(Integer):

    def __init__(self, func=0):
        self.func = func

    def __repr__(self):
        return 'Integer.from_callable(%r)' % self.func

    def __int__(self):
        return int(self.func())