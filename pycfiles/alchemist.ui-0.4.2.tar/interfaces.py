# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/alchemist/traversal/interfaces.py
# Compiled at: 2008-09-24 15:09:06
from zope import interface, schema

class IManagedContainer(interface.Interface):
    """
    """


class IConstraintManager(interface.Interface):
    """
    manages the constraints on a managed container
    """

    def setConstrainedValues(instance, target):
        """
        ensures existence of conformant constraint values
        to match the query.
        """
        pass

    def getQueryModifier(instance, container):
        """
        given an instance inspect for the query to retrieve 
        related objects from the given alchemist container.
        """
        pass