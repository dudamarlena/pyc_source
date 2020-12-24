# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\Users\Auzzy\Documents\git\pyinq\examples\discover_api_pattern.py
# Compiled at: 2013-10-27 20:36:12
from pyinq import discover_tests
if __name__ == '__main__':
    suite = discover_tests('examples', 'assert*')
    if suite:
        print 'HERE'
        suite()