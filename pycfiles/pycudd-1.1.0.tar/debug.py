# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-armv7l/egg/pycuda/debug.py
# Compiled at: 2015-06-16 13:16:13
from __future__ import absolute_import
from __future__ import print_function
import pycuda.driver
pycuda.driver.set_debugging()
import sys
from optparse import OptionParser
parser = OptionParser(usage='usage: %prog [options] SCRIPT-TO-RUN [SCRIPT-ARGUMENTS]')
parser.disable_interspersed_args()
options, args = parser.parse_args()
if len(args) < 1:
    parser.print_help()
    sys.exit(2)
mainpyfile = args[0]
from os.path import exists
if not exists(mainpyfile):
    print('Error:', mainpyfile, 'does not exist')
    sys.exit(1)
sys.argv = args
exec compile(open(mainpyfile).read(), mainpyfile, 'exec')