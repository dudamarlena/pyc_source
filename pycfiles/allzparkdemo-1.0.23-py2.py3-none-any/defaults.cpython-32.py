# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/__plugin__/gui_action/defaults.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Feb 23, 2012\n\n@package: ally actions gui \n@copyright: 2011 Sourcefabric o.p.s.\n@license:  http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Mihai Balaceanu\n'
from .service import addAction
from ally.container import ioc, app
from gui.action.api.action import Action

@ioc.entity
def menuAction():
    """
    Register default action name: menu
    This node should contain actions to be used to generate the top navigation menu 
    """
    return Action('menu')


@ioc.entity
def modulesAction():
    """
    Register default action name: modules
    This node should contain actions to be used inside the application 
    as main modules (whole page for edit/add/etc.)
    """
    return Action('modules')


@ioc.entity
def modulesDashboardAction():
    """
    Register default action name: modules.dashboard
    This node should contain actions to be used inside the dashboard of the application 
    as main modules (whole page for edit/add/etc.)
    """
    return Action('dashboard', Parent=modulesAction())


@app.deploy
def registerActions():
    """
    Register defined actions on the manager
    """
    addAction(menuAction())
    addAction(modulesAction())
    addAction(modulesDashboardAction())