# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyage/main.py
# Compiled at: 2015-12-21 16:57:02
import sys
from pyage import inject
from pyage.Computation import Computation
if __name__ == '__main__':
    inject.config = sys.argv[1]
    computation = Computation()
    computation.run()