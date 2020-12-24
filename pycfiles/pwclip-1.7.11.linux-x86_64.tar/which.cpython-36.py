# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pwclip/lib/system/which.py
# Compiled at: 2020-03-20 08:07:42
# Size of source mod 2**32: 375 bytes
"""which module to find executables"""
from os import X_OK, access, environ, name as osname
from os.path import abspath, join as pjoin

def which(prog):
    """which function like the linux 'which' program"""
    delim = ';' if osname == 'nt' else ':'
    for path in environ['PATH'].split(delim):
        if access(pjoin(path, prog), X_OK):
            return pjoin(abspath(path), prog)

    return ''