# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pwclip/lib/system/which.py
# Compiled at: 2020-03-20 08:07:42
# Size of source mod 2**32: 375 bytes
__doc__ = 'which module to find executables'
from os import X_OK, access, environ, name as osname
from os.path import abspath, join as pjoin

def which(prog):
    """which function like the linux 'which' program"""
    delim = ';' if osname == 'nt' else ':'
    for path in environ['PATH'].split(delim):
        if access(pjoin(path, prog), X_OK):
            return pjoin(abspath(path), prog)

    return ''