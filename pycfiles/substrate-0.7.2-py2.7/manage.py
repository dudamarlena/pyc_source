# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/substrate/data/manage.py
# Compiled at: 2012-02-03 19:38:43
import os, sys
LOCAL_SUBSTRATE_LIB_PATH = [
 os.path.join('.', 'local', 'substrate', 'lib')]
sys.path = LOCAL_SUBSTRATE_LIB_PATH + sys.path
from management import *
if __name__ == '__main__':
    run_command(__file__, globals())