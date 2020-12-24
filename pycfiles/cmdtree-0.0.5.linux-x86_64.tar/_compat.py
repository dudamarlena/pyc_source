# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/winkidney/.virtualenvs/side-project/lib/python2.7/site-packages/cmdtree/_compat.py
# Compiled at: 2016-08-27 23:01:35
import sys
WIN = sys.platform.startswith('win')

def get_filesystem_encoding():
    return sys.getfilesystemencoding() or sys.getdefaultencoding()


if WIN:

    def _get_argv_encoding():
        import locale
        return locale.getpreferredencoding()


else:

    def _get_argv_encoding():
        return getattr(sys.stdin, 'encoding', None) or get_filesystem_encoding()