# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/superdesk/security/impl/user_action.py
# Compiled at: 2013-10-02 09:54:57
"""
Created on Feb 27, 2012

@package: superdesk security
@copyright 2011 Sourcefabric o.p.s.
@license http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Action manager implementation for user GUI actions. 
"""
from acl.right_action import RightAction
from acl.spec import TypeAcl
from ally.container import wire
from ally.container.ioc import injected
from ally.container.support import setup
from ally.design.processor.assembly import Assembly
from ally.design.processor.attribute import defines, requires
from ally.design.processor.context import Context
from ally.design.processor.execution import Processing, Chain
from collections import Iterable
from gui.action.api.action import IActionManagerService, Action
from gui.action.impl.action import processChildCount
from superdesk.security.api.user_action import IUserActionService

class Solicitation(Context):
    """
    The solicitation context.
    """
    userId = defines(int, doc='\n    @rtype: integer\n    The id of the user to create gateways for.\n    ')
    types = defines(Iterable, doc='\n    @rtype: Iterable(TypeAcl)\n    The ACL types to create gateways for.\n    ')


class Reply(Context):
    """
    The reply context.
    """
    rightsAvailable = requires(Iterable, doc='\n    @rtype: Iterable(RightAcl)\n    The rights that are available.\n    ')


@injected
@setup(IUserActionService, name='userActionService')
class IUserActionServiceAlchemy(IUserActionService):
    """
    Provides the implementation user GUI actions @see: IUserActionService.
    """
    actionManagerService = IActionManagerService
    wire.entity('actionManagerService')
    actionType = TypeAcl
    wire.entity('actionType')
    assemblyActiveRights = Assembly
    wire.entity('assemblyActiveRights')

    def __init__(self):
        assert isinstance(self.actionManagerService, IActionManagerService), 'Invalid action manager service %s' % self.actionManagerService
        assert isinstance(self.actionType, TypeAcl), 'Invalid acl action type %s' % self.actionType
        assert isinstance(self.assemblyActiveRights, Assembly), 'Invalid assembly rights %s' % self.assemblyActiveRights
        self._processing = self.assemblyActiveRights.create(solicitation=Solicitation, reply=Reply)

    def getAll(self, userId, path=None, origPath=None):
        """
        @see: IUserActionService.getAll
        """
        assert isinstance(userId, int), 'Invalid user id %s' % userId
        proc = self._processing
        assert isinstance(proc, Processing), 'Invalid processing %s' % proc
        solicitation = proc.ctx.solicitation()
        assert isinstance(solicitation, Solicitation), 'Invalid solicitation %s' % solicitation
        solicitation.userId = userId
        solicitation.types = (self.actionType,)
        chain = Chain(proc)
        chain.process(solicitation=solicitation, reply=proc.ctx.reply()).doAll()
        reply = chain.arg.reply
        assert isinstance(reply, Reply), 'Invalid reply %s' % reply
        if Reply.rightsAvailable not in reply:
            return ()
        actionPaths = set()
        for aclRight in reply.rightsAvailable:
            if isinstance(aclRight, RightAction):
                assert isinstance(aclRight, RightAction)
                for action in aclRight.actions():
                    assert isinstance(action, Action)
                    actionPaths.add(action.Path)

                continue

        actions = []
        for action in self.actionManagerService.getAll(path):
            if action.Path in actionPaths:
                actions.append(action)
                continue

        return processChildCount(actions)