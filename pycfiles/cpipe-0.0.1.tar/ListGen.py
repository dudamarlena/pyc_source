# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/cpip/util/ListGen.py
# Compiled at: 2017-10-03 13:07:16
__doc__ = 'Treats a list as a generator with an optional additional generator. This is\nused for macro replacement for example.\n'
__author__ = 'Paul Ross'
__date__ = '2011-07-10'
__rights__ = 'Copyright (c) 2008-2017 Paul Ross'

class ListAsGenerator(object):
    """Class that takes a list and provides a generator on that list. If the
    list is exhausted and call for another object is made then it is pulled of
    the generator (if available).
    
    The attribute ``listIsEmpty`` is True if the immediate list is empty.
    
    Iterating through the result and stopping when the list is exhausted using
    the flag listIsEmpty:
    
    To be clear: when this flag is set, for example if we have a list [0,1,2,3]
    followed by ['A', 'B', 'C'] thus::
    
        myObj = ListAsGenerator(range(3), ListAsGenerator(list('ABC')).next())
    
    And we try to iterate over it with list comprehension::
    
        myGen = myObj.next()
        myResult = [x for x in myGen if not myObj.listIsEmpty]
        
    myResult will be [0, 1,] because when 3 is yielded the flag is False as
    it refers to the _next_ item.
    
    Similarly the list comprehension::
    
        myResult = [x for x in myGen if myObj.listIsEmpty]
    
    Will be [3, 'A', 'B', 'C']
    
    If you want to recover the then this the technique::
    
        myResult = []
        if not myObj.listIsEmpty:
            for aVal in myGen:
                myResult.append(aVal)
                if myObj.listIsEmpty:
                    break
    
    
    Or exclude the list then this the technique::
    
        if not myObj.listIsEmpty:
            for aVal in myGen:
                if myObj.listIsEmpty:
                    break
        myResult = [x for x in myGen]
    
    The rationale for this behaviour is for generating macro replacement tokens
    in that the list contains tokens for re-examination and the last token may
    turn out to be a function like macro that needs the generator to (possibly)
    complete the expansion. Once that last token has been re-examined we do
    not want to consume any more tokens than necessary.
    """

    def __init__(self, theList, theGen=None):
        """Initialise the class with a list of objects to yield and,
        optionally, a generator. If the generator is present it will be used
        as a continuation of the list."""
        self._list = theList
        self._gen = theGen
        self._listIdx = 0

    def __next__(self):
        """yield the next value. The attribute listIsEmpty will be set True
        immediately before yielding the last value."""
        self._listIdx = 0
        for aVal in self._list:
            self._listIdx += 1
            r = yield aVal
            if r is not None:
                self._listIdx -= 1
                yield
                yield r

        if self._gen is not None:
            while 1:
                r = yield next(self._gen)
                if r is not None:
                    yield
                    yield r
            else:
                continue

        return

    next = __next__

    @property
    def listIsEmpty(self):
        """True if the next yield would come from the generator, not the list."""
        return self._listIdx >= len(self._list)