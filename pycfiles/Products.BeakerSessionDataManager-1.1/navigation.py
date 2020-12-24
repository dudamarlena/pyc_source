# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/BastionZenoss/browser/portlets/navigation.py
# Compiled at: 2011-01-11 16:22:56
from zope import schema
from zope.formlib import form
from zope.interface import implements
from Acquisition import aq_get, aq_inner
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.portlet.static import PloneMessageFactory as _
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from Products.CMFCore.utils import getToolByName
GROUPS = ('main', 'classes', 'browseby', 'mgmt')

class INavigationPortlet(IPortletDataProvider):
    """  zentinel navigation portlet """
    __module__ = __name__
    title = schema.TextLine(title=_('Portlet Title'), description=_('The title of the portlet.'), required=True, default='Zentinel')
    base = schema.ASCIILine(title=_('Base URL'), description=_('The url of the Zentinel as dispatched via ZWindow.'), required=True, default='zentinel/show_window?url=/zport/dmd')
    enterprise = schema.Bool(title=_('Enterprise'), description=_('Indicate if this is Zenoss Enterprise rather than Zenoss Core'), required=False, default=False)
    additional = schema.Text(title=_('Additional Links'), description=_('Colon-delimited links, tagged on group,title,link - group is one of %s. For example main:More stuff:Devices/More' % (', ').join(GROUPS)), required=False, default='')


class Renderer(base.Renderer):
    """ Overrides static.pt in the rendering of the portlet. """
    __module__ = __name__
    render = ViewPageTemplateFile('navigation.pt')

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)

    @property
    def available(self):
        return True

    def site_url(self):
        return getToolByName(self.context, 'portal_url').getPortalObject().absolute_url()

    def additional(self):
        """
        return a dict of the additional groupings
        """
        results = {}
        text = self.data.additional
        if text:
            for line in text.split('\n'):
                for (group, title, anchor) in line.split(':'):
                    if not results.has_key(group):
                        results[group] = [{'title': title, 'link': anchor}]
                    else:
                        results[group].append({'title': title, 'link': anchor})

        return results

    def base(self):
        return '%s/%s' % (self.site_url(), self.data.base)

    def enterprise(self):
        return self.data.enterprise

    def title(self):
        """
        the title of the portlet
        """
        return self.data.title


class Assignment(base.Assignment):
    """ Assigner for portlet. """
    __module__ = __name__
    implements(INavigationPortlet)
    title = _('Zentinel Menus')

    def __init__(self, title, base, enterprise, additional):
        self.title = title
        self.base = base
        self.enterprise = enterprise
        self.additional = additional


class AddForm(base.AddForm):
    __module__ = __name__
    form_fields = form.Fields(INavigationPortlet)
    label = _('Add Zentinel Navigation Portlet')
    description = _('This portlet provides your zentinel menus.')

    def create(self, data):
        return Assignment(data.get('title', 'Zentinel'), data.get('base', ''), data.get('enterprise', False), data.get('additional', ''))


class EditForm(base.EditForm):
    __module__ = __name__
    form_fields = form.Fields(INavigationPortlet)
    label = _('Edit Zentinel Navigation Portlet')
    description = _('This portlet provides your zentinel menus.')