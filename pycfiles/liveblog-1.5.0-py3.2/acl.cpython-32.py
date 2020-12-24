# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/__plugin__/superdesk_security/acl.py
# Compiled at: 2013-10-02 09:54:57
"""
Created on Jan 15, 2013

@package: superdesk security
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the acl setup.
"""
from ..acl import acl
from ..acl.gui import defaultRight, updateDefault
from acl.spec import Filter
from ally.container import ioc, support
from ally.support.util import ref
from gui.action.api.action import IActionManagerService
from superdesk.security.api.authentication import IAuthenticationService
from superdesk.security.api.filter_authenticated import Authenticated, IAuthenticatedFilterService
from superdesk.security.api.user_action import IUserActionService
from superdesk.user.api.user import User, IUserService

@ioc.entity
def filterAuthenticated() -> Filter:
    """
    Provides filtering for the authenticated user.
    """
    return Filter(1, Authenticated.Id, User.Id, support.entityFor(IAuthenticatedFilterService))


@ioc.replace(updateDefault)
def updateFilteredDefaults():
    defaultRight().allGet(IUserActionService, filter=filterAuthenticated())
    defaultRight().add(ref(IAuthenticationService).requestLogin, ref(IAuthenticationService).performLogin)
    defaultRight().add(ref(IUserService).getById, filter=filterAuthenticated())


@acl.setupAlternate
def updateAlternates():
    acl.aclAlternate(ref(IActionManagerService).getAll, ref(IUserActionService).getAll)