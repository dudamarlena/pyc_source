# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/collective/portlet/toc/tocportlet.py
# Compiled at: 2010-03-25 06:46:28
from zope.interface import implements
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base
from zope import schema
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from collective.portlet.toc import TocPortletMessageFactory as _
DEFAULT_TYPES = ('News Item', 'Document', 'Event')

class ITocPortlet(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """
    __module__ = __name__
    types = schema.Tuple(title=_('Types'), description=_('Types that trigger the Portlet to appear'), default=DEFAULT_TYPES, required=True, value_type=schema.Choice(vocabulary='plone.app.vocabularies.ReallyUserFriendlyTypes'))
    scan_anchors = schema.Bool(title=_('Scan Anchors'), description=_('Scan content anchors and add items to the toc'), default=True, required=True)


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """
    __module__ = __name__
    implements(ITocPortlet)

    def __init__(self, types=DEFAULT_TYPES, scan_anchors=True):
        self.types = types
        self.scan_anchors = scan_anchors

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return 'Toc Portlet'


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """
    __module__ = __name__
    render = ViewPageTemplateFile('tocportlet.pt')

    @property
    def available(self):
        if self.context.portal_type in self.data.types:
            if len(self.context.getRelatedItems()) > 0 or len(self.context.getBRefs()) > 0:
                return True
            else:
                return False
        else:
            return False

    def getRelatedItemsByType(self, type):
        related = self.context.getRefs()
        backRelated = self.context.getBRefs()
        result = []
        workflow = getToolByName(self, 'portal_workflow')
        member = getToolByName(self, 'portal_membership')
        for backItem in backRelated:
            if self.getTypeName(backItem.getPortalTypeName()) == self.getTypeName(type) and (not self.isPublishable(backItem) or workflow.getInfoFor(backItem, 'review_state') == 'published' or not member.isAnonymousUser()):
                result.append(backItem)

        for item in related:
            if self.getTypeName(item.getPortalTypeName()) == self.getTypeName(type) and (not self.isPublishable(item) or workflow.getInfoFor(item, 'review_state') == 'published' or not member.isAnonymousUser()):
                result.append(item)

        return self.uniq(result)

    def isPublishable(self, item):
        if item.getPortalTypeName() == 'File' or item.getPortalTypeName() == 'Image':
            return False
        else:
            return True

    def uniq(self, alist):
        set = {}
        return [ set.setdefault(e, e) for e in alist if e not in set ]

    def purgeTypes(self, types):
        names = []
        purged = []
        for item in types:
            if self.getTypeName(item) not in names:
                names.append(self.getTypeName(item))
                purged.append(item)

        return purged

    def getTypeName(self, type):
        if type == 'Document':
            name = 'Documents'
        elif type == 'Person':
            name = 'People and Organizations'
        elif type == 'Folder':
            name = 'Media'
        elif type == 'Event':
            name = 'Events'
        elif type == 'Work':
            name = 'Works'
        elif type == 'Organization':
            name = 'People and Organizations'
        elif type == 'Image':
            name = 'Image'
        else:
            name = 'Others'
        return name

    def getOrderedTypes(self):
        result = [
         'Event', 'Work', 'Person', 'Organization', 'Document', 'Folder']
        putils = getToolByName(self, 'plone_utils')
        types = putils.getUserFriendlyTypes()
        for item in types:
            if item not in result:
                result.append(item)

        purgedResult = self.purgeTypes(result)
        return purgedResult


class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    __module__ = __name__
    form_fields = form.Fields(ITocPortlet)

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    __module__ = __name__
    form_fields = form.Fields(ITocPortlet)