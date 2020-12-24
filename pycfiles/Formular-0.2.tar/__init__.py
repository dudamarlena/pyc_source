# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dasich/projects/formular/docs/../formular/i18n/__init__.py
# Compiled at: 2010-03-09 18:13:13
"""
    formular.i18n
    ~~~~~~~~~~~~~

    Internationalization utilities used by Formular. This module is not part of
    the public api, therefore any of it's contents or the module itself may be
    changed or removed at any time.

    :copyright: 2010 by Formular Team, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""
from gettext import GNUTranslations, NullTranslations as NullTranslationsBase
from os import path
CATALOG_DIR = path.dirname(__file__)

class Translations(GNUTranslations):
    """
    A :class:`gettext.GNUTranslations` implementation which uses always
    unicode.
    """
    gettext = GNUTranslations.ugettext
    ngettext = GNUTranslations.ungettext

    def __init__(self, fileobj=None, locale=None):
        GNUTranslations.__init__(self, fileobj)
        self.locale = locale


class NullTranslations(NullTranslationsBase):
    """
    A :class:`gettext.NullTranslations` implementation which uses always
    unicode.
    """
    gettext = NullTranslationsBase.ugettext
    ngettext = NullTranslationsBase.ungettext

    def __init__(self, fileobj=None, locale=None):
        NullTranslationsBase.__init__(self, fileobj)
        self.locale = locale


def find_catalog(locale, domain='messages'):
    """
    Returns the path to the catalog or ``None``.

    .. note:: This works only for Formular.
    """
    catalog = path.join(CATALOG_DIR, locale, domain + '.mo')
    if path.isfile(catalog):
        return catalog


def get_translations(locale, domain='messages'):
    """
    Returns a :class:`Translations` instance for the given `locale` and
    `domain`. If no catalog is found a :class:`NullTranslations` instance
    is returned.
    """
    catalog = find_catalog(locale, domain)
    if catalog:
        with open(catalog) as (f):
            return Translations(f, locale=locale)
    return NullTranslations(locale=locale)


__all__ = [
 'Translations', 'NullTranslations', 'find_catalog',
 'get_translations']