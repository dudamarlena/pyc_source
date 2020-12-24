# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/alchemist/traversal/managed.py
# Compiled at: 2008-10-16 00:49:22
__doc__ = "\n\n$Id: $\n\nfunctionally this gives us class descriptors that return alchemsit z3 containers \n\nideally we should hook into sa's property definition syntax, so we can have a z3 container\nas an sa instructmented container class.\n"
from zope import interface
from zope.dottedname.resolve import resolve
from zope.app.security.protectclass import protectLikeUnto
from zope.security.proxy import removeSecurityProxy
from zope.location import ILocation
from ore.alchemist.container import PartialContainer
from sqlalchemy import orm
import interfaces

class _ManagedContainer(PartialContainer):

    def __repr__(self):
        m = self.__class__.__bases__[1]
        s = '%s.%s' % (m.__module__, m.__name__)
        return '<Managed %s>' % s

    def __setitem__(self, key, value):
        super(_ManagedContainer, self).__setitem__(key, value)
        self.constraints.setConstrainedValues(self.__parent__, value)

    def setConstraintManager(self, constraints):
        self.constraints = constraints
        if self.__parent__ is not None:
            self.setQueryModifier(constraints.getQueryModifier(self.__parent__, self))
        return


class ConstraintManager(object):
    """
    manages the constraints on a managed container
    """

    def setConstrainedValues(self, instance, target):
        """
        ensures existence of conformant constraint values
        to match the query.
        """
        pass

    def getQueryModifier(self, instance, container):
        """
        given an instance inspect for the query to retrieve 
        related objects from the given alchemist container.
        """
        pass


class One2Many(ConstraintManager):

    def __init__(self, fk):
        self.fk = fk

    def getQueryModifier(self, instance, container):
        mapper = orm.class_mapper(instance.__class__)
        primary_key = mapper.primary_key_from_instance(instance)[0]
        return container.domain_model.c[self.fk] == primary_key

    def setConstrainedValues(self, instance, target):
        trusted = removeSecurityProxy(instance)
        mapper = orm.object_mapper(trusted)
        primary_key = mapper.primary_key_from_instance(trusted)[0]
        column = target.__class__.c[self.fk]
        setattr(target, column.name, primary_key)


def one2many(name, container, fk):
    constraint = One2Many(fk)
    container = ManagedContainerDescriptor(name, container, constraint)
    return container


class ManagedContainerDescriptor(object):
    _container_class = None
    interface.implements(interfaces.IManagedContainer)

    def __init__(self, name, container, constraint):
        self.name = name
        self.container = container
        self.constraint = constraint

    def __get__(self, instance, class_):
        if instance is None and self._container_class is None:
            return
        container = self.domain_container()
        if instance is None:
            return container
        container.__parent__ = instance
        container.__name__ = self.name
        container.setConstraintManager(self.constraint)
        return container

    @property
    def domain_container(self):
        if self._container_class:
            return self._container_class
        container_class = resolve(self.container)
        self._container_class = type('ManagedContainer', (_ManagedContainer, container_class), dict(container_class.__dict__))
        protectLikeUnto(self._container_class, container_class)
        return self._container_class