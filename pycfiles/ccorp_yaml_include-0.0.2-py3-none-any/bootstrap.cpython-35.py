# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/cconvert/bootstrap.py
# Compiled at: 2014-03-24 22:48:34
# Size of source mod 2**32: 358 bytes
__doc__ = 'bootstrap.bootstrap: provides entry point main().'
__version__ = '0.2.0'
import sys
from .stuff import Stuff

def main():
    print('Executing bootstrap version %s.' % __version__)
    print('List of argument strings: %s' % sys.argv[1:])
    print('Stuff and Boo():\n%s\n%s' % (Stuff, Boo()))


class Boo(Stuff):
    pass