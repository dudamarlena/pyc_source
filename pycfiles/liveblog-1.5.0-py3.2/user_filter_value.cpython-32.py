# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/superdesk/security/core/impl/processor/user_filter_value.py
# Compiled at: 2013-10-02 09:54:57
"""
Created on Feb 28, 2013

@package: superdesk security
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Processor that provides a static value for filters that can have predicted resource value. In this case we are referring to
@see: IAuthenticatedFilterService service where we actually know that the valid resource value is the same with the authenticated
value.
"""
from acl.api.filter import IAclFilter
from acl.spec import Filter
from ally.container import wire
from ally.container.ioc import injected
from ally.container.support import setup
from ally.design.processor.attribute import requires, defines
from ally.design.processor.context import Context
from ally.design.processor.handler import HandlerProcessorProceed, Handler
from collections import Iterable
from inspect import isclass
import logging
log = logging.getLogger(__name__)

class PermissionFilters(Context):
    """
    The permission context.
    """
    filters = requires(list)
    values = defines(dict, doc='\n    @rtype: dictionary{TypeProperty: string}\n    The static values to be used for the permission, as a key the type property that has the value.\n    ')


class Solicitation(Context):
    """
    The solicitation context.
    """
    userId = requires(int)
    permissions = requires(Iterable)


@injected
@setup(Handler, name='userValueForFilter')
class UserValueForFilter(HandlerProcessorProceed):
    """
    Processor that provides the user value for filters that consider the authenticated user is to be valid if equal with the
    resource user id.
    """
    equaliltyUserFilterClasses = list
    wire.entity('equaliltyUserFilterClasses')

    def __init__(self):
        """
        Construct the persistence invoker service.
        """
        assert isinstance(self.equaliltyUserFilterClasses, list), 'Invalid user filter classes %s' % self.equaliltyUserFilterClasses
        for clazz in self.equaliltyUserFilterClasses:
            assert isclass(clazz), 'Invalid class %s' % clazz
            if not issubclass(clazz, IAclFilter):
                raise AssertionError('Invalid filter class %s' % clazz)

        super().__init__()

    def process(self, Permission: PermissionFilters, solicitation: Solicitation, **keyargs):
        """
        @see: HandlerProcessorProceed.process
        
        Process permission static user filters.
        """
        assert issubclass(Permission, PermissionFilters), 'Invalid permission class %s' % Permission
        assert isinstance(solicitation, Solicitation), 'Invalid solicitation %s' % solicitation
        assert isinstance(solicitation.permissions, Iterable), 'Invalid permissions %s' % solicitation.permissions
        assert isinstance(solicitation.userId, int), 'Invalid solicitation user id %s' % solicitation.userId
        solicitation.permissions = self.processPermissions(solicitation.permissions, solicitation.userId)

    def processPermissions(self, permissions, userId):
        """
        Process the permissions for static user filters.
        """
        for permission in permissions:
            assert isinstance(permission, PermissionFilters), 'Invalid permission %s' % permission
            if not permission.filters:
                yield permission
                continue
            k = 0
            while k < len(permission.filters):
                rfilter = permission.filters[k]
                k += 1
                assert isinstance(rfilter, Filter), 'Invalid filter %s' % rfilter
                for clazz in self.equaliltyUserFilterClasses:
                    if isinstance(rfilter.filter, clazz):
                        assert isinstance(rfilter.filter, IAclFilter), 'Invalid acl filter %s' % rfilter.filter
                        assert rfilter.filter.isAllowed(userId, userId), 'Filter %s failed to allow for the expected behavior' % rfilter.filter
                        if not log.debug('Replaced %s with the static user id value %s', rfilter.filter, userId):
                            assert True
                            if permission.values is None:
                                permission.values = {}
                            permission.values[rfilter.resource] = str(userId)
                            k -= 1
                            del permission.filters[k]
                            break

            yield permission

        return