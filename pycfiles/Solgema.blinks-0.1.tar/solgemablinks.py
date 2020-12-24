# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/Solgema/solgema/src/Solgema.blinks/Solgema/blinks/portlets/solgemablinks.py
# Compiled at: 2010-08-06 02:08:16
import urllib2, socket, sys
from zope.interface import implements
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base
from Acquisition import aq_base, aq_inner, aq_parent
from zope import schema
from zope.formlib import form
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone import utils
from plone.portlet.collection import PloneMessageFactory as _pmf
from Solgema.blinks.config import _

class ISolgemaBlinksPortlet(IPortletDataProvider):
    """A portlet which renders the links given by www.b-links.fr.
    """
    __module__ = __name__
    header = schema.TextLine(title=_pmf('Portlet header'), description=_pmf('Title of the rendered portlet'), required=False)
    key = schema.TextLine(title=_('label_blinks_key'), description=_('description_blinks_key'), required=True)
    urls = schema.Text(title=_('label_blinks_urls'), description=_('description_blinks_urls'), required=True)


class Assignment(base.Assignment):
    __module__ = __name__
    implements(ISolgemaBlinksPortlet)
    header = ''
    key = ''
    urls = ''

    def __init__(self, header='', key='', urls=''):
        self.header = header
        self.key = key
        self.urls = urls

    @property
    def title(self):
        return self.header


class Renderer(base.Renderer):
    __module__ = __name__
    render = ViewPageTemplateFile('solgemablinks.pt')

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)
        self.blinks = self.isCurrentUrl() and self.getBLinks() or ''

    def getUrls(self):
        return [ str(a.replace('http://', '')) for a in self.data.urls.split('\n') ]

    def isCurrentUrl(self):
        parent = aq_inner(self.context)
        while utils.isDefaultPage(parent, self.request):
            parent = aq_parent(parent)

        if parent.absolute_url().replace('http://', '') in self.getUrls():
            return True
        return False

    @property
    def available(self):
        return len(self.blinks)

    def getBLinks(self):
        host = 'http://www.b-links.fr'
        key = self.data.key
        parent = aq_inner(self.context)
        while utils.isDefaultPage(parent, self.request):
            parent = aq_parent(parent)

        here_url = parent.absolute_url().replace('http://', '')
        timeout = 2
        socket.setdefaulttimeout(timeout)
        the_url = host + key + here_url
        req = urllib2.Request(the_url)
        try:
            handle = urllib2.urlopen(req)
        except:
            return ''

        the_page = handle.read()
        if the_page:
            the_page = '<ul>' + ('').join([ '<li>' + link + '</a></li>' for link in the_page.split('</a>') if link ]) + '</ul>'
        return the_page


class AddForm(base.AddForm):
    __module__ = __name__
    form_fields = form.Fields(ISolgemaBlinksPortlet)
    label = _('label_add_solgemablinks_portlet')
    description = _('This portlet display a listing of links given by www.b-links.fr. Please check www.b-links.fr to get all the infos.')

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    __module__ = __name__
    form_fields = form.Fields(ISolgemaBlinksPortlet)
    label = _('label_edit_solgemablinks_portlet')
    description = _('description_solgemablinks_portlet')