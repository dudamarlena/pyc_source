# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/__plugin__/administration/actions.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Feb 2, 2012\n\n@package: introspection request\n@copyright: 2011 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Mihai Balaceanu\n\nRegistered actions for request plugin\n'
from ..acl import gui
from ..gui_action import defaults
from ..gui_action.service import addAction
from ..gui_core.gui_core import publishedURI
from acl.right_action import RightAction
from admin.introspection.api.component import IComponentService
from admin.introspection.api.plugin import IPluginService
from admin.introspection.api.request import IRequestService
from ally.container import ioc, support
from ally.internationalization import NC_
from gui.action.api.action import Action
support.listenToEntities(Action, listeners=addAction)
support.loadAllEntities(Action)

@ioc.entity
def menuAction() -> Action:
    return Action('request', NC_('menu', 'Request'), Parent=defaults.menuAction(), NavBar='/api-requests', Script=publishedURI('superdesk/request/scripts/js/menu.js'))


@ioc.entity
def modulesAction() -> Action:
    return Action('request', Parent=defaults.modulesAction())


@ioc.entity
def modulesListAction() -> Action:
    return Action('list', Parent=modulesAction(), Script=publishedURI('superdesk/request/scripts/js/list.js'))


@ioc.entity
def rightRequestsInspection() -> RightAction:
    return gui.actionRight(NC_('security', 'Requests inspection'), NC_('security', '\n    Allows for the viewing of all possible requests that can be made on the REST server, also the plugins and components\n    that are part of the application are also visible.'))


@gui.setup
def registerAcl():
    r = rightRequestsInspection()
    r.addActions(menuAction(), modulesAction(), modulesListAction())
    r.allGet(IComponentService, IPluginService, IRequestService)