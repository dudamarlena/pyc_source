# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/brocaar/Work/Projects/Brocaar/Flask/flask-views/flask_views/tests/__init__.py
# Compiled at: 2012-02-23 14:56:55
import unittest2 as unittest

def suite():
    suite = unittest.TestSuite()
    for test in unittest.TestLoader().discover('.'):
        suite.addTest(test)

    return suite