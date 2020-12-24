# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\seishub\core\scripts\runtests.py
# Compiled at: 2010-12-23 17:42:43
"""
SeisHub's test runner.

This script will run every test included into SeisHub.
"""
import doctest, sys, unittest

def main():
    doctest.testmod(sys.modules[__name__])
    unittest.main(module='seishub.core.test', defaultTest='getSuite')


if __name__ == '__main__':
    main()