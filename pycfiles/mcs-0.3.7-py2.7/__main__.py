# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\mcs\__main__.py
# Compiled at: 2012-03-19 14:46:54
from . import Mcs

def main():
    mcs = Mcs()
    try:
        raise SystemExit(mcs.main())
    except KeyboardInterrupt:
        print '-- interrupted --'


if __name__ == '__main__':
    main()