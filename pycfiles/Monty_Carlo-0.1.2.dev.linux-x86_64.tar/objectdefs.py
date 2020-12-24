# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/monty-carlo/objectdefs/objectdefs.py
# Compiled at: 2011-09-11 12:46:59
"""
Object definitions for a general system in concern. 
"""
import probes

class Element(object, probes.probeable_obj):
    """
    General definition of an element object.
    """

    def __init__(self, *args, **kwargs):
        probes.probeable_obj.__init__(self)
        self.explanation = ''
        self.parameters = []


class State(object, probes.probeable_obj):
    """
    Definition of the state object.
    """

    def __init__(self, *args, **kwargs):
        probes.probeable_obj.__init__(self)
        self.explanation = ''
        self.parameters = []
        self.constituents = None
        return


class Action(object, probes.probeable_obj):
    """
    Definition of the action object.
    Encapsulates an action on a state.
    """

    def __init__(self, *args, **kwargs):
        probes.probeable_obj.__init__(self)
        self.explanation = ''
        self.actson_states = None
        self.actson_elements = None
        self.language = None
        self.function = None
        return


class System(object, probes.probeable_obj):
    """
    Definition of the system object.
    """

    def __init__(self, *args, **kwargs):
        probes.probeable_obj.__init__(self)
        self.explanation = ''


class Potential(object, probes.probeable_obj):
    """
    A potential class.
    Defined with the presence of two elements of the system.
    """

    def __init__(self):
        probes.probeable_obj.__init__(self)
        self.explanation = ''


class ElementalInteraction(object, probes.probeable_obj):
    """
    A class for every interaction concerning two element-type objects
    """

    def __init__(self, function, *args, **kwargs):
        """
        an object of ElementalInteraction is defined with function that has
        two objects of type element as input.
        """
        probes.probeable_obj.__init__(self)
        self.function = function
        self.explanation = ''


class EnergyDefinition(object, probes.probeable_obj):
    """
    Class for energy definitions.
    An enery definition needs an elemental interaction
    And a rule of whom are interacting.
    """

    def __init__(self, elem_inter, rule, *args, **kwargs):
        probes.probeable_obj.__init__(self)