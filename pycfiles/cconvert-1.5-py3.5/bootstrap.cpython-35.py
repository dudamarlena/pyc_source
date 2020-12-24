# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/cconvert/bootstrap.py
# Compiled at: 2014-03-24 22:48:34
# Size of source mod 2**32: 358 bytes
"""bootstrap.bootstrap: provides entry point main()."""
__version__ = '0.2.0'
import sys
from .stuff import Stuff

def main():
    print('Executing bootstrap version %s.' % __version__)
    print('List of argument strings: %s' % sys.argv[1:])
    print('Stuff and Boo():\n%s\n%s' % (Stuff, Boo()))


class Boo(Stuff):
    pass