# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/collective/multisitepanel/browser/msp_panel.py
# Compiled at: 2010-08-05 07:14:13
import OFS.Folder
from zope import interface
from collective.multisitepanel.browser.interfaces import IMultiSitePanel
from Products.Five import BrowserView
from Products.Five.browser import pagetemplatefile
from collective.multisitepanel import MultisitePanelMessageFactory as _

class MultiSitePanel(OFS.Folder.Folder):
    __module__ = __name__
    interface.implements(IMultiSitePanel)

    def Title(self):
        return 'Multisite Panel'


class ControlPanelView(BrowserView):
    __module__ = __name__
    __call__ = pagetemplatefile.ViewPageTemplateFile('templates/msp_panel.pt')
    label = _('Multisite panel')

    def back_link(self):
        return dict(label=_('Up to Site Setup'), url=self.context.absolute_url() + '/plone_control_panel')