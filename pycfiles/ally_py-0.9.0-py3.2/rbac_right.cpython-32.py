# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/security/rbac/core/impl/processor/rbac_right.py
# Compiled at: 2013-10-02 09:54:40
"""
Created on Feb 21, 2013

@package: support acl
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Processor that populates the rights based on the RBAC structure.
"""
from acl.spec import TypeAcl
from ally.container import wire
from ally.container.ioc import injected
from ally.container.support import setup
from ally.design.processor.attribute import requires, defines
from ally.design.processor.context import Context
from ally.design.processor.handler import HandlerProcessorProceed, Handler
from collections import Iterable
from itertools import chain
from security.rbac.core.spec import IRbacSupport

class Solicitation(Context):
    """
    The solicitation context.
    """
    rbacId = requires(int, doc='\n    @rtype: integer\n    The id of the rbac to fetch the rights for.\n    ')
    types = requires(Iterable, doc='\n    @rtype: Iterable(TypeAcl)\n    The ACL types to provide rights for.\n    ')
    rights = defines(Iterable, doc='\n    @rtype: Iterable(RightAcl)\n    The default rights for the types.\n    ')


@injected
@setup(Handler, name='rbacPopulateRights')
class RbacPopulateRights(HandlerProcessorProceed):
    """
    Provides the handler that populates the rights based on RBAC structure.
    """
    rbacSupport = IRbacSupport
    wire.entity('rbacSupport')

    def __init__(self):
        assert isinstance(self.rbacSupport, IRbacSupport), 'Invalid rbac support %s' % self.rbacSupport
        super().__init__()

    def process(self, solicitation: Solicitation, **keyargs):
        """
        @see: HandlerProcessorProceed.process
        
        Populate the rights.
        """
        assert isinstance(solicitation, Solicitation), 'Invalid solicitation %s' % solicitation
        assert isinstance(solicitation.rbacId, int), 'Invalid rbac Id %s' % solicitation.rbacId
        allTypes, rights, types = {aclType.name:aclType for aclType in solicitation.types}, [], []
        for typeName, names in self.rbacSupport.iterateTypeAndRightsNames(solicitation.rbacId):
            aclType = allTypes.get(typeName)
            if not aclType:
                continue
            types.append(aclType)
            assert isinstance(aclType, TypeAcl)
            rights.extend(aclType.rightsFor(names))

        solicitation.types = types
        if solicitation.rights is not None:
            solicitation.rights = chain(solicitation.rights, rights)
        else:
            solicitation.rights = rights
        return