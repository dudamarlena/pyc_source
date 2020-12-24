# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ally/gateway/http/impl/processor/repository_captcha.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Jun 7, 2013\n\n@package: gateway service reCAPTCHA\n@copyright: 2011 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Gabriel Nistor\n\nProvides the gateway reCAPTCHA repository processor.\n'
from .respository import GatewayRepositoryHandler, Identifier
from ally.container.ioc import injected
from ally.design.processor.attribute import defines
from ally.design.processor.context import Context

class Gateway(Context):
    """
    The gateway context.
    """
    isWithCaptcha = defines(bool, doc='\n    @rtype: boolean\n    If True it means the gateway needs to be solved with captcha.\n    ')


@injected
class GatewayCaptchaRepositoryHandler(GatewayRepositoryHandler):
    """
    Extension for @see: GatewayRepositoryHandler that provides the service for captcha gateways.
    """

    def process(self, processing, Gateway: Gateway, **keyargs):
        """
        @see: GatewayRepositoryHandler.process
        """
        super().process(processing, Gateway=Gateway, **keyargs)

    def populate(self, identifier, obj):
        """
        @see: GatewayCaptchaRepositoryHandler.populate
        
        Provides the captcha mark.
        """
        assert isinstance(identifier, Identifier), 'Invalid identifier %s' % identifier
        assert isinstance(identifier.gateway, Gateway), 'Invalid gateway %s' % identifier.gateway
        identifier.gateway.isWithCaptcha = True
        return super().populate(identifier, obj)