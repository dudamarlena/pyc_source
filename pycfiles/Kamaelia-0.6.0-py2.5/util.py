# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Axon/util.py
# Compiled at: 2008-10-19 12:19:52
"""===========================================
General utility functions & common includes
===========================================

"""
from AxonExceptions import invalidComponentInterface
import sets
production = False

def logError(someException, *args):
    """    Currently does nothing but can be rewritten to log ignored errors if the
    production value is true.
    """
    pass


def axonRaise(someException, *args):
    """    Raises the supplied exception with the supplied arguments *if*
    Axon.util.production is set to True.
    """
    if production:
        logError(someException, *args)
        return False
    else:
        raise someException(*args)


def removeAll(xs, y):
    """Very simplistic method of removing all occurances of y in list xs."""
    try:
        while 1:
            del xs[xs.index(y)]

    except ValueError, reason:
        if not reason.__str__() == 'list.index(x): x not in list':
            raise ValueError, reason


def listSubset(requiredList, suppliedList):
    """Returns true if the requiredList is a subset of the suppliedList."""
    return sets.Set(requiredList).issubset(sets.Set(suppliedList))


def testInterface(theComponent, interface):
    """Look for a minimal match interface for the component.
   The interface should be a tuple of lists, i.e. ([inboxes],[outboxes])."""
    (requiredInboxes, requiredOutboxes) = interface
    if not listSubset(requiredInboxes, theComponent.Inboxes):
        return axonRaise(invalidComponentInterface, 'inboxes', theComponent, interface)
    if not listSubset(requiredOutboxes, theComponent.Outboxes):
        return axonRaise(invalidComponentInterface, 'outboxes', theComponent, interface)
    return True


def safeList(arg=None):
    """Returns the list version of arg, otherwise returns an empty list."""
    try:
        return list(arg)
    except TypeError:
        return []


class Finality(Exception):
    """Used for implementing try...finally... inside a generator."""
    pass