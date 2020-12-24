# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mrdon/dev/flask-async/venv/lib/python3.3/site-packages/flask/testsuite/examples.py
# Compiled at: 2014-01-20 12:41:11
# Size of source mod 2**32: 942 bytes
"""
    flask.testsuite.examples
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Tests the examples.

    :copyright: (c) 2014 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""
import os, unittest
from flask.testsuite import add_to_path

def setup_path():
    example_path = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'examples')
    add_to_path(os.path.join(example_path, 'flaskr'))
    add_to_path(os.path.join(example_path, 'minitwit'))


def suite():
    setup_path()
    suite = unittest.TestSuite()
    try:
        from minitwit_tests import MiniTwitTestCase
    except ImportError:
        pass
    else:
        suite.addTest(unittest.makeSuite(MiniTwitTestCase))
    try:
        from flaskr_tests import FlaskrTestCase
    except ImportError:
        pass
    else:
        suite.addTest(unittest.makeSuite(FlaskrTestCase))
    return suite