# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/cpip/util/MaxMunchGen.py
# Compiled at: 2017-10-03 13:07:16
"""Generic Maximal Munch generator."""
__author__ = 'Paul Ross'
__date__ = '2011-07-10'
__rights__ = 'Copyright (c) 2008-2017 Paul Ross'
from . import BufGen
from cpip import ExceptionCpip

class ExceptionMaxMunchGen(ExceptionCpip):
    """Exception specialisation for MaxMunchGen."""
    pass


def anyToken(theGen):
    """A function that always reads one token.
    This can be used as the last registered function to ensure that the token
    stream is read to completion. The kind returned is None."""
    try:
        next(theGen)
    except StopIteration:
        return (0, None, None)

    return (1, None, None)


class MaxMunchGen(object):
    """Provides a generator that applies Maximal munch rules."""

    def __init__(self, theGen, theFnS, isExclusive=False, yieldReplacement=False):
        """Constructor that takes a generator and a list of Maximal munch
        functions.
        Each function is required to take a generator as an object and return a
        triple (count, kind, replace) where:
        count   - is a integer
        kind    - is arbitrary.
        replace - is None or an iterable.
        Typically the functions should be written thus:
        def f(theGen):
            i = 0
            for aVal in theGen:
                if not <some condition of aVal>:
                    break
                i +=1
            return i, <kind>, <replace>
        Or (note the catching of StopIteration):
        def f(theGen):
            i = 0
            try:
                while theGen.next() <some condition>:
                    i += 1
            except StopIteration:
                pass
            return i, <kind>, <replace>
        
        If isExclusive is True then the first function that returns a non-zero
        integer will be used and the others will not be exercised for that token.
        """
        self._bufGen = BufGen.BufGen(theGen)
        self._fnS = theFnS
        self._isExcl = isExclusive
        self._yieldRepl = yieldReplacement

    @property
    def bufGen(self):
        return self._bufGen

    def gen(self):
        """Yields a maximal munch.
        If yieldReplacement is False these will be pairs of (iterable, kind)
        where kind is from the function, any replacement will be done on the fly.
        If yieldReplacement is True these will be triples of
        (iterable, kind, repl) where kind and repl are from the function with
        repl being None if no replacement. No replacement will have been done.
        
        TODO: Reconsider this design. Really yieldReplacement decides if the
        underlying generator buffer contains the replacement rather than whether
        self yields the replacement.
        """
        while 1:
            mySize = 0
            myKind = None
            myRepl = None
            myBufIdx = 0
            assert myBufIdx <= 1, 'self._bufGen.lenBuf is %d: %s' % (self._bufGen.lenBuf, self._bufGen._buf)
            for aFn in self._fnS:
                s, k, r = aFn(self._bufGen.gen())
                if s > 0:
                    if s == mySize:
                        raise ExceptionMaxMunchGen('Ambiguous result [%d] for munch.' % s)
                    elif s > mySize:
                        mySize = s
                        myKind = k
                        myRepl = r
                    if self._isExcl:
                        break

            if mySize == 0:
                raise StopIteration
            if myRepl is not None:
                if self._yieldRepl:
                    yield (
                     self._bufGen.slice(mySize), myKind, myRepl)
                else:
                    self._bufGen.replace(myBufIdx, mySize, myRepl)
                    yield (self._bufGen.slice(len(myRepl)), myKind)
            elif self._yieldRepl:
                yield (
                 self._bufGen.slice(mySize), myKind, None)
            else:
                yield (
                 self._bufGen.slice(mySize), myKind)

        return