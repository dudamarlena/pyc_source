# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/plone/multilingual/manager.py
# Compiled at: 2013-10-15 10:29:21
from zope import interface
from zope.event import notify
from plone.uuid.interfaces import IUUID
from plone.multilingual.interfaces import ILanguage, ITranslationManager, ITranslationFactory, ITranslationLocator, ITG, IMutableTG, NOTG
from plone.multilingual.handlers import addAttributeTG
from plone.multilingual.events import ObjectWillBeTranslatedEvent, ObjectTranslatedEvent
from plone.uuid.handlers import addAttributeUUID
from plone.app.uuid.utils import uuidToObject
from zope.site.hooks import getSite
from Products.CMFCore.utils import getToolByName

class TranslationManager(object):
    interface.implements(ITranslationManager)

    def __init__(self, context):
        self.context = context
        if isinstance(context, str):
            self.tg = context
        else:
            self.tg = self.get_tg(context)
        self._canonical = None
        site = getSite()
        self.pcatalog = getToolByName(site, 'portal_catalog', None)
        return

    def get_id(self, context):
        """If an object is created via portal factory we don't get a id, we
           have to wait till the object is really created.
           TODO: a better check if we are in the portal factory!
        """
        try:
            context_id = IUUID(context)
        except KeyError:
            addAttributeUUID(context, None)
            context.reindexObject(idxs=['UID'])
            context_id = IUUID(context)

        return context_id

    def get_tg(self, context):
        """If an object is created via portal factory we don't get a id, we
           have to wait till the object is really created.
           TODO: a better check if we are in the portal factory!
        """
        try:
            context_id = ITG(context)
        except TypeError:
            addAttributeTG(context, None)
            context.reindexObject(idxs=['TranslationGroup'])
            context_id = ITG(context)

        return context_id

    def query_canonical(self):
        return self.tg

    def register_translation(self, language, content):
        """ register a translation for an existing content """
        if not language and language != '':
            raise KeyError('There is no target language')
        if type(content) == str:
            content_obj = uuidToObject(content)
        else:
            content_obj = content
        brains = self.pcatalog.unrestrictedSearchResults(TranslationGroup=self.tg, Language=language)
        if len(brains) > 0 and brains[0].UID != self.get_id(content_obj):
            raise KeyError('Translation already exists')
        IMutableTG(content_obj).set(self.tg)
        content_obj.reindexObject()

    def update(self):
        """ see interfaces"""
        language = ILanguage(self.context).get_language()
        brains = self.pcatalog.unrestrictedSearchResults(TranslationGroup=self.tg, Language=language)
        if len(brains) == 0:
            self.register_translation(language, self.context)
        else:
            brain = brains[0]
            content_id = self.get_id(self.context)
            if brain.UID != content_id:
                old_object = brain.getObject()
                IMutableTG(old_object).set(NOTG)
                old_object.reindexObject(idxs=('Language', 'TranslationGroup'))

    def add_translation(self, language):
        """ see interfaces """
        if not language and language != '':
            raise KeyError('There is no target language')
        notify(ObjectWillBeTranslatedEvent(self.context, language))
        translation_factory = ITranslationFactory(self.context)
        translated_object = translation_factory(language)
        ILanguage(translated_object).set_language(language)
        translated_object.reindexObject()
        self.register_translation(language, translated_object)
        notify(ObjectTranslatedEvent(self.context, translated_object, language))

    def add_translation_delegated(self, language):
        """
        Creation is delegated to factory/++add++
        Lets return the url where we are going to create the translation
        """
        if not language and language != '':
            raise KeyError('There is no target language')
        notify(ObjectWillBeTranslatedEvent(self.context, language))
        locator = ITranslationLocator(self.context)
        parent = locator(language)
        return parent

    def remove_translation(self, language):
        """ see interfaces """
        translation = self.get_translation(language)
        IMutableTG(translation).set(NOTG)
        translation.reindexObject()

    def get_translation(self, language):
        """ see interfaces """
        brains = self.pcatalog.unrestrictedSearchResults(TranslationGroup=self.tg, Language=language)
        if len(brains) != 1:
            return None
        else:
            return brains[0].getObject()

    def get_restricted_translation(self, language):
        """ see interfaces """
        brains = self.pcatalog.searchResults(TranslationGroup=self.tg, Language=language)
        if len(brains) != 1:
            return None
        else:
            return brains[0].getObject()

    def get_translations(self):
        """ see interfaces """
        translations = {}
        brains = self.pcatalog.unrestrictedSearchResults(TranslationGroup=self.tg)
        for brain in brains:
            translations[brain.Language] = brain.getObject()

        return translations

    def get_restricted_translations(self):
        """ see interfaces """
        translations = {}
        brains = self.pcatalog.searchResults(TranslationGroup=self.tg, Language='all')
        for brain in brains:
            translations[brain.Language] = brain.getObject()

        return translations

    def get_translated_languages(self):
        """ see interfaces """
        languages = []
        brains = self.pcatalog.unrestrictedSearchResults(TranslationGroup=self.tg)
        for brain in brains:
            if brain.Language not in languages:
                languages.append(brain.Language)

        return languages

    def has_translation(self, language):
        """ see interfaces """
        return language in self.get_translated_languages()