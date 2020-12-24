# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/gateway/core/impl/processor/method_override_gateway.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Feb 21, 2013\n\n@package: support acl\n@copyright: 2012 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Gabriel Nistor\n\nProcessor that adds default Gateway objects.\n'
from ally.container import wire
from ally.container.ioc import injected
from ally.container.support import setup
from ally.design.processor.attribute import defines
from ally.design.processor.context import Context
from ally.design.processor.handler import HandlerProcessorProceed, Handler
from ally.http.spec.server import HTTP_DELETE, HTTP_POST, HTTP_GET, HTTP_PUT
from ally.support.api.util_service import copy
from collections import Iterable
from gateway.api.gateway import Gateway

class Reply(Context):
    """
    The reply context.
    """
    gateways = defines(Iterable, doc='\n    @rtype: Iterable(Gateway)\n    The gateways to have the override method gateways populated.\n    ')


@injected
@setup(Handler, name='registerMethodOverride')
class RegisterMethodOverride(HandlerProcessorProceed):
    """
    Provides the method override gateways, basically support for @see: MethodOverrideHandler.
    """
    pattern_xmethod_override = 'X\\-HTTP\\-Method\\-Override\\:[\\s]*%s[\\s]*(?i)'
    wire.config('pattern_xmethod_override', doc="\n    The header pattern for the method override, needs to contain '%s' where the value will be placed.\n    ")
    methods_override = {HTTP_DELETE: [
                   HTTP_GET], 
     HTTP_PUT: [
                HTTP_POST]}
    wire.config('methods_override', doc='\n    A dictionary containing as a key the overrided method and as a value the methods that are overriden.\n    ')

    def __init__(self):
        """
        Construct the populate method override filter.
        """
        assert isinstance(self.pattern_xmethod_override, str), 'Invalid method override pattern %s' % self.pattern_xmethod_override
        assert isinstance(self.methods_override, dict), 'Invalid methods override %s' % self.methods_override
        super().__init__()

    def process(self, reply: Reply, **keyargs):
        """
        @see: HandlerProcessorProceed.process
        
        Adds the default gateways.
        """
        assert isinstance(reply, Reply), 'Invalid reply %s' % reply
        if reply.gateways is None:
            return
        else:
            reply.gateways = self.register(reply.gateways)
            return

    def register(self, gateways):
        """
        Register the method override gateways based on the provided gateways.
        """
        assert isinstance(gateways, Iterable), 'Invalid gateways %s' % gateways
        for gateway in gateways:
            assert isinstance(gateway, Gateway), 'Invalid gateway %s' % gateway
            yield gateway
            if not gateway.Methods:
                continue
            methods, overrides = set(), set()
            for method in gateway.Methods:
                override = self.methods_override.get(method)
                if override:
                    methods.add(method)
                    overrides.update(override)
                    continue

            if methods.union(overrides).issubset(gateway.Methods):
                continue
            ogateway = Gateway()
            copy(gateway, ogateway, exclude=('Methods', ))
            ogateway.Methods = list(overrides)
            if Gateway.Headers not in ogateway:
                ogateway.Headers = []
            for method in methods:
                ogateway.Headers.append(self.pattern_xmethod_override % method)

            yield ogateway