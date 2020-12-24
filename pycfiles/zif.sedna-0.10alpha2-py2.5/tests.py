# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/zif/sedna/tests.py
# Compiled at: 2008-03-30 11:18:23
import doctest

def doTests():
    doctest.testfile('README.txt')
    doctest.testfile('README_sednaobject.txt')


if __name__ == '__main__':
    doTests()