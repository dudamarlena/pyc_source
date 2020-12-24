# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bauble/gettext_windows.py
# Compiled at: 2016-08-05 01:29:02
"""Helper for standard gettext.py on Windows.

Module obtains user language code on Windows to use with standard
Python gettext.py library.

The module provides 2 functions: setup_env and get_language.

You may use setup_env before initializing gettext functions.

Or you can use get_language to get the list of language codes suitable
to pass them to gettext.find or gettext.translation function.

Usage example #1:

import gettext, gettext_windows
gettext_windows.setup_env()
gettext.install('myapp')

Usage example #2:

import gettext, gettext_windows
lang = gettext_windows.get_language()
translation = gettext.translation('myapp', languages=lang)
_ = translation.gettext
"""
import locale, os, sys
OS_WINDOWS = sys.platform == 'win32'

def setup_env_windows(system_lang=True):
    """Check environment variables used by gettext
    and setup LANG if there is none.
    """
    if _get_lang_env_var() is not None:
        return
    else:
        lang = get_language_windows(system_lang)
        if lang:
            os.environ['LANGUAGE'] = (':').join(lang)
        return


def get_language_windows(system_lang=True):
    """Get language code based on current Windows settings.
    @return: list of languages.
    """
    try:
        import ctypes
    except ImportError:
        return [locale.getdefaultlocale()[0]]

    lcid_user = ctypes.windll.kernel32.GetUserDefaultLCID()
    lcid_system = ctypes.windll.kernel32.GetSystemDefaultLCID()
    if system_lang and lcid_user != lcid_system:
        lcids = [
         lcid_user, lcid_system]
    else:
        lcids = [
         lcid_user]
    return filter(None, [ locale.windows_locale.get(i) for i in lcids ]) or None


def setup_env_other(system_lang=True):
    pass


def get_language_other(system_lang=True):
    lang = _get_lang_env_var()
    if lang is not None:
        return lang.split(':')
    else:
        return


def _get_lang_env_var():
    for i in ('LANGUAGE', 'LC_ALL', 'LC_MESSAGES', 'LANG'):
        lang = os.environ.get(i)
        if lang:
            return lang

    return


if OS_WINDOWS:
    setup_env = setup_env_windows
    get_language = get_language_windows
else:
    setup_env = setup_env_other
    get_language = get_language_other