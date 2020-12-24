# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: E:\work\capturemock\bin\capturemock.py
# Compiled at: 2019-04-10 04:51:47
# Size of source mod 2**32: 674 bytes
import site, os, sys

def removeSelfFromPath():
    binDir = os.path.normpath(os.path.dirname(os.path.abspath(__file__))).replace('/', '\\')
    for path in sys.path:
        if binDir == os.path.normpath(path).replace('/', '\\'):
            sys.path.remove(path)
            break


if os.name == 'nt':
    removeSelfFromPath()
elif __name__ == '__main__':
    from capturemock import commandline
    commandline()
else:
    del sys.modules['capturemock']
    from capturemock import *