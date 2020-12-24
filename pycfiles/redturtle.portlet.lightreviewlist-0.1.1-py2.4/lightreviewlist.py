# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/redturtle/portlet/lightreviewlist/lightreviewlist.py
# Compiled at: 2009-09-14 07:03:04
from zope.interface import implements
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base
from zope import schema
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from redturtle.portlet.lightreviewlist import LightReviewListMessageFactory as _

class ILightReviewList(IPortletDataProvider):
    """A lighter review list portlet; it only display a link to full_review_list
    as normal review list portlet is someway slow and inefficent.
    """
    __module__ = __name__


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """
    __module__ = __name__
    implements(ILightReviewList)

    def __init__(self):
        pass

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return 'Light review list'


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """
    __module__ = __name__
    render = ViewPageTemplateFile('lightreviewlist.pt')

    @property
    def available(self):
        """Don't show anything if anon user"""
        return not getToolByName(self.context, 'portal_membership').isAnonymousUser()

    @property
    def portal_url(self):
        return getToolByName(self.context, 'portal_url').getPortalObject().absolute_url()


class AddForm(base.NullAddForm):
    """Portlet add form"""
    __module__ = __name__

    def create(self):
        return Assignment()