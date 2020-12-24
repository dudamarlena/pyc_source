# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/lib.linux-i686-2.6/m_lib/m_path.py
# Compiled at: 2016-07-25 12:05:26
from __future__ import print_function
_homedir = None

def get_homedir():
    global _homedir
    if _homedir is None:
        import sys, os
        _homedir = os.path.abspath(os.path.dirname(sys.argv[0]))
    return _homedir


def test():
    print(get_homedir())


if __name__ == '__main__':
    test()