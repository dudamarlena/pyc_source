# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/BastionBanking/browser/portlets/donate.py
# Compiled at: 2015-07-18 19:38:10
from zope import schema
from zope.interface import implements
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.portlet.static import PloneMessageFactory as _
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base
from Products.BastionBanking.config import MERCHANTTOOL

class IDonatePortlet(IPortletDataProvider):
    """  a Donations portlet """
    bms = schema.ASCIILine(title=_('Bastion Merchant Serice Id'), description=_("id of the BMS to use (we'll acquire it from here)."), required=True, default=MERCHANTTOOL)
    desc = schema.Text(title=_('User Message'), description=_('Any text to include in the portlet'), required=False, default='')
    donation = schema.ASCIILine(title=_('A minimum suggest donation amount'), description=_('Please include currency code!!'), required=True, default='USD 10.00')


class Renderer(base.Renderer):
    """ Overrides static.pt in the rendering of the portlet. """
    render = ViewPageTemplateFile('donate.pt')

    @property
    def available(self):
        return self._tool() is not None

    def suggestedAmount(self):
        """
       returns a suggested minimum amount to donate
       """
        return self.data.donation

    def merchantURL(self):
        """
        return the URL of the BMS processing any donation
        """
        tool = self._tool()
        if tool:
            return tool.absolute_url()
        return ''

    def referenceURL(self):
        """
        return the URL of the calling portlet
        """
        return self.context.absolute_url()

    def serviceIcon(self):
        """
        """
        tool = self._tool()
        if tool:
            return tool.serviceIcon()
        return ''

    def Description(self):
        """
        A site-defined message to display in the donations portlet
        """
        return self.data.desc

    def _tool(self):
        try:
            return getattr(self.context, self.data.bms)
        except:
            return

        return


class Assignment(base.Assignment):
    """ Assigner for Donations portlet. """
    implements(IDonatePortlet)
    title = _('Donations')

    def __init__(self, bms, donation, desc=''):
        self.bms = bms
        self.donation = donation
        self.desc = desc


class AddForm(base.AddForm):
    """ Make sure that add form creates instances of our custom portlet instead of the base class portlet. """
    form_fields = form.Fields(IDonatePortlet)
    label = _('Accept Donations Portlet')
    description = _('This portlet allows you to accept donations.')

    def create(self, data):
        return Assignment(bms=data.get('BMS', MERCHANTTOOL), donation=data.get('donation', 'USD 10.00'), desc=data.get('desc', ''))


class EditForm(base.EditForm):
    """ edit Donations portlet"""
    form_fields = form.Fields(IDonatePortlet)
    label = _('Edit Donations Portlet')
    description = _('This portlet allows you to accept donations.')