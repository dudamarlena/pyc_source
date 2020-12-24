# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mrdon/dev/flask-async/venv/lib/python3.3/site-packages/flask/testsuite/subclassing.py
# Compiled at: 2014-01-20 12:41:11
# Size of source mod 2**32: 1214 bytes
"""
    flask.testsuite.subclassing
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Test that certain behavior of flask can be customized by
    subclasses.

    :copyright: (c) 2014 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""
import flask, unittest
from logging import StreamHandler
from flask.testsuite import FlaskTestCase
from flask._compat import StringIO

class FlaskSubclassingTestCase(FlaskTestCase):

    def test_suppressed_exception_logging(self):

        class SuppressedFlask(flask.Flask):

            def log_exception(self, exc_info):
                pass

        out = StringIO()
        app = SuppressedFlask(__name__)
        app.logger_name = 'flask_tests/test_suppressed_exception_logging'
        app.logger.addHandler(StreamHandler(out))

        @app.route('/')
        def index():
            1 // 0

        rv = app.test_client().get('/')
        self.assert_equal(rv.status_code, 500)
        self.assert_in(b'Internal Server Error', rv.data)
        err = out.getvalue()
        self.assert_equal(err, '')


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(FlaskSubclassingTestCase))
    return suite