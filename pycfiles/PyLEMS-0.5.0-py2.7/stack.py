# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/lems/base/stack.py
# Compiled at: 2015-11-16 08:17:20
"""
Stack class.

@author: Gautham Ganapathy
@organization: LEMS (http://neuroml.org/lems/, https://github.com/organizations/LEMS)
@contact: gautham@lisphacker.org
"""
from lems.base.base import LEMSBase
from lems.base.errors import StackError

class Stack(LEMSBase):
    """
    Basic stack implementation.
    """

    def __init__(self):
        """
        Constructor.
        """
        self.stack = []

    def push(self, val):
        """
        Pushed a value onto the stack.

        @param val: Value to be pushed.
        @type val: *
        """
        self.stack = [
         val] + self.stack

    def pop(self):
        """
        Pops a value off the top of the stack.

        @return: Value popped off the stack.
        @rtype: *

        @raise StackError: Raised when there is a stack underflow.
        """
        if self.stack:
            val = self.stack[0]
            self.stack = self.stack[1:]
            return val
        raise StackError('Stack empty')

    def top(self):
        """
        Returns the value off the top of the stack without popping.

        @return: Value on the top of the stack.
        @rtype: *

        @raise StackError: Raised when there is a stack underflow.
        """
        if self.stack:
            return self.stack[0]
        raise StackError('Stack empty')

    def is_empty(self):
        """
        Checks if the stack is empty.

        @return: True if the stack is empty, otherwise False.
        @rtype: Boolean
        """
        return self.stack == []

    def __str__(self):
        """
        Returns a string representation of the stack.

        @note: This assumes that the stack contents are capable of generating
        string representations.
        """
        if len(self.stack) == 0:
            s = '[]'
        else:
            s = '[' + str(self.stack[0])
            for i in range(1, len(self.stack)):
                s += ', ' + str(self.stack[i])

            s += ']'
        return s

    def __repr__(self):
        return self.__str__()