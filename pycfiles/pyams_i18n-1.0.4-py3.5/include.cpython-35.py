# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_i18n/include.py
# Compiled at: 2020-02-20 11:01:05
# Size of source mod 2**32: 1157 bytes
"""PyAMS_i18n.include module

This module is used for Pyramid integration.
"""
from chameleon import PageTemplateFile
from pyams_i18n.tales import I18nExpr
__docformat__ = 'restructuredtext'

def include_package(config):
    """Pyramid package include"""
    config.add_translation_dirs('pyams_i18n:locales')
    from .negotiator import get_locale, locale_negotiator
    config.add_request_method(get_locale, 'locale', reify=True)
    config.set_locale_negotiator(locale_negotiator)
    config.scan()
    PageTemplateFile.expression_types['i18n'] = I18nExpr