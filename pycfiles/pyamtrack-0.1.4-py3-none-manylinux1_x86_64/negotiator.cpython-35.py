# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_i18n/negotiator.py
# Compiled at: 2020-02-20 11:01:05
# Size of source mod 2**32: 5611 bytes
__doc__ = 'PyAMS_i18n.negotiator module\n\nThis module defines a I18n negotiator utility, which is responsible of decoding browser\nsettings to extract preferred languages.\n\nIt also provides Pyramid request properties to set locale.\n'
from persistent import Persistent
from pyramid.interfaces import IRequest
from zope.container.contained import Contained
from zope.i18n.interfaces import INegotiator as IZopeNegotiator
from zope.i18n.locales import locales
from zope.interface import Interface, implementer
from zope.schema.fieldproperty import FieldProperty
from zope.traversing.interfaces import ITraversable
from pyams_i18n.interfaces import INegotiator, LANGUAGE_CACHE_KEY
from pyams_utils.adapter import ContextRequestAdapter, adapter_config
from pyams_utils.i18n import get_browser_language
from pyams_utils.registry import get_global_registry, query_utility, utility_config
__docformat__ = 'restructuredtext'

@implementer(INegotiator)
class Negotiator(Persistent, Contained):
    """Negotiator"""
    policy = FieldProperty(INegotiator['policy'])
    server_language = FieldProperty(INegotiator['server_language'])
    offered_languages = FieldProperty(INegotiator['offered_languages'])
    cache_enabled = FieldProperty(INegotiator['cache_enabled'])

    def __init__(self):
        self.server_language = 'en'

    def get_language(self, request):
        """See :intf:`INegotiator`"""
        if 'lang' in request.params:
            return request.params['lang']
        policies = self.policy.split(' --> ')
        for policy in policies:
            if policy == 'server':
                if self.server_language:
                    return self.server_language
            elif policy == 'session':
                if self.cache_enabled:
                    try:
                        cached = request.annotations[LANGUAGE_CACHE_KEY]
                        return cached
                    except AttributeError:
                        return self.server_language
                    except KeyError:
                        try:
                            session = request.session
                            lang = session.get('language')
                            if lang is not None:
                                request.annotations[LANGUAGE_CACHE_KEY] = lang
                                return lang
                        except (AttributeError, KeyError):
                            return self.server_language

                else:
                    try:
                        session = request.session
                        lang = session.get('language')
                        if lang is not None:
                            return lang
                    except AttributeError:
                        return self.server_language

            elif policy == 'browser':
                lang = get_browser_language(request)
                if lang is not None:
                    return lang

        return self.server_language

    @staticmethod
    def clear_cache(request):
        """Clear cached language value"""
        try:
            del request.annotations[LANGUAGE_CACHE_KEY]
        except KeyError:
            pass


@adapter_config(name='lang', context=(Interface, IRequest), provides=ITraversable)
class LangNamespaceTraverser(ContextRequestAdapter):
    """LangNamespaceTraverser"""

    def traverse(self, name, furtherpath=None):
        """Traverse to set request parameter to given language attribute"""
        if name != '*':
            self.request.GET['lang'] = name
        return self.context


def locale_negotiator(request):
    """Negotiate language based on server, browser, request and user settings

    Locale is extracted from request's "lang" parameter, from browser settings or from
    negotiator utility
    """
    negotiator = query_utility(INegotiator)
    if negotiator is not None:
        locale_name = negotiator.get_language(request)
    else:
        locale_name = get_browser_language(request)
    if not locale_name:
        registry = request.registry
        locale_name = registry.settings.get('pyramid.default_locale_name', 'en')
    if '-' in locale_name:
        locale_name = locale_name.split('-')[0]
    return locale_name


def get_locale(request):
    """Get zope.i18n "locale" attribute"""
    return locales.getLocale(request.locale_name)


@utility_config(provides=IZopeNegotiator)
class ZopeNegotiator:
    """ZopeNegotiator"""

    def getLanguage(self, langs, env):
        """Get current language negotiator"""
        return locale_negotiator(env)