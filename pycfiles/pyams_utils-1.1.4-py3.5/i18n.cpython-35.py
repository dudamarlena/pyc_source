# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_utils/i18n.py
# Compiled at: 2020-02-18 19:11:13
# Size of source mod 2**32: 3201 bytes
"""PyAMS_utils.i18n module

This module is used to get browser language from request
"""
import locale
__docformat__ = 'restructuredtext'

def normalize_lang(lang):
    """Normalize input languages string

    >>> from pyams_utils.i18n import normalize_lang
    >>> lang = 'fr,en-US ; q=0.9, en-GB ; q=0.8, en ; q=0.7'
    >>> normalize_lang(lang)
    'fr,en-us;q=0.9,en-gb;q=0.8,en;q=0.7'
    """
    return lang.strip().lower().replace('_', '-').replace(' ', '')


def get_browser_language(request):
    """Custom locale negotiator

    Copied from zope.publisher code

    >>> from pyramid.testing import DummyRequest
    >>> from pyams_utils.i18n import get_browser_language

    >>> request = DummyRequest()
    >>> request.headers['Accept-Language'] = 'fr, en-US ; q=0.9, en-GB ; q=0.8, en ; q=0.7'
    >>> get_browser_language(request)
    'fr'
    """
    accept_langs = request.headers.get('Accept-Language', '').split(',')
    accept_langs = [normalize_lang(l) for l in accept_langs]
    accept_langs = [l for l in accept_langs if l]
    accepts = []
    for index, lang in enumerate(accept_langs):
        lang_item = lang.split(';', 2)
        quality = 1.0
        if len(lang_item) == 2:
            qual = lang_item[1]
            if qual.startswith('q='):
                qual = qual.split('=', 2)[1]
                try:
                    quality = float(qual)
                except ValueError:
                    continue

                if quality == 1.0:
                    quality = 1.9 - 0.001 * index
                accepts.append((quality, lang_item[0]))

    accepts = [acc for acc in accepts if acc[0]]
    accepts.sort()
    accepts.reverse()
    if accepts:
        return [lang for _, lang in accepts][0]


def set_locales(config):
    """Define locale environment variables

    :param config: Pyramid's settings object
    """
    for attr in ('LC_CTYPE', 'LC_COLLATE', 'LC_TIME', 'LC_MONETARY', 'LC_NUMERIC',
                 'LC_ALL'):
        value = config.get('pyams.locale.{0}'.format(attr.lower()))
        if value:
            locale.setlocale(getattr(locale, attr), value)