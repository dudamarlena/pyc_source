# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\testsuite.py
# Compiled at: 2011-12-15 09:20:39
import unittest, doctest
mods = []
for name in ['reader', 'writer', 'model', 'munger', 'filter', 'formatter', 'options']:
    parent = __import__('todopy.' + name)
    mods.append(getattr(parent, name))

def load_tests(loader, tests, ignore):
    for mod in mods:
        try:
            tests.addTests(doctest.DocTestSuite(mod))
        except ValueError:
            pass

    return tests