# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/HelloBikeLibrary2/__init__.py
# Compiled at: 2020-03-13 04:56:34
# Size of source mod 2**32: 483 bytes
from HelloBikeLibrary2.request import Request
from HelloBikeLibrary2.version import VERSION
from HelloBikeLibrary2.common import Common
__version__ = VERSION

class HelloBikeLibrary(Request, Common):
    __doc__ = '\n\t\tHelloBikeLibrary 1.0\n\t'
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'


if __name__ == '__main__':
    pass