# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/myams/viewlet/toplinks/interfaces.py
# Compiled at: 2014-06-17 12:26:48
from zope.viewlet.interfaces import IViewlet, IViewletManager
from zope.schema import TextLine, List, Object, Dict
from ztfy.myams import _

class ITopLinksViewletManager(IViewletManager):
    """Top links viewlet manager interface"""
    pass


class ITopLinksMenu(IViewlet):
    """Top link menu"""
    css_class = TextLine(title=_('Menu CSS class'), required=False)
    label = TextLine(title=_('Menu label'))
    click_handler = TextLine(title=_('Menu click handler'))
    url = TextLine(title=_('Menu link location'))
    data = Dict(title=_('Menu data attributes'), key_type=TextLine(), value_type=TextLine())


class ITopLinksViewlet(IViewlet):
    """Top link viewlet"""
    label = TextLine(title=_('Main label'))
    dropdown_label = TextLine(title=_('Dropdown menu label'))
    css_class = TextLine(title=_('Main CSS class'))
    viewlets = List(title=_('Top links menus'), value_type=Object(schema=ITopLinksMenu))


class ITopTabsTab(IViewlet):
    """Top tabs tab"""
    css_class = TextLine(title=_('Tab CSS class'), required=False)
    label = TextLine(title=_('Tab label'))
    click_handler = TextLine(title=_('Tab click handler'))
    url = TextLine(title=_('Tab link location'))
    data = Dict(title=_('Tab data attributes'), key_type=TextLine(), value_type=TextLine())


class ITopTabsViewlet(IViewlet):
    """Top tabs viewlet"""
    label = TextLine(title=_('Main label'))
    css_class = TextLine(title=_('Main CSS class'))
    viewlets = List(title=_('Top tabs items'), value_type=Object(schema=ITopTabsTab))