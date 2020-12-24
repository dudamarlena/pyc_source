# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/finenight/transition.py
# Compiled at: 2015-02-11 20:22:13
import copy

class Transition:
    """
    This object is a general representation of a transition, that is
    easier to use than a 4-tuple or a 3-tuple transition.
    """

    def __init__(self, tuple):
        """
        This is the constructor of a Transition.
        
        tuple may be a 4-tuple:
        (Q, E1*, E2*, Q) that is, The input state, The input symbol,
        The output symbol and the output state, respectely.

        tuple may also be a 3-tuple:
        (Q, E1, Q) that is, The input state, The input symbol
        and the output state, respectely.
        """
        self.start = str(tuple[0])
        self.input = tuple[1]
        if len(tuple) == 4:
            self.output = tuple[2]
            self.target = str(tuple[3])
        else:
            self.output = None
            self.target = str(tuple[2])
        return

    def __str__(self):
        """
        Return the string representation of the instance
        """
        output = '(' + self.start + ', '
        if self.output is not None:
            output += '(' + self.input + ', '
            output += self.output + '), '
        else:
            output += self.input + ', '
        output += self.target + ')'
        return output

    def inverse(self):
        """
        This function inverse the transition.
        such that, for a 4-tuple, (q1, a, b, q2) becomes (q1, b, a, q2).
        Note that it doesn't do nothing for a 3-tuple.
        """
        other = copy.copy(self)
        if other.output is not None:
            output = other.output
            other.output = other.input
            other.input = output
        return other