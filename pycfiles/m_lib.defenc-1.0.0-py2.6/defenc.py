# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/lib.linux-i686-2.6/m_lib/defenc.py
# Compiled at: 2017-04-16 07:58:41
"""Get default encoding"""
from __future__ import print_function
import sys
try:
    import locale
    use_locale = True
except ImportError:
    use_locale = False

__all__ = ['default_encoding']
if use_locale:
    try:
        lcAll = locale.getdefaultlocale()
    except locale.Error, err:
        print('WARNING:', err, file=sys.stderr)
        lcAll = []
    else:
        if len(lcAll) == 2 and lcAll[0] is not None:
            default_encoding = lcAll[1]
        else:
            try:
                default_encoding = locale.getpreferredencoding()
            except locale.Error, err:
                print('WARNING:', err, file=sys.stderr)
                default_encoding = sys.getdefaultencoding()

else:
    default_encoding = sys.getdefaultencoding()
default_encoding = default_encoding.lower()
if __name__ == '__main__':
    print(default_encoding)