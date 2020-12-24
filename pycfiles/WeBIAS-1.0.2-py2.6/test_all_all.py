# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webias/gnosis/xml/pickle/test/test_all_all.py
# Compiled at: 2015-04-13 16:10:47
import os, sys
dpath = os.path.abspath('../../../..')
sys.path.insert(0, dpath)
from disthelper.find_python import get_python_verlist
for (exe, info) in get_python_verlist():
    os.system('%s test_all.py' % exe)