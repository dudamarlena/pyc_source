# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/holmium/core/conditions.py
# Compiled at: 2016-02-28 21:16:09
"""
utility callables to be passed to holmium.core.Element(s) only_if parameter
"""
from abc import ABCMeta, abstractmethod
import re, threading
from six import add_metaclass

@add_metaclass(ABCMeta)
class BaseCondition(object):
    """
    base class to implement conditions passed
    to the ``only_if`` parameter of :class:`holmium.core.pageobject.ElementGetter`
    subclasses.
    """
    stack = threading.local()
    stack.stack = []

    def __call__(self, element):
        return self.evaluate(element)

    @abstractmethod
    def evaluate(self, element):
        """
        abstract method to be implemented by derived classes.
        """
        raise NotImplementedError

    def __enter__(self):
        self.stack.stack.append(self)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stack.stack.pop()

    @classmethod
    def get_current(cls):
        if cls.stack.stack:
            return cls.stack.stack[0]
        else:
            return


class VISIBLE(BaseCondition):
    """
    checks if the element is visible
    """

    def evaluate(self, element):
        return element and element.is_displayed()


class INVISIBLE(BaseCondition):
    """
    checks if the element is invisible
    """

    def evaluate(self, element):
        return not element or not element.is_displayed()


class MATCHES_TEXT(BaseCondition):
    """
    checks if the  element's text matches the provided
    regular expression.
    """

    def __init__(self, expr):
        self.expr = expr

    def evaluate(self, element):
        return element and re.compile(self.expr).match(element.text)


class ANY(BaseCondition):
    """
    checks if any of the elements in the collection
    match the condition.
    """

    def __init__(self, condition):
        self.cond = condition

    def evaluate(self, elements):
        return any(self.cond(el) for el in elements)


class ALL(BaseCondition):
    """
    checks if all of the elements in the collection
    match the condition.
    """

    def __init__(self, condition):
        self.cond = condition

    def evaluate(self, elements):
        return all(self.cond(el) for el in elements)