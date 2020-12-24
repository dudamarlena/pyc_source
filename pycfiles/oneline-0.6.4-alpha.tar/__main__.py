# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /cygdrive/c/Users/Nad/oneline/oneline/lib/lz4/nose-1.3.4-py2.7.egg/nose/__main__.py
# Compiled at: 2014-09-06 21:58:19
import sys
from nose.core import run_exit
if sys.argv[0].endswith('__main__.py'):
    sys.argv[0] = '%s -m nose' % sys.executable
run_exit()