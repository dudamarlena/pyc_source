# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bauble/i18n.py
# Compiled at: 2016-10-03 09:39:22
"""
The i18n module defines the _() function for creating translatable strings.

_() is added to the Python builtins so there is no reason to import
this module more than once in an application.  It is usually imported
in :mod:`bauble`
"""
import os, locale, gettext, bauble.paths as paths
from bauble import version_tuple
import bauble.gettext_windows
bauble.gettext_windows.setup_env()
__all__ = [
 '_']
TEXT_DOMAIN = 'bauble-%s' % ('.').join(version_tuple[0:2])
langs = []
lang_code, encoding = locale.getdefaultlocale()
if lang_code:
    langs = [lang_code]
language = os.environ.get('LANGUAGE', None)
if language:
    langs += language.split(':')
langs += ['en']
gettext.bindtextdomain(TEXT_DOMAIN, paths.locale_dir())
gettext.textdomain(TEXT_DOMAIN)
lang = gettext.translation(TEXT_DOMAIN, paths.locale_dir(), languages=langs, fallback=True)
_ = gettext.gettext
import __builtin__
__builtin__._ = gettext.gettext