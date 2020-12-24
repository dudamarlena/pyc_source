# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/Products/LinguaFace/patches.py
# Compiled at: 2010-11-30 09:59:25
from Products.Archetypes.BaseObject import BaseObject
from zope.component import adapts
from zope.interface import implements
from Acquisition import aq_inner, aq_parent
from OFS.ObjectManager import ObjectManager
_getOb = ObjectManager._getOb
_delOb = ObjectManager._delOb
_marker = []
from AccessControl import ClassSecurityInfo
from Products.LinguaPlone import permissions
from Products.LinguaPlone.config import KWARGS_TRANSLATION_KEY, RELATIONSHIP
from Products.LinguaPlone.I18NBaseObject import I18NBaseObject
from Products.CMFPlone.utils import _createObjectByType
from Products.CMFPlone.utils import isDefaultPage
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import base_hasattr
from plone.locking.interfaces import ILockable
from zope.interface import Interface, classImplements
from zope.app.traversing.adapters import Traverser
from interface import ITranslatable
from Products.Archetypes.utils import shasattr
security = ClassSecurityInfo()
security.declareProtected(permissions.View, 'getCanonicalPath')

def getCanonicalPath(self):
    """ Return a path going only through canonical folders.  """
    if base_hasattr(self.aq_inner.aq_parent, 'getCanonicalPath'):
        path = self.aq_inner.aq_parent.getCanonicalPath()
        path += (self.getCanonical().id,)
        return path
    else:
        return self.getCanonical().getPhysicalPath()


security.declareProtected(permissions.AccessContentsInformation, 'myGetTranslations')

def myGetTranslations(self):
    """ Return a table containting all the translations
    """
    languages = self.getTranslationLanguages()
    return [ self.getTranslation(language) for language in languages ]


security.declareProtected(permissions.AccessContentsInformation, 'getOtherTranslations')

def getOtherTranslations(self):
    """ Return a table containting all the translations
    """
    languages = self.getTranslationLanguages()
    languages.remove(self.getLanguage())
    return [ self.getTranslation(language) for language in languages ]


security.declareProtected(permissions.AddPortalContent, 'newAddTranslation')

def newAddTranslation(self, language, *args, **kwargs):
    """Add a translation patched for LinguaFace events handlers
       Just add a '_v__dont_move_translations__' volatile attribute
       when moving contents during folder translations."""
    canonical = self.getCanonical()
    parent = aq_parent(aq_inner(self))
    req = getattr(self, 'REQUEST', None)
    if ITranslatable.providedBy(parent):
        parent = parent.getTranslation(language) or parent
    if self.hasTranslation(language):
        translation = self.getTranslation(language)
        raise AlreadyTranslated, translation.absolute_url()
    id = canonical.getId()
    while not parent.checkIdAvailable(id):
        id = '%s-%s' % (id, language)

    kwargs[KWARGS_TRANSLATION_KEY] = canonical
    if kwargs.get('language', None) != language:
        kwargs['language'] = language
    o = _createObjectByType(self.portal_type, parent, id, *args, **kwargs)
    if o.getCanonical() != canonical:
        o.addTranslationReference(canonical)
    self.invalidateTranslationCache()
    schema = canonical.Schema()
    independent_fields = schema.filterFields(languageIndependent=True)
    for field in independent_fields:
        accessor = field.getEditAccessor(canonical)
        if not accessor:
            accessor = field.getAccessor(canonical)
        data = accessor()
        translation_mutator = getattr(o, field.translation_mutator)
        translation_mutator(data)

    if self.isPrincipiaFolderish:
        moveids = []
        for obj in self.objectValues():
            if ITranslatable.providedBy(obj) and obj.getLanguage() == language:
                lockable = ILockable(obj, None)
                if lockable is not None and lockable.can_safely_unlock():
                    lockable.unlock()
                moveids.append(obj.getId())

        if moveids:
            o._v__dont_move_translations__ = True
            o.manage_pasteObjects(self.manage_cutObjects(moveids))
            delattr(o, '_v__dont_move_translations__')
    o.reindexObject()
    if isDefaultPage(canonical, self.REQUEST):
        o._lp_default_page = True
    return


security.declareProtected(permissions.ModifyPortalContent, 'newSetLanguage')

def newSetLanguage(self, value, **kwargs):
    """Sets the language code .

    When changing the language in a translated folder structure,
    we try to move the content to the existing language tree.

    Method patched for LinguaFace events handlers
    Just add a '_v__dont_move_translations__' volatile attribute
    when moving contents during folder translations.

    """
    translation = self.getTranslation(value)
    if self.hasTranslation(value):
        if translation == self:
            return
        else:
            raise AlreadyTranslated, translation.absolute_url()
    self.getField('language').set(self, value, **kwargs)
    req = getattr(self, 'REQUEST', None)
    if shasattr(req, 'get'):
        if req.get('SCHEMA_UPDATE', None) is not None:
            return
    if not value:
        self.deleteReferences(RELATIONSHIP)
    parent = aq_parent(aq_inner(self))
    if ITranslatable.providedBy(parent):
        new_parent = parent.getTranslation(value) or parent
        if new_parent != parent:
            info = parent.manage_cutObjects([self.getId()])
            new_parent._v__dont_move_translations__ = True
            new_parent.manage_pasteObjects(info)
            delattr(new_parent, '_v__dont_move_translations__')
    self.reindexObject()
    self.invalidateTranslationCache()
    return


I18NBaseObject.getCanonicalPath = getCanonicalPath
I18NBaseObject.myGetTranslations = myGetTranslations
I18NBaseObject.getOtherTranslations = getOtherTranslations
I18NBaseObject.old_addTranslation = I18NBaseObject.addTranslation
I18NBaseObject.addTranslation = newAddTranslation
I18NBaseObject.old_setLanguage = I18NBaseObject.setLanguage
I18NBaseObject.setLanguage = newSetLanguage
classImplements(I18NBaseObject, ITranslatable)