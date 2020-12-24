# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/acl/impl/gateway_acl.py
# Compiled at: 2013-10-04 10:48:33
"""
Created on Aug 13, 2013

@package: gateway acl
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Implementation for the ACL group based gateways.
"""
from ..api.gateway_acl import IGatewayACLService
from ally.container import wire
from ally.container.ioc import injected
from ally.container.support import setup
from ally.design.processor.assembly import Assembly
from ally.design.processor.attribute import defines, requires
from ally.design.processor.context import Context
from ally.design.processor.execution import Processing, FILL_CLASSES
from collections import Iterable

class Solicit(Context):
    """
    The solicit context.
    """
    acl = defines(object, doc='\n    @rtype: Iterable(string)\n    The groups names to create gateways for.\n    ')
    gateways = requires(Iterable)


@injected
@setup(IGatewayACLService, name='gatewayACLService')
class GatewayACLService(IGatewayACLService):
    """
    Implementation for @see: IGatewayACLService that provides the ACL gateways.
    """
    assemblyGroupGateways = Assembly
    wire.entity('assemblyGroupGateways')

    def __init__(self):
        assert isinstance(self.assemblyGroupGateways, Assembly), 'Invalid assembly gateways %s' % self.assemblyGroupGateways
        self._processing = self.assemblyGroupGateways.create(solicit=Solicit)

    def getGateways(self, group):
        """
        @see: IGatewayACLService.getGateways
        """
        assert isinstance(group, str), 'Invalid group name %s' % group
        proc = self._processing
        assert isinstance(proc, Processing), 'Invalid processing %s' % proc
        solicit = proc.execute(FILL_CLASSES, solicit=proc.ctx.solicit(acl={group})).solicit
        assert isinstance(solicit, Solicit), 'Invalid solicit %s' % solicit
        return solicit.gateways or ()