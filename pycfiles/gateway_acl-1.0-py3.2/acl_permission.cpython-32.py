# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/acl/core/impl/processor/gateway/acl_permission.py
# Compiled at: 2013-10-04 10:48:33
"""
Created on Aug 21, 2013

@package: gateway acl
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Processor that adds the permissions based on ACL structure.
"""
from acl.api.access import Access
from acl.core.spec import IAclPermissionProvider
from ally.container.ioc import injected
from ally.design.processor.attribute import defines, requires
from ally.design.processor.context import Context
from ally.design.processor.handler import HandlerProcessor
from collections import Iterable
import itertools

class Solicit(Context):
    """
    The solicit context.
    """
    permissions = defines(Iterable, doc='\n    @rtype: Iterable(Context)\n    The ACL permissions.\n    ')
    acl = requires(object)


class PermissionAcl(Context):
    """
    The permission context.
    """
    access = defines(Access, doc='\n    @rtype: Access\n    The ACL access associated with the permission.\n    ')
    filters = defines(dict, doc='\n    @rtype: dictionary{object: tuple(dictionary{integer:list[string]}, dictionary{string:list[string]})}\n    The filters dictionary contains:\n        identifier: (filter paths for entries indexed by entry position, filter paths for properties indexed by property name)\n    ')


@injected
class RegisterAclPermissionHandler(HandlerProcessor):
    """
    Provides the handler that adds the permissions based on ACL structure.
    """
    aclPermissionProvider = IAclPermissionProvider

    def __init__(self):
        assert isinstance(self.aclPermissionProvider, IAclPermissionProvider), 'Invalid ACL permission provider %s' % self.aclPermissionProvider
        super().__init__()

    def process(self, chain, solicit: Solicit, Permission: PermissionAcl, **keyargs):
        """
        @see: HandlerProcessor.process
        
        Adds the ACL access permissions.
        """
        assert isinstance(solicit, Solicit), 'Invalid reply %s' % solicit
        if solicit.acl is None:
            return
        else:
            permissions = self.iteratePermissions(solicit.acl, Permission)
            if solicit.permissions is not None:
                solicit.permissions = itertools.chain(solicit.permissions, permissions)
            else:
                solicit.permissions = permissions
            return

    def iteratePermissions(self, acl, Permission):
        """
        Iterate the permissions for the identifiers.
        """
        assert issubclass(Permission, PermissionAcl), 'Invalid permission class %s' % Permission
        for access, filters in self.aclPermissionProvider.iteratePermissions(acl):
            assert isinstance(access, Access), 'Invalid access %s' % access
            assert isinstance(filters, dict), 'Invalid filters %s' % filters
            yield Permission(access=access, filters=filters)