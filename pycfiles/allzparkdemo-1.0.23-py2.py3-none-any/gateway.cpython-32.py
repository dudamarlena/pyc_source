# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/gateway/impl/gateway.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Jan 28, 2013\n\n@package: gateway\n@copyright: 2012 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Gabriel Nistor\n\nImplementation for the default anonymous gateway data.\n'
from ..api.gateway import IGatewayService
from ally.container import wire
from ally.container.ioc import injected
from ally.container.support import setup
from ally.design.processor.assembly import Assembly
from ally.design.processor.attribute import requires
from ally.design.processor.context import Context
from ally.design.processor.execution import Chain, Processing
from collections import Iterable

class Reply(Context):
    """
    The reply context.
    """
    gateways = requires(Iterable, doc='\n    @rtype: Iterable(Gateway)\n    The gateways.\n    ')


@injected
@setup(IGatewayService, name='gatewayService')
class GatewayService(IGatewayService):
    """
    Implementation for @see: IGatewayService that provides the default anonymous gateway data.
    """
    assemblyAnonymousGateways = Assembly
    wire.entity('assemblyAnonymousGateways')

    def __init__(self):
        assert isinstance(self.assemblyAnonymousGateways, Assembly), 'Invalid assembly gateways %s' % self.assemblyAnonymousGateways
        self._processing = self.assemblyAnonymousGateways.create(reply=Reply)

    def getAnonymous(self):
        """
        @see: IGatewayService.getAnonymous
        """
        proc = self._processing
        assert isinstance(proc, Processing), 'Invalid processing %s' % proc
        chain = Chain(proc)
        chain.process(reply=proc.ctx.reply()).doAll()
        reply = chain.arg.reply
        assert isinstance(reply, Reply), 'Invalid reply %s' % reply
        if Reply.gateways not in reply:
            return ()
        return reply.gateways