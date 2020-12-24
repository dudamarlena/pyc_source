# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/i18n/tal/api.py
# Compiled at: 2013-04-19 05:58:36
from z3c.language.negotiator.interfaces import INegotiatorManager
from z3c.language.switch.interfaces import II18n
from zope.tales.interfaces import ITALESFunctionNamespace
from ztfy.i18n.interfaces import II18nManager, II18nManagerInfo, II18nAttributesAware
from ztfy.i18n.tal.interfaces import II18nTalesAPI
from zope.component import queryUtility
from zope.i18n import translate
from zope.interface import implements
from ztfy.utils import getParent

class I18nTalesAdapter(object):
    implements(II18nTalesAPI, ITALESFunctionNamespace)

    def __init__(self, context):
        self.context = context
        self._i18n = II18n(getParent(self.context, II18nAttributesAware), None)
        return

    def setEngine(self, engine):
        self.request = engine.vars['request']

    def __getattr__(self, attribute):
        if self._i18n is not None:
            value = self._i18n.queryAttribute(attribute, language=self.request.get('language'), request=self.request)
        else:
            value = getattr(self.context, attribute, '')
        if value is None:
            value = ''
        return value

    def translate(self):
        return translate(self.context, context=self.request)

    def langs(self):
        if self._i18n is not None:
            default_language = self._i18n.getDefaultLanguage()
            languages = self._i18n.getAvailableLanguages()
            return sorted(languages, key=lambda x: x == default_language and '__' or x)
        else:
            i18n = getParent(self.context, II18nManager)
            if i18n is not None:
                info = II18nManagerInfo(i18n)
                default_language = info.defaultLanguage
                return sorted(info.availableLanguages, key=lambda x: x == default_language and '__' or x)
            negotiator = queryUtility(INegotiatorManager)
            if negotiator is not None:
                default_language = negotiator.serverLanguage
                return sorted(negotiator.offeredLanguages, key=lambda x: x == default_language and '__' or x)
            return ('en', )

    def user_lang(self):
        if self._i18n is not None:
            return self._i18n.getPreferedLanguage()
        else:
            return 'en'

    def default_lang(self):
        if self._i18n is not None:
            return self._i18n.getDefaultLanguage()
        else:
            return 'en'