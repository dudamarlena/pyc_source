# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/Users/ant/code/dj/build/lib/python3.6/_bootlocale.py
# Compiled at: 2019-07-30 17:44:32
# Size of source mod 2**32: 1301 bytes
"""A minimal subset of the locale module used at interpreter startup
(imported by the _io module), in order to reduce startup time.

Don't import directly from third-party code; use the `locale` module instead!
"""
import sys, _locale
if sys.platform.startswith('win'):

    def getpreferredencoding(do_setlocale=True):
        return _locale._getdefaultlocale()[1]


else:
    try:
        _locale.CODESET
    except AttributeError:

        def getpreferredencoding(do_setlocale=True):
            import locale
            return locale.getpreferredencoding(do_setlocale)


    else:

        def getpreferredencoding(do_setlocale=True):
            assert not do_setlocale
            result = _locale.nl_langinfo(_locale.CODESET)
            if not result:
                if sys.platform == 'darwin':
                    result = 'UTF-8'
            return result