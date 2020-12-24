# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/weakpoint/main.py
# Compiled at: 2012-11-21 04:46:57
import sys
from weakpoint.core import WeakPoint
from weakpoint.exceptions import WeakPointException

def main():
    try:
        WeakPoint()
    except WeakPointException, e:
        print e
        return e.code

    return 0


if __name__ == '__main__':
    sys.exit(main())