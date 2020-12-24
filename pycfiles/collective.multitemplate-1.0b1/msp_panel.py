# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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