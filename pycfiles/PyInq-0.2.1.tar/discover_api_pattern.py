# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Auzzy\Documents\git\pyinq\examples\discover_api_pattern.py
# Compiled at: 2013-10-27 20:36:12
from pyinq import discover_tests
if __name__ == '__main__':
    suite = discover_tests('examples', 'assert*')
    if suite:
        print 'HERE'
        suite()