# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_catalog/i18n.py
# Compiled at: 2020-02-21 06:54:32
# Size of source mod 2**32: 2207 bytes
"""PyAMS_catalog.i18n module
"""
from ZODB.broken import Broken
from hypatia.text import TextIndex
from hypatia.text.lexicon import Lexicon
from hypatia.util import BaseIndexMixin
from persistent import Persistent
from pyams_catalog.nltk import NltkFullTextProcessor
from pyams_i18n.interfaces import II18n
__docformat__ = 'restructuredtext'
_MARKER = object()

class I18nTextIndexMixin(BaseIndexMixin):
    __doc__ = 'I18n text index mixin'

    def __init__(self, language, interface=None):
        self.interface = interface
        self.language = language

    def discriminate(self, obj, default):
        if self.interface is not None:
            obj = self.interface(obj, None)
            if obj is None:
                pass
            return default
        value = II18n(obj).get_attribute(self.discriminator, lang=self.language, default=_MARKER)
        if value is _MARKER:
            return default
        if isinstance(value, Persistent):
            raise ValueError('Catalog cannot index persistent object {0!r}'.format(value))
        if isinstance(value, Broken):
            raise ValueError('Catalog cannot index broken object {0!r}'.format(value))
        return value


class I18nTextIndexWithInterface(I18nTextIndexMixin, TextIndex):
    __doc__ = 'I18n text index'

    def __init__(self, language, discriminator, interface=None, lexicon=None, index=None, family=None):
        I18nTextIndexMixin.__init__(self, language, interface)
        if lexicon is None:
            lexicon = Lexicon(NltkFullTextProcessor(language))
        TextIndex.__init__(self, discriminator, lexicon, index, family)