# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/icsemantic/core/interfaces.py
# Compiled at: 2008-10-06 10:31:08
""" icsemantic.core interfaces.
"""
from zope import schema
from zope.interface import Interface
from zope.schema.fieldproperty import FieldProperty
from icsemantic.core.i18n import _

class IicSemanticSite(Interface):
    """ represents a platecom installation, should be a local site
        with local components installed
    """
    __module__ = __name__


class IicSemanticConfiglet(Interface):
    """ platecom configlet
    """
    __module__ = __name__


class IicSemanticManagementContentTypes(Interface):
    __module__ = __name__
    fallback_types = schema.List(title=_('Fallback Content Types'), required=False, default=[], description=_('Content Types with language fallback capabilities'), value_type=schema.Choice(vocabulary='icsemantic.content_types'))


class IicSemanticUserConfiguration(Interface):
    __module__ = __name__
    pref_languages = schema.List(title=_('Extra Language Configuration'), required=False, default=[], description=_('Alternative Languages'), value_type=schema.Choice(vocabulary='languages'))


class ILanguagesManager(Interface):
    """

    """
    __module__ = __name__

    def listCurrentUserLanguages(self):
        """
        """
        pass

    def listUserLanguages(self, user_id):
        """
        """
        pass

    def storeUserLanguages(self, user_id, languages):
        """
        """
        pass


class IMultilingualContentMarker(Interface):
    """ Marker para un ContentType que tiene
        getters multilingües
    """
    __module__ = __name__


class IMultilingualGettersMarker(Interface):
    """ Marker para un ContentType que tiene
        getters multilingües en lugar de los
        originales de archetypes
    """
    __module__ = __name__


class IContentTypesMultilingualPatcher(Interface):
    """ Utility para aplicar los parches de soporte multilenguaje
        a un ContentType en particular
    """
    __module__ = __name__

    def patch(self, klass):
        u""" Incorpora los metodos con fallback multilingüe
        """
        pass

    def unpatch(self, klass):
        u""" Remueve los metodos con fallback multilingüe
        """
        pass


class IFieldEmptiness(Interface):
    """ Emptiness adapter.
    """
    __module__ = __name__

    def __call__(self, instance):
        """
        """
        pass


class IicSemanticManageUserLanguages(Interface):
    """
        """
    __module__ = __name__
    icsemantic_preferred_languages = schema.List(title=_('User Languages'), required=False, default=[], description=_('User Languages'), value_type=schema.Choice(vocabulary='icsemantic.languages'))