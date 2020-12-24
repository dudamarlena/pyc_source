# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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