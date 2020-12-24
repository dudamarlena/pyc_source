# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/sunflower/_poly.py
# Compiled at: 2009-01-12 20:14:59
from __future__ import division
__version__ = '$Revision: 49 $'
import sys

def _chunk(collection):
    return collection


def _substitute(text):
    return text


try:
    from poly import chunk, substitute
except ImportError:
    chunk = _chunk
    substitute = _substitute

def main(args=sys.argv[1:]):
    pass


if __name__ == '__main__':
    sys.exit(main())