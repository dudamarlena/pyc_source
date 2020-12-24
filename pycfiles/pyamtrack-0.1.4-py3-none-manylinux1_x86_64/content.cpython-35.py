# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_i18n/content.py
# Compiled at: 2020-02-20 11:01:05
# Size of source mod 2**32: 1447 bytes
__doc__ = 'PyAMS_i18n.content module\n\nThis module provides a single class which is an I18n "manager"; this mixin class is used to\nsupport setting of "offered" languages which will be usable for contents translations.\n'
from zope.interface import implementer
from zope.schema.fieldproperty import FieldProperty
from pyams_i18n.interfaces import II18nManager, INegotiator
from pyams_utils.registry import query_utility
__docformat__ = 'restructuredtext'

@implementer(II18nManager)
class I18nManagerMixin:
    """I18nManagerMixin"""
    languages = FieldProperty(II18nManager['languages'])

    def get_languages(self):
        """Get list of offered languages, including server language"""
        langs = []
        negotiator = query_utility(INegotiator)
        if negotiator is not None:
            langs.append(negotiator.server_language)
        langs.extend(sorted(filter(lambda x: x not in langs, self.languages or ())))
        return langs