# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/qtipy/utils.py
# Compiled at: 2014-05-14 17:14:44
from __future__ import unicode_literals
import logging, re, os, errno

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def find_packager():
    import sys
    frozen = getattr(sys, b'frozen', None)
    if not frozen:
        return
    else:
        if frozen in ('dll', 'console_exe', 'windows_exe'):
            return b'py2exe'
        else:
            if frozen in ('macosx_app', ):
                return b'py2app'
            if frozen is True:
                return True
            return b'<unknown packager: %r>' % (frozen,)

        return


pkg = find_packager()
if pkg == None:
    scriptdir = os.path.dirname(os.path.realpath(__file__))
elif pkg == True:
    scriptdir = os.path.dirname(sys.executable)
elif pkg == b'py2app':
    scriptdir = os.environ[b'RESOURCEPATH']
elif pkg == b'py2exe':
    scriptdir = os.path.dirname(str(sys.executable, sys.getfilesystemencoding()))