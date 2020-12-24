# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/acl/core/impl/processor/gateway/anonymous_group.py
# Compiled at: 2013-10-04 10:48:33
"""
Created on Aug 21, 2013

@package: gateway acl
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Processor that injects the anonymous groups identifiers.
"""
from acl.api.group import IGroupService, QGroup
from ally.container import wire
from ally.container.ioc import injected
from ally.container.support import setup
from ally.design.processor.attribute import defines
from ally.design.processor.context import Context
from ally.design.processor.handler import HandlerProcessor, Handler
from ally.design.processor.execution import Chain

class Solicit(Context):
    """
    The solicit context.
    """
    acl = defines(object, doc='\n    @rtype: Iterable(string)\n    The group names to create gateways for.\n    ')


@injected
@setup(Handler, name='anonymousGroup')
class AnonymousGroupHandler(HandlerProcessor):
    """
    Provides the handler that injects the anonymous groups for gateways.
    """
    groupService = IGroupService
    wire.entity('groupService')

    def __init__(self):
        assert isinstance(self.groupService, IGroupService), 'Invalid group service %s' % self.groupService
        super().__init__()

    def process(self, chain, solicit: Solicit, **keyargs):
        """
        @see: HandlerProcessor.process
        
        Inject the groups identifiers.
        """
        assert isinstance(chain, Chain), 'Invalid chain %s' % chain
        assert isinstance(solicit, Solicit), 'Invalid solicit %s' % solicit
        assert solicit.acl is None, 'There is already an acl object %s' % solicit.acl
        solicit.acl = list(self.groupService.getAll(q=QGroup(isAnonymous=True)))
        if not solicit.acl:
            chain.cancel()
        return