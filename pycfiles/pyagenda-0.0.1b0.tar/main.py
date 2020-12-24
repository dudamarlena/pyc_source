# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyage/main.py
# Compiled at: 2015-12-21 16:57:02
import sys
from pyage import inject
from pyage.Computation import Computation
if __name__ == '__main__':
    inject.config = sys.argv[1]
    computation = Computation()
    computation.run()