# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_i18n/content.py
# Compiled at: 2020-02-20 11:01:05
# Size of source mod 2**32: 1447 bytes
"""PyAMS_i18n.content module

This module provides a single class which is an I18n "manager"; this mixin class is used to
support setting of "offered" languages which will be usable for contents translations.
"""
from zope.interface import implementer
from zope.schema.fieldproperty import FieldProperty
from pyams_i18n.interfaces import II18nManager, INegotiator
from pyams_utils.registry import query_utility
__docformat__ = 'restructuredtext'

@implementer(II18nManager)
class I18nManagerMixin:
    __doc__ = 'I18n manager class mixin'
    languages = FieldProperty(II18nManager['languages'])

    def get_languages(self):
        """Get list of offered languages, including server language"""
        langs = []
        negotiator = query_utility(INegotiator)
        if negotiator is not None:
            langs.append(negotiator.server_language)
        langs.extend(sorted(filter(lambda x: x not in langs, self.languages or ())))
        return langs