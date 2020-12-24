# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/raymond/Documents/0x01.Source/twnews/build/lib/twnews/__init__.py
# Compiled at: 2019-02-13 20:13:05
# Size of source mod 2**32: 1112 bytes
"""
twnews 套件載入前作業，用來解決 Windows 環境會發生的編碼問題
"""
import sys, locale, _locale
if locale.getpreferredencoding() == 'cp950':
    _locale._getdefaultlocale = lambda *args: [
     'zh_TW', 'utf-8']
    VERSION = sys.version_info
    if VERSION.major == 3:
        if VERSION.minor == 5:
            NATIVE_PRINT = __builtins__['print']

            def _replaced_print(*objects, sep=' ', end='\n', file=sys.stdout, flush=False):
                """
            替換用的 print()
            """
                global NATIVE_PRINT
                filtered = []
                for obj in objects:
                    if isinstance(obj, str):
                        filtered.append(obj.encode('cp950', 'ignore').decode('cp950'))
                    else:
                        filtered.append(obj)

                NATIVE_PRINT(*filtered, sep=sep, end=end, file=file, flush=flush)


            __builtins__['print'] = _replaced_print