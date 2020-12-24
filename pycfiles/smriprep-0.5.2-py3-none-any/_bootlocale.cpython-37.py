# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/src/smriprep/build/lib/python3.7/_bootlocale.py
# Compiled at: 2019-09-12 11:41:56
# Size of source mod 2**32: 1801 bytes
"""A minimal subset of the locale module used at interpreter startup
(imported by the _io module), in order to reduce startup time.

Don't import directly from third-party code; use the `locale` module instead!
"""
import sys, _locale
if sys.platform.startswith('win'):

    def getpreferredencoding(do_setlocale=True):
        if sys.flags.utf8_mode:
            return 'UTF-8'
        return _locale._getdefaultlocale()[1]


else:
    try:
        _locale.CODESET
    except AttributeError:
        if hasattr(sys, 'getandroidapilevel'):

            def getpreferredencoding(do_setlocale=True):
                return 'UTF-8'


        else:

            def getpreferredencoding(do_setlocale=True):
                if sys.flags.utf8_mode:
                    return 'UTF-8'
                import locale
                return locale.getpreferredencoding(do_setlocale)


    else:

        def getpreferredencoding(do_setlocale=True):
            if do_setlocale:
                raise AssertionError
            else:
                if sys.flags.utf8_mode:
                    return 'UTF-8'
                result = _locale.nl_langinfo(_locale.CODESET)
                if not result:
                    if sys.platform == 'darwin':
                        result = 'UTF-8'
            return result