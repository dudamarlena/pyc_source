# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/plone/multilingual/subscriber.py
# Compiled at: 2013-10-15 20:25:17
from Acquisition import aq_parent
from Products.CMFCore.interfaces import IFolderish
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import IPloneSiteRoot
from plone.multilingual.interfaces import LANGUAGE_INDEPENDENT
from plone.multilingual.interfaces import ILanguage
from plone.multilingual.interfaces import IMutableTG
from plone.multilingual.interfaces import ITranslationManager
from plone.multilingual.interfaces import ITranslatable
from zope.component.hooks import getSite
from zope.lifecycleevent import modified
from zope.lifecycleevent.interfaces import IObjectRemovedEvent
from plone.multilingual.interfaces import ITranslationCloner

def remove_translation_on_delete(obj, event):
    """ Deprecated """
    pass


def update_on_modify(obj, event):
    """ Deprecated """
    pass


def reindex_object(obj):
    obj.reindexObject(idxs=('Language', 'TranslationGroup', 'path', 'allowedRolesAndUsers'))


def set_recursive_language(obj, language):
    """ Set the language at this object and recursive
    """
    if ILanguage(obj).get_language() != language:
        ILanguage(obj).set_language(language)
        ITranslationManager(obj).update()
        reindex_object(obj)
    if IFolderish.providedBy(obj):
        for item in obj.items():
            if ITranslatable.providedBy(item):
                set_recursive_language(item, language)


def createdEvent(obj, event):
    """ It can be a
        IObjectRemovedEvent - don't do anything
        IObjectMovedEvent
        IObjectAddedEvent
        IObjectCopiedEvent
    """
    if IObjectRemovedEvent.providedBy(event):
        return
    portal = getSite()
    language_tool = getToolByName(portal, 'portal_languages')
    parent = aq_parent(event.object)
    if language_tool.startNeutral() and ITranslatable.providedBy(obj):
        set_recursive_language(obj, LANGUAGE_INDEPENDENT)
    elif IPloneSiteRoot.providedBy(parent) and ITranslatable.providedBy(obj) and ILanguage(obj).get_language() == LANGUAGE_INDEPENDENT:
        language = language_tool.getPreferredLanguage()
        set_recursive_language(obj, language)
    elif ITranslatable.providedBy(parent):
        language = ILanguage(parent).get_language()
        set_recursive_language(obj, language)
        sdm = obj.session_data_manager
        session = sdm.getSessionData()
        if 'tg' in session.keys() and not portal.portal_factory.isTemporary(obj):
            IMutableTG(obj).set(session['tg'])
            old_obj = ITranslationManager(obj).get_translation(session['old_lang'])
            cloner = ITranslationCloner(old_obj)
            cloner(obj)
            reindex_object(obj)
            del session['tg']