# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/plone/multilingual/interfaces.py
# Compiled at: 2013-10-15 10:29:21
from zope.interface import Interface, Attribute
LANGUAGE_INDEPENDENT = ''
ATTRIBUTE_NAME = '_plone.tg'
NOTG = 'notg'

class ILanguage(Interface):

    def get_language(self):
        """ return the contents language """
        pass

    def set_language(self):
        """ return the contents language """
        pass


class ITranslatable(Interface):
    """Marker interface for content types that support translation"""


class ITranslationFactory(Interface):
    """Adapts ITranslated and is capable of returning
       a translation clone to be added.
    """

    def __call__(language):
        """Create a clone of the context
           for translation to the given language
        """
        pass


class ITranslationLocator(Interface):
    """Find a parent folder for a translation.
       Adapts ITranslated.
    """

    def __call__(language):
        """Return a parent folder into which a new translation can be added"""
        pass


class ITranslationIdChooser(Interface):
    """Find a valid id for a translation
       Adapts ITranslated.
    """

    def __call__(parent, language):
        """ Return a valid id for the translation """
        pass


class ITranslationCloner(Interface):
    """Subscription adapters to perform various aspects of cloning an object.
       Allows componentisation of things like workflow history cloning.
       Adapts ITranslated.
    """

    def __call__(object):
        """Update the translation copy that is being constructed"""
        pass


class ITranslationManager(Interface):

    def add_translation(object, intid):
        """
        create the translated content and register the translation
        """
        pass

    def remove_translation(language):
        """
        remove translation if exists (unregister the translation)
        """
        pass

    def get_translation(language):
        """
        get translation (translated object) if exists
        """
        pass

    def get_restricted_translation(language):
        """
        get translation (translated object) if exists and permitted
        """
        pass

    def get_translations():
        """
        get all the translated objects (including the context)
        """
        pass

    def get_restricted_translations():
        """
        get all the translated objects (including the context) if permitted
        """
        pass

    def get_translated_languages():
        """
        get a list of the translated languages
        (language-code like 'en', 'it' etc. )
        """
        pass

    def register_translation(language, content):
        """
        register an existing content as translation
        for context
        """
        pass

    def update():
        """
        update the item registered in the canonical
        check that there aren't two translations on the same language
        (used for changing the contexts language)
        """
        pass

    def query_canonical():
        """
        query if there is an canonical for the context
        used for migration
        """
        pass


class ILanguageIndependentFieldsManager(Interface):
    context = Attribute('context', 'A translatable object')

    def copy_fields(translation):
        """ Copy language independent fields to translation."""
        pass


class IMutableTG(Interface):
    """Adapt an object to this interface to manage the TG of an object
    
    Be sure of what you are doing. TG is supposed to be stable and
    widely used
    """

    def get():
        """Return the TG of the context"""
        pass

    def set(tg):
        """Set the unique id of the context with the tg value.
        """
        pass


class ITG(Interface):
    """Abstract representation of a TG.

    Adapt an object to this interface to obtain its UUID. Adaptation will
    fail if the object does not have a TG (yet).
    """


class ICanonical(Interface):
    languages = Attribute('dictionary {LANG_KEY: UUID, ...}')

    def add_item(language, intid):
        """ """
        pass

    def remove_item(language):
        """ """
        pass

    def get_item(language):
        """ """
        pass

    def remove_item_by_language(language):
        """ """
        pass

    def remove_item_by_id(id):
        """ """
        pass

    def get_items():
        """ """
        pass

    def get_keys():
        """ """
        pass


class IMultilingualStorage(Interface):
    """ Stores the canonical objects at the portal_multilingual tool """

    def add_canonical(id, canonical):
        """ add canonical """
        pass

    def get_canonical(id):
        """ get canonical """
        pass

    def remove_canonical(id):
        """ remove canonical """
        pass

    def get_canonicals():
        """ get all canonicals """
        pass


class ICanonicalStorage(Interface):
    """ Deprecated in 0.2, for migration purposes only """

    def add_canonical(id, canonical):
        """ add canonical """
        pass

    def get_canonical(id):
        """ get canonical """
        pass

    def remove_canonical(id):
        """ remove canonical """
        pass