# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/locale/locale_tool.py
# Compiled at: 2019-12-26 17:18:27
# Size of source mod 2**32: 1908 bytes
import locale
from contextlib import contextmanager
from future.utils import lmap
from foxylib.tools.string.string_tool import str2lower, str2upper

class LocaleTool:

    @classmethod
    def locale2lang(cls, locale):
        if not locale:
            return locale
        return cls.locale2lang_country(locale)[0]

    @classmethod
    def locale2country(cls, locale):
        if not locale:
            return locale
        return cls.locale2lang_country(locale)[1]

    @classmethod
    def locale2lang_country(cls, locale):
        if not locale:
            return (None, None)
        l = locale.split('-')
        return (str2lower(l[0]), str2upper(l[1]) if len(l) >= 2 else None)

    @classmethod
    def lang_country2locale(cls, lang, country):
        if not country:
            return lang
        return '-'.join([lang, country])

    @classmethod
    def locale2is_english(cls, locale):
        return cls.contains_lang(['en', None], locale)

    @classmethod
    def contains_lang(cls, locale_list, locale):
        for _locale in locale_list:
            lang_01, lang_02 = lmap(lambda x: str2lower(cls.locale2lang(x)), [locale, _locale])
            if lang_01 == lang_02:
                return True

        return False

    @classmethod
    def locale_pair2has_same_language(cls, locale1, locale2):
        lang1 = cls.locale2lang(locale1)
        lang2 = cls.locale2lang(locale2)
        return str2lower(lang1) == str2lower(lang2)