# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/kreveik/classes/other.py
# Compiled at: 2012-09-09 23:45:49
"""
This module houses class definitions that more complex class definitions are inherited from.
"""
import logging

class Ensemble(object):
    """Base class for all that are going to be used as an ensemble of elements that are subject to 
    Genetical Algorithm
    """

    def __init__(self):
        self.scorer = None
        self.selector = None
        self.mutator = None
        self.killer = None
        return


class Element(object):
    """Base class for all that are going to be used as individuals within an element in a Genetical 
    Algorithm
    """

    def __init__(self):
        self.score = None
        self.mutated = 0
        self.parent = None
        self.children = []
        return


class ProbeableObj(object):
    """
    Base class for objects that a Probe object can be attached. 
    """

    def __init__(self):
        self.probes = []

    def attach(self, probe):
        if probe in self.probes:
            logging.warning('The probe is already attached.')
        else:
            self.probes.append(probe)

    def __call__(self, probed):
        self.attach(probed)

    def populate_probes(self, subroutine):
        for probe in self.probes:
            if probe.subroutine == subroutine:
                measured = probe.function(self)
                probe.data.append(measured)


class Mutator(object):
    """This is the class definition for the mutators. A mutating function must be given as an
    input
    """

    def __init__(self, function):
        self.mutation = function

    def __call__(self, element):
        self.mutation(element)


class Selector(object):
    """This is the class definition for the selector of the genetic iteration
    The selecting function must be supplied as an input.
    """

    def __init__(self, function, **kwargs):
        self.selection = function
        self.kwargs = kwargs

    def __call__(self, element):
        self.selection(element, self.kwargs)


class Killer(object):
    """This is the base class definition for the killer. A killing function must be supplied, which
    will act on ensemble objects.
    """

    def __init__(self, function):
        self.scoring = function

    def __call__(self, ensemble):
        self.scoring(ensemble)


class Scorer(object):
    """This is the base class definition for the scorers. A scoring function must be supplied.
    """

    def __init__(self, function):
        self.scoring = function

    def __call__(self, element):
        self.scoring(element)