# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hanzo/warctools/log.py
# Compiled at: 2013-01-14 05:25:26
import sys
__all__ = ['debug']

def debug(*args):
    print >> sys.stderr, 'WARCTOOLS', args