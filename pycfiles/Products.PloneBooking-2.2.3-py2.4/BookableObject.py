# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\Products\PloneBooking\content\BookableObject.py
# Compiled at: 2008-11-19 15:29:17
"""
    PloneBooking: Bookable Object
"""
__version__ = '$Revision: 1.6 $'
__author__ = ''
__docformat__ = 'restructuredtext'
from types import DictionaryType
from zope.interface import implements
from AccessControl import ClassSecurityInfo
from DateTime import DateTime
from Globals import InitializeClass
from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName
try:
    from Products.LinguaPlone.public import *
except ImportError:
    from Products.Archetypes.public import *

from Products.PloneBooking.config import PROJECTNAME, I18N_DOMAIN
from Products.PloneBooking.content.schemata import BookableObjectSchema
from Products.PloneBooking.interfaces import IBookableObject

class BookableObject(BaseBTreeFolder):
    """
      Bookable Object is an object that can be booked ...
    """
    __module__ = __name__
    implements(IBookableObject)
    _at_rename_after_creation = True
    schema = BookableObjectSchema
    security = ClassSecurityInfo()

    def __len__(self):
        return 1

    security.declarePrivate('setDefaults')

    def setDefaults(self):
        """Set field values to the default values
        """
        BaseBTreeFolder.setDefaults(self)
        default_method = getattr(self, 'bookableobject_defaults', self.restrictedTraverse('@@defaultFieldValues', None))
        if default_method is not None:
            kwargs = default_method()
            if type(kwargs) is DictionaryType:
                self.edit(**kwargs)
        return

    security.declarePublic('getBookableObject')

    def getBookableObject(self):
        """Returns bookable object himself"""
        utool = getToolByName(self, 'portal_url')
        return self.restrictedTraverse(utool.getRelativeContentURL(self))

    security.declarePrivate('getTypeVocabulary')

    def getTypeVocabulary(self):
        """ Get a type list for the bookable object.
        """
        center_obj = self.getBookingCenter()
        return Vocabulary(center_obj.getTypeDisplayList(), self, I18N_DOMAIN)

    security.declarePrivate('getCategoryVocabulary')

    def getCategoryVocabulary(self):
        """ Get a category list for the bookable object.
        """
        center_obj = self.getBookingCenter()
        new_items = []
        dl = center_obj.getCategoryDisplayList()
        new_items.append(('', 'No category', 'label_no_category'))
        new_items.extend(dl.items())
        return Vocabulary(DisplayList(tuple(new_items)), self, I18N_DOMAIN)

    security.declareProtected(permissions.ModifyPortalContent, 'edit')

    def edit(self, **kwargs):
        """Alias for update()
        """
        self.update(**kwargs)

    security.declareProtected(permissions.View, 'CookedBody')

    def CookedBody(self, stx_level='ignored'):
        """CMF compatibility method
        """
        return self.getText()


registerType(BookableObject, PROJECTNAME)