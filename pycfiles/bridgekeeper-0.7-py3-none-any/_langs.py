# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/bridgedb/_langs.py
# Compiled at: 2016-07-29 18:59:30
__doc__ = '_langs.py - Storage for information on installed language support.'
RTL_LANGS = ('ar', 'he', 'fa', 'gu_IN', 'ku')

def get_langs():
    """Return a list of two-letter country codes of translations which were
    installed (if we've already been installed).
    """
    return supported


supported = set(['ar', 'az', 'bg', 'ca', 'cs', 'cy', 'da', 'de', 'el', 'en', 'en_GB', 'en_US', 'eo', 'es', 'es_CL', 'eu', 'fa', 'fi', 'fr', 'fr_CA', 'gl', 'he', 'hr_HR', 'hu', 'id', 'it', 'ja', 'km', 'kn', 'ko', 'lv', 'mk', 'ms_MY', 'nb', 'nl', 'pl', 'pt', 'pt_BR', 'ro', 'ru', 'si_LK', 'sk', 'sk_SK', 'sl_SI', 'sq', 'sr', 'sv', 'ta', 'th', 'tr', 'uk', 'zh_CN', 'zh_TW'])