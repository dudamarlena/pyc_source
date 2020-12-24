# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_i18n/vocabulary.py
# Compiled at: 2020-02-20 11:01:05
# Size of source mod 2**32: 2899 bytes
"""PyAMS_i18n.vocabulary module

This module provides named vocabularies for offered and selected content languages.
"""
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from pyams_i18n.interfaces import CONTENT_LANGUAGES_VOCABULARY_NAME, II18nManager, INegotiator, OFFERED_LANGUAGES_VOCABULARY_NAME
from pyams_i18n.language import BASE_LANGUAGES
from pyams_utils.registry import query_utility
from pyams_utils.request import check_request
from pyams_utils.traversing import get_parent
from pyams_utils.vocabulary import vocabulary_config
__docformat__ = 'restructuredtext'
from pyams_i18n import _

@vocabulary_config(name=OFFERED_LANGUAGES_VOCABULARY_NAME)
class I18nOfferedLanguages(SimpleVocabulary):
    __doc__ = 'I18n offered languages vocabulary'

    def __init__(self, context=None):
        terms = []
        negotiator = query_utility(INegotiator)
        if negotiator is not None:
            translate = check_request().localizer.translate
            for lang in negotiator.offered_languages:
                terms.append(SimpleTerm(lang, title=translate(BASE_LANGUAGES.get(lang) or _('<unknown>'))))

        super(I18nOfferedLanguages, self).__init__(terms)


@vocabulary_config(name=CONTENT_LANGUAGES_VOCABULARY_NAME)
class I18nContentLanguages(SimpleVocabulary):
    __doc__ = 'I18n content languages vocabulary'

    def __init__(self, context):
        terms = []
        translate = check_request().localizer.translate
        negotiator = query_utility(INegotiator)
        if negotiator is not None:
            terms.append(SimpleTerm(negotiator.server_language, title=translate(BASE_LANGUAGES.get(negotiator.server_language))))
        manager = get_parent(context, II18nManager)
        if manager is not None:
            for lang in manager.languages:
                if negotiator is None or lang != negotiator.server_language:
                    terms.append(SimpleTerm(lang, title=translate(BASE_LANGUAGES.get(lang) or _('<unknown>'))))

        super(I18nContentLanguages, self).__init__(terms)