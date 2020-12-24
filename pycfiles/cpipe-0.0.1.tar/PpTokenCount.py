# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/cpip/core/PpTokenCount.py
# Compiled at: 2017-10-03 13:07:16
__doc__ = 'Keeps a count of Preprocessing tokens.\n'
__author__ = 'Paul Ross'
__date__ = '2011-07-10'
__rights__ = 'Copyright (c) 2008-2017 Paul Ross'
from cpip import ExceptionCpip
from cpip.core import PpToken

class ExceptionPpTokenCount(ExceptionCpip):
    """Exception when handling PpTokenCount object."""


class ExceptionPpTokenCountStack(ExceptionPpTokenCount):
    """Exception when handling PpTokenCountStack object."""


class PpTokenCount(object):
    """Maps of ``{token_type : integer_count, ...}``
    self._cntrTokAll is all tokens."""

    def __init__(self):
        self._cntrTokAll = {}
        self._cntrTokUncon = {}

    def __iadd__(self, other):
        """In-place add of the contents of another PpTokenCount object."""
        for tt in other._cntrTokAll:
            try:
                self._cntrTokAll[tt] += other._cntrTokAll[tt]
            except KeyError:
                self._cntrTokAll[tt] = other._cntrTokAll[tt]

        for tt in other._cntrTokUncon:
            try:
                self._cntrTokUncon[tt] += other._cntrTokUncon[tt]
            except KeyError:
                self._cntrTokUncon[tt] = other._cntrTokUncon[tt]

        return self

    def inc(self, tok, isUnCond, num=1):
        """Increment the count. tok is a PpToken, isUnCond is a boolean that is
        True if this is not conditionally compiled. num is the number of tokens
        to increment."""
        self._inc(tok.tt, isUnCond, num)

    def _inc(self, tokStr, isUnCond, num):
        """Increment the count. tok is a string, isUnCond is a boolean that is
        True if this is not conditionally compiled. num is the number of tokens
        to increment."""
        try:
            self._cntrTokAll[tokStr] += num
        except KeyError:
            self._cntrTokAll[tokStr] = num

        if isUnCond:
            try:
                self._cntrTokUncon[tokStr] += num
            except KeyError:
                self._cntrTokUncon[tokStr] = num

    @property
    def totalAll(self):
        """The total token count."""
        return sum(self._cntrTokAll.values())

    @property
    def totalAllUnconditional(self):
        """The token count of unconditional tokens."""
        return sum(self._cntrTokUncon.values())

    @property
    def totalAllConditional(self):
        """The token count of conditional tokens."""
        return sum(self._cntrTokAll.values()) - sum(self._cntrTokUncon.values())

    def tokenCount(self, theType, isAll):
        """Returns the token count of a particular type. If isAll is true then
        the count of all tokens is returned, if False the count of
        unconditional tokens is returned."""
        try:
            if isAll:
                return self._cntrTokAll[theType]
            else:
                return self._cntrTokUncon[theType]

        except KeyError:
            pass

        return 0

    def tokenCountNonWs(self, isAll):
        """Returns the token count of a particular type. If isAll is true then
        the count of all tokens is returned, if False the count of
        unconditional tokens is returned."""
        try:
            if isAll:
                return self.totalAll - self._cntrTokAll['whitespace']
            else:
                return self.totalAllUnconditional - self._cntrTokUncon['whitespace']

        except KeyError:
            pass

        if isAll:
            return self.totalAll
        return self.totalAllUnconditional

    def tokenTypesAndCounts(self, isAll, allPossibleTypes=True):
        """Generator the yields ``(type, count)`` in
        ``PpToken.LEX_PPTOKEN_TYPES`` order where type is a string and count an
        integer.
        
        If *isAll* is true then the count of all tokens is returned, if False the
        count of unconditional tokens is returned.
        
        If *allPossibleTypes* is True the counts of all token types are yielded
        even if zero, if False then only token types encountered will be
        yielded i.e. all counts will be non-zero."""
        for aType in PpToken.LEX_PPTOKEN_TYPES:
            if allPossibleTypes:
                yield (
                 aType, self.tokenCount(aType, isAll))
            elif isAll:
                if aType in self._cntrTokAll:
                    yield (
                     aType, self._cntrTokAll[aType])
            elif aType in self._cntrTokUncon:
                yield (
                 aType, self._cntrTokUncon[aType])


class PpTokenCountStack(object):
    """This simply holds a stack of PpTokenCount objects that can be created
    and popped of the stack."""

    def __init__(self):
        """ctor with empty stack."""
        self._stack = []

    def __len__(self):
        return len(self._stack)

    def __iadd__(self, other):
        self._stack[(-1)] += other
        return self

    def push(self):
        """Add a new counter object to the stack."""
        self._stack.append(PpTokenCount())

    def counter(self):
        """Returns a reference to the current PpTokenCount object."""
        if len(self._stack) == 0:
            raise ExceptionPpTokenCountStack('PpTokenCountStack.counter() on empty stack.')
        return self._stack[(-1)]

    def pop(self):
        """Pops the current PpTokenCount object off the stack and returns it."""
        if len(self._stack) == 0:
            raise ExceptionPpTokenCountStack('PpTokenCountStack.pop() on empty stack.')
        return self._stack.pop()

    def close(self):
        """Finalisation, will raise a ExceptionPpTokenCountStack if there is
        anything on the stack."""
        if len(self._stack) != 0:
            raise ExceptionPpTokenCountStack('PpTokenCountStack.close() on non-zero stack length [%d].' % len(self._stack))