# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/superdesk/security/core/impl/processor/user_rbac_provider.py
# Compiled at: 2013-10-02 09:54:57
"""
Created on Feb 21, 2013

@package: superdesk security
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Processor that adds default Gateway objects.
"""
from ally.api.operator.type import TypeProperty
from ally.container import wire
from ally.container.ioc import injected
from ally.container.support import setup
from ally.design.processor.attribute import defines, definesIf, requires
from ally.design.processor.context import Context
from ally.design.processor.execution import Chain
from ally.design.processor.handler import HandlerProcessor, Handler
from collections import Callable
from superdesk.security.core.spec import IUserRbacSupport
from superdesk.user.api.user import User

class Solicitation(Context):
    """
    The solicitation context.
    """
    userId = requires(int, doc='\n    @rtype: integer\n    The user id to create gateways for.\n    ')
    rbacId = defines(int, doc='\n    @rtype: integer\n    The id of the rbac to create gateways for.\n    ')
    provider = definesIf(Callable, doc='\n    @rtype: callable(TypeProperty) -> string|None\n    Callable used for getting the authenticated value.\n    ')


@injected
@setup(Handler, name='userRbacProvider')
class UserRbacProvider(HandlerProcessor):
    """
    Provides the handler that extracts the rbac id for the user id.
    """
    userRbacSupport = IUserRbacSupport
    wire.entity('userRbacSupport')

    def __init__(self):
        assert isinstance(self.userRbacSupport, IUserRbacSupport), 'Invalid user rbac support %s' % self.userRbacSupport
        super().__init__()

    def process(self, chain, solicitation: Solicitation, **keyargs):
        """
        @see: HandlerProcessor.process
        
        Populate the rbac id.
        """
        assert isinstance(chain, Chain), 'Invalid chain %s' % chain
        assert isinstance(solicitation, Solicitation), 'Invalid solicitation %s' % solicitation
        assert isinstance(solicitation.userId, int), 'Invalid solicitation user id %s' % solicitation.userId
        solicitation.rbacId = self.userRbacSupport.rbacIdFor(solicitation.userId)
        if solicitation.rbacId is None:
            return
        else:
            if Solicitation.provider in solicitation:
                solicitation.provider = UserProvider(str(solicitation.userId))
            chain.proceed()
            return


class UserProvider:
    """
    Implementation for @see: IAuthenticatedProvider that provides the authenticated user id.
    """
    __slots__ = ('userId', )

    def __init__(self, userId):
        """
        Construct the provider for the user id.
        
        @param userId: string
            The user id.
        """
        assert isinstance(userId, str), 'Invalid user id %s' % userId
        self.userId = userId

    def __call__(self, propertyType):
        """
        Provide the value for the property type.
        """
        assert isinstance(propertyType, TypeProperty), 'Invalid property type %s' % propertyType
        if propertyType.parent.clazz == User or issubclass(propertyType.parent.clazz, User):
            return self.userId