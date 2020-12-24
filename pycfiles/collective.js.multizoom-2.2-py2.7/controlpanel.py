# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/collective/js/multizoom/controlpanel.py
# Compiled at: 2013-08-21 05:07:59
import logging
from zope import component
from zope import interface
from zope import schema
try:
    from zope.component.hooks import getSite
except ImportError:
    from zope.site.hooks import getSite

from plone.registry.interfaces import IRecordModifiedEvent
from plone.app.registry.browser import controlpanel as basepanel
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.i18nmessageid import MessageFactory
_ = MessageFactory('collective.js.multizoom')

class IMultizoomPrefs(interface.Interface):
    """Multizoom Prefs"""
    zoom_width = schema.Int(title=_('label_zoom_width', default='Zoom width'), default=300, required=True)
    zoom_height = schema.Int(title=_('label_zoom_height', default='Zoom height'), default=300, required=True)


class MultizoomControlPanelForm(basepanel.RegistryEditForm):
    schema = IMultizoomPrefs
    control_panel_view = '@@jquery-multizoom-controlpanel'


class MultizoomControlPanelView(basepanel.ControlPanelFormWrapper):
    form = MultizoomControlPanelForm
    index = ViewPageTemplateFile('controlpanel.pt')
    label = 'Multizoom settings'