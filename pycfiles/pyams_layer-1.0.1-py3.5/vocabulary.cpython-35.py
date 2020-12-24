# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_layer/vocabulary.py
# Compiled at: 2020-02-21 07:39:56
# Size of source mod 2**32: 2200 bytes
"""PyAMS_layer.vocabulary module

This module provides vocabularies used to get skins lists.
"""
from zope.componentvocabulary.vocabulary import UtilityTerm, UtilityVocabulary
from pyams_layer.interfaces import BASE_SKINS_VOCABULARY_NAME, IPyAMSUserLayer, ISkin, USER_SKINS_VOCABULARY_NAME
from pyams_utils.request import check_request
from pyams_utils.vocabulary import vocabulary_config
__docformat__ = 'restructuredtext'

@vocabulary_config(name=BASE_SKINS_VOCABULARY_NAME)
class SkinsVocabulary(UtilityVocabulary):
    __doc__ = 'PyAMS skins vocabulary'
    interface = ISkin
    nameOnly = True

    def __init__(self, context, **kw):
        request = check_request()
        registry = request.registry
        translate = request.localizer.translate
        utils = [(name, translate(util.label)) for name, util in registry.getUtilitiesFor(self.interface)]
        self._terms = dict((title, UtilityTerm(name, title)) for name, title in utils)


@vocabulary_config(name=USER_SKINS_VOCABULARY_NAME)
class UserSkinsVocabulary(UtilityVocabulary):
    __doc__ = 'PyAMS custom users skins vocabulary'
    interface = ISkin
    nameOnly = True

    def __init__(self, context, **kw):
        request = check_request()
        registry = request.registry
        translate = request.localizer.translate
        utils = [(name, translate(util.label)) for name, util in registry.getUtilitiesFor(self.interface) if issubclass(util.layer, IPyAMSUserLayer)]
        self._terms = dict((title, UtilityTerm(name, title)) for name, title in utils)