# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mrdon/dev/flask-async/venv/lib/python3.3/site-packages/flask/testsuite/deprecations.py
# Compiled at: 2014-01-20 12:41:11
# Size of source mod 2**32: 511 bytes
"""
    flask.testsuite.deprecations
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Tests deprecation support.

    :copyright: (c) 2014 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""
import flask, unittest
from flask.testsuite import FlaskTestCase, catch_warnings

class DeprecationsTestCase(FlaskTestCase):
    __doc__ = 'not used currently'


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(DeprecationsTestCase))
    return suite