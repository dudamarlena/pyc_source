# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/acl/aco.py
# Compiled at: 2009-04-27 10:47:19
"""
Access Control Objects.

"""
import re
from acl.exc import ExistingACOError, NoACOMatchError
__all__ = [
 'Target', 'ACO', 'Resource', 'Operation']

class Target(object):
    """
    Represent the target ACO in a request, which may not exist.
    
    """

    def __init__(self, resource, operation):
        self.resource = resource
        self.operation = operation

    def __unicode__(self):
        """
        Return the URI for the target ACO.
        
        """
        return 'aco:%s#%s' % (self.resource, self.operation)


class ACO(object):
    """
    Recursive Access Control Object.
    
    An ACO is the unit to be protected with ACLs. It can be a resource or an
    operation.
    
    .. attribute:: name
    
        The name of this ACO.
    
    """
    invalid_name_pattern = re.compile('[/#\n\r]')

    def __init__(self, name):
        """
        Create an ACO called ``name`` with no parent.
        
        :param name: The name for the current ACO.
        :type name: basestring
        :raises ValueError: If ``name`` contains forward slashes, number signs,
            and/or new line characters.
        
        """
        if self.invalid_name_pattern.search(name):
            raise ValueError('"%s" is an invalid name for an ACO' % name)
        self.name = name
        self._parent = None
        return

    def get_ancestors(self, include_myself=False):
        """
        Return the ancestors of the current ACO.
        
        :param include_myself: Should the current ACO object be appended?
        :type include_myself: bool
        :return: A list whose users are the ancestor objects.
        :rtype: list
        
        """
        ancestors = []
        if self._parent:
            my_ancestors = self._parent.get_ancestors(True)
            ancestors.extend(my_ancestors)
        if include_myself:
            ancestors.append(self)
        return tuple(ancestors)


class Resource(ACO):
    """
    Resource definition.
    
    A resource is the unit on which one or more *operations* can be performed.
    
    """

    def __init__(self, name, *children):
        """
        
        :param name: The name of this resource.
        :type name: basestring
        :raisess ExistingACOError: If one of the children already exists.
        
        The ``children`` are the sub-resources and/or operations contained in
        this resource.
        
        """
        super(Resource, self).__init__(name)
        self._resources = {}
        self._operations = {}
        for child in children:
            if isinstance(child, self.__class__):
                self.add_subresource(child)
            else:
                self.add_operation(child)

    def add_subresource(self, resource):
        """
        Add ``resource`` to this resource.
        
        :param resource: A sub-resource to be contained in this resource.
        :type resource: :class:`Resource`
        :raises ExistingACOError: If ``resource`` is already in.
        
        It also sets ``resource``'s parent to this resource.
        
        """
        resource._parent = self
        if resource.name in self._resources:
            raise ExistingACOError('ACO %s already has a sub-resource called %s' % (
             self, resource.name))
        self._resources[resource.name] = resource

    def get_subresource(self, subresource_name):
        """
        Return the subresource ``subresource_name``.
        
        :param subresource_name: The name of a subresource contained in this
            resource.
        :type subresource_name: basestring
        :return: The object for the subresource ``subresource_name``.
        :rtype: :class:`Resource`
        :raises NoACOMatchError: If the subresource is not contained in
            this resource.
        
        """
        if subresource_name not in self._resources:
            raise NoACOMatchError('Resource %s has no sub-resource "%s"' % (
             self, subresource_name))
        return self._resources[subresource_name]

    def add_operation(self, operation):
        """
        Add ``operation`` to this resource.
        
        :param operation: An operation to be available for this resource.
        :type resource: :class:`Operation`
        :raises ExistingACOError: If ``operation`` is already available.
        
        It also sets ``operation``'s parent to this resource.
        
        """
        operation._parent = self
        if operation.name in self._operations:
            raise ExistingACOError('ACO %s already has an operation called %s' % (
             self, operation.name))
        self._operations[operation.name] = operation

    def get_operation(self, operation_name):
        """
        Return the operation ``operation_name``.
        
        :param operation_name: The name of a operation available for this
            resource.
        :type operation_name: basestring
        :return: The object for the operation ``operation_name``.
        :rtype: :class:`Operation`
        :raises NoACOMatchError: If the operation is not available for
            this resource.
        
        """
        if operation_name not in self._operations:
            raise NoACOMatchError('Resource %s has no operation "%s"' % (
             self, operation_name))
        return self._operations[operation_name]

    def load_acos(self, target):
        """
        Return all the ACOs involved in the ``target``.
        
        :param target: The target ACO.
        :type target: :class:`Target`
        :return: The objects for the ACOs involved in the ``target``.
        :rtype: list
        :raises NoACOMatchError: If one of the ACOs specified in the ``target``
            aren't defined.
        
        For example, if ``target`` represents the
        ``aco:/admin/accounts#add`` ACO, the :class:`ACO` objects represented
        by the following URIs will be returned:
        
        - ``aco:/`` -- the root ACO.
        - ``aco:/admin``
        - ``aco:/admin/accounts``
        - ``aco:/admin/accounts#add``
        
        """
        acos = [
         self]
        subresources = target.resource[1:].split('/')
        current_resource = self
        for subresource in subresources:
            current_resource = current_resource.get_subresource(subresource)
            acos.append(current_resource)

        final_resource = current_resource
        operation = final_resource.get_operation(target.operation)
        acos.append(operation)
        return acos

    def target_exists(self, target):
        """
        Check that the ``target`` ACO is defined in this ACO.
        
        :param target: The target ACO.
        :type target: :class:`Target`
        :return: Whether it exists or not.
        :rtype: bool
        
        """
        try:
            self.load_acos(target)
            return True
        except NoACOMatchError:
            return False

    def __unicode__(self):
        """Represent this resource as an URI."""
        everybody = [ ancestor.name for ancestor in self.get_ancestors(True) ]
        everybody = everybody[1:]
        everybody = ('/').join(everybody)
        return 'aco:/%s' % everybody


class Operation(ACO):
    """
    Operation definition.
    
    An operation is an action that can be performed on a resource (see
    :class:`Resource`).
    
    """

    def __unicode__(self):
        """Represent this operation and its parent resource as an URI."""
        resource = unicode(self._parent)
        return '%s#%s' % (resource, self.name)