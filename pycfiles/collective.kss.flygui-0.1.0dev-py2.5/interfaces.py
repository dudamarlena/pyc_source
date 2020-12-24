# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/collective/kss/flygui/browser/interfaces.py
# Compiled at: 2008-05-01 14:12:35
from zope.interface import directlyProvides
from zope.interface import Interface
from zope.schema import Tuple
from zope.schema import Choice
from zope.app.publisher.interfaces.browser import IMenuItemType
from zope.app.publisher.interfaces.browser import IBrowserMenu
from plone.app.portlets.portlets.navigation import INavigationPortlet as IBaseNavigationPortlet
from collective.kss.flygui import MessageFactory as _

class IContentMenuItem(Interface):
    """Special menu item type for Plone's content menu."""
    pass


directlyProvides(IContentMenuItem, IMenuItemType)

class IWorkflowMenu(IBrowserMenu):
    """The workflow menu.

    This gets its menu items from the list of possible transitions in
    portal_workflow.
    """
    pass


class IFolderCommands(Interface):
    """Interface for KSS Commands to deal with folder contents"""
    pass


class INavigationPortlet(IBaseNavigationPortlet):
    """Extended properties for extended navigation portlet
    """
    portalTypes = Tuple(title=_('Portal types'), description=_('Select portal types to show'), default=(), required=False, value_type=Choice(vocabulary='flygui.vocabulary.portal_types'))