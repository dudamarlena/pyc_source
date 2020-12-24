# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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