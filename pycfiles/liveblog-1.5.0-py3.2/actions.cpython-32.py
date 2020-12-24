# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/__plugin__/superdesk_user/actions.py
# Compiled at: 2013-10-02 09:54:57
"""
Created on Feb 23, 2012

@package: ally actions gui 
@copyright: 2011 Sourcefabric o.p.s.
@license:  http://www.gnu.org/licenses/gpl-3.0.txt
@author: Mihai Balaceanu

Actions and acl action setups.
"""
from ..acl import gui
from ..gui_action import defaults
from ..gui_action.service import addAction
from ..gui_core.gui_core import publishedURI
from acl.right_action import RightAction
from ally.container import ioc, support
from ally.internationalization import NC_
from gui.action.api.action import Action
from superdesk.user.api.user import IUserService
support.listenToEntities(Action, listeners=addAction)
support.loadAllEntities(Action)

@ioc.entity
def menuAction() -> Action:
    return Action('user', Parent=defaults.menuAction(), Label=NC_('menu', 'Users'), NavBar='/users', Script=publishedURI('superdesk/user/scripts/js/menu.js'))


@ioc.entity
def modulesAction() -> Action:
    return Action('user', Parent=defaults.modulesAction())


@ioc.entity
def modulesUpdateAction() -> Action:
    return Action('update', Parent=modulesAction(), Script=publishedURI('superdesk/user/scripts/js/modules-update.js'))


@ioc.entity
def modulesListAction() -> Action:
    return Action('list', Parent=modulesAction(), Script=publishedURI('superdesk/user/scripts/js/list.js'))


@ioc.entity
def rightUserView() -> RightAction:
    return gui.actionRight(NC_('security', 'Users view'), NC_('security', '\n    Allows read only access to users.'))


@ioc.entity
def rightUserUpdate() -> RightAction:
    return gui.actionRight(NC_('security', 'Users update'), NC_('security', '\n    Allows the update of users.'))


@gui.setup
def registerAclUserView():
    r = rightUserView()
    r.addActions(menuAction(), modulesAction(), modulesListAction())
    r.allGet(IUserService)


@gui.setup
def registerAclUserUpdate():
    r = rightUserUpdate()
    r.addActions(menuAction(), modulesAction(), modulesListAction(), modulesUpdateAction())
    r.all(IUserService)