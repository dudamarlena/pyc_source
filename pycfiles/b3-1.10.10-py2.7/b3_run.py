# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\b3_run.py
# Compiled at: 2016-03-08 18:42:10
__author__ = 'ThorN'
__version__ = '1.2'
import sys
if sys.version_info >= (3, ):
    raise SystemExit('Sorry, cannot continue: B3 is not yet compatible with python version 3!')
if sys.version_info < (2, 7):
    raise SystemExit('Sorry, cannot continue: B3 is not compatible with python versions earlier than 2.7!')
import b3.run

def main():
    b3.run.main()


if __name__ == '__main__':
    main()