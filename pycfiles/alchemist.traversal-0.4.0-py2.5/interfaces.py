# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/alchemist/traversal/interfaces.py
# Compiled at: 2008-09-24 15:09:06
from zope import interface, schema

class IManagedContainer(interface.Interface):
    """
    """
    pass


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