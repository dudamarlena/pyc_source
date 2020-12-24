# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/torchrs/__main__.py
# Compiled at: 2014-09-19 06:42:11
__author__ = 'Binh Vu <binh@toan2.com>'
import os, sys
from .resolver import Resolver
from .shell.shell import Shell

def log(s):
    print s


if __name__ == '__main__':
    composerPath = os.path.join(os.path.abspath('.'), 'composer.json')
    if not os.path.exists(composerPath):
        print 'composer.json not found'
        exit(0)
    if sys.argv[1] == 'install':
        if len(sys.argv) > 2 and sys.argv[2] == '--hard':
            Shell.call(['rm', '__init__.py'], log)
            Shell.call(['rm', '-rf', 'modules'], log)
        resolver = Resolver(composerPath)
        resolver.resolve()
    else:
        print 'not support yet'