# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/Products/UpfrontContacts/browser/contact.py
# Compiled at: 2010-03-10 13:47:43
from zope.interface import implements
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone import PloneMessageFactory as _

class IContactToolsPortlet(IPortletDataProvider):
    """A portlet that renders tools for importing, exporting and
       searching contacts
    """
    __module__ = __name__


class Assignment(base.Assignment):
    __module__ = __name__
    implements(IContactToolsPortlet)
    title = _('label_contact_tools', default='Contact Tools')


class Renderer(base.Renderer):
    """ Renderer for contact tools portlet
    """
    __module__ = __name__
    render = ViewPageTemplateFile('contacttools.pt')


class AddForm(base.NullAddForm):
    __module__ = __name__

    def create(self):
        return Assignment()