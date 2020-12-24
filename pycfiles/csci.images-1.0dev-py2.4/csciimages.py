# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/csci/images/portlets/csciimages.py
# Compiled at: 2009-09-02 08:29:12
from zope.interface import Interface
from zope.interface import implements
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from zope import schema
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from csci.images.portlets import csciimagesMessageFactory as _
from Products.CMFCore.utils import getToolByName
import random

class Icsciimages(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """
    __module__ = __name__
    portlet_title = schema.TextLine(title=_('Title'), description=_('The title of the portlet'), required=True, default=_('images'))
    image_folder = schema.TextLine(title=_('Image folder path from root'), description=_('master folder for images'), required=True, default=_('images'))
    images_number = schema.TextLine(title=_('Number of images to display'), description=_('number'), required=True)


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """
    __module__ = __name__
    implements(Icsciimages)
    image_folder = 'images'
    images_number = '5'
    portlet_title = 'images'

    def __init__(self, image_folder='', images_number='', portlet_title=''):
        self.image_folder = image_folder
        self.images_number = images_number
        self.portlet_title = portlet_title

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return 'CSCI Images'


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """
    __module__ = __name__
    render = ViewPageTemplateFile('csciimages.pt')

    def title(self):
        return self.data.portlet_title

    def getimages(self):
        urltool = getToolByName(self.context, 'portal_url')
        portal = urltool.getPortalObject()
        local_path = self.data.image_folder + '/'
        local_path += ('/').join(self.context.getPhysicalPath()[2:])
        local_path = local_path.lower()
        print local_path
        try:
            image_folder = portal.restrictedTraverse(str(local_path))
        except:
            return

        images_togo = []
        objects_avail = image_folder.contentValues()
        for obj in objects_avail:
            if obj.Type() == 'Image':
                images_togo.append(obj)

        random.shuffle(images_togo)
        return images_togo[:int(self.data.images_number)]


class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    __module__ = __name__
    form_fields = form.Fields(Icsciimages)

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    __module__ = __name__
    form_fields = form.Fields(Icsciimages)