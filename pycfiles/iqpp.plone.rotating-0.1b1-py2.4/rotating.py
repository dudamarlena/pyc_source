# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/iqpp/plone/rotating/portlets/rotating.py
# Compiled at: 2008-08-03 12:15:43
from zope.formlib import form
from zope.interface import implements
from zope import schema
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from iqpp.plone.rotating.config import _
from iqpp.plone.rotating.interfaces import IRotating

class IRotatingPortlet(IPortletDataProvider):
    """
    """
    __module__ = __name__
    name = schema.TextLine(title=_('Title'), description=_('The title of the portlet'), required=True, default='Title')
    path = schema.TextLine(title=_('Path To Folder'), description=_('The source folder.'), required=True, default='')
    limit = schema.Int(title=_('Number of objects to display'), description=_('How many objects to list.'), required=True, default=1)


class Assignment(base.Assignment):
    """
    """
    __module__ = __name__
    implements(IRotatingPortlet)

    def __init__(self, name='Rotating Objects', path='', limit=1):
        """
        """
        self.name = name
        self.path = path
        self.limit = limit

    @property
    def title(self):
        return _('Rotating')


class Renderer(base.Renderer):
    """
    """
    __module__ = __name__
    render = ViewPageTemplateFile('rotating.pt')

    def update(self):
        """
        """
        mtool = getToolByName(self.context, 'portal_membership')
        if mtool.checkPermission('Manage portal', self.context):
            self.isNoManager = False
        else:
            self.isNoManager = True

    def getRotatingObjects(self):
        """
        """
        path = self.data.path.encode('utf-8')
        obj = self.context.restrictedTraverse(path)
        return IRotating(obj).getItems(self.data.limit)

    def title(self):
        """
        """
        return self.data.name


class AddForm(base.AddForm):
    """
    """
    __module__ = __name__
    form_fields = form.Fields(IRotatingPortlet)
    label = _('Rotating Portlet')
    description = _('This portlet displays rotating objects.')

    def create(self, data):
        """
        """
        return Assignment(name=data.get('name', 'Title'), path=data.get('path', ''), limit=data.get('limit', 5))


class EditForm(base.EditForm):
    """
    """
    __module__ = __name__
    form_fields = form.Fields(IRotatingPortlet)
    label = _('Edit Rotating Portlet')
    description = _('This portlet displays rotating objects.')