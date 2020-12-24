# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/greenlight/tests.py
# Compiled at: 2010-10-17 14:49:43
import os.path
testfile = os.path.join(os.path.dirname(__file__), '..', 'README.rst')
if __name__ == '__main__':
    import doctest
    doctest.testfile(testfile)