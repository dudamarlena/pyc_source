# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mrdon/dev/flask-async/venv/lib/python3.3/site-packages/flask/testsuite/appctx.py
# Compiled at: 2014-01-20 12:41:11
# Size of source mod 2**32: 3544 bytes
"""
    flask.testsuite.appctx
    ~~~~~~~~~~~~~~~~~~~~~~

    Tests the application context.

    :copyright: (c) 2014 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""
import flask, unittest
from flask.testsuite import FlaskTestCase

class AppContextTestCase(FlaskTestCase):

    def test_basic_url_generation(self):
        app = flask.Flask(__name__)
        app.config['SERVER_NAME'] = 'localhost'
        app.config['PREFERRED_URL_SCHEME'] = 'https'

        @app.route('/')
        def index():
            pass

        with app.app_context():
            rv = flask.url_for('index')
            self.assert_equal(rv, 'https://localhost/')

    def test_url_generation_requires_server_name(self):
        app = flask.Flask(__name__)
        with app.app_context():
            with self.assert_raises(RuntimeError):
                flask.url_for('index')

    def test_url_generation_without_context_fails(self):
        with self.assert_raises(RuntimeError):
            flask.url_for('index')

    def test_request_context_means_app_context(self):
        app = flask.Flask(__name__)
        with app.test_request_context():
            self.assert_equal(flask.current_app._get_current_object(), app)
        self.assert_equal(flask._app_ctx_stack.top, None)
        return

    def test_app_context_provides_current_app(self):
        app = flask.Flask(__name__)
        with app.app_context():
            self.assert_equal(flask.current_app._get_current_object(), app)
        self.assert_equal(flask._app_ctx_stack.top, None)
        return

    def test_app_tearing_down(self):
        cleanup_stuff = []
        app = flask.Flask(__name__)

        @app.teardown_appcontext
        def cleanup(exception):
            cleanup_stuff.append(exception)

        with app.app_context():
            pass
        self.assert_equal(cleanup_stuff, [None])
        return

    def test_app_tearing_down_with_previous_exception(self):
        cleanup_stuff = []
        app = flask.Flask(__name__)

        @app.teardown_appcontext
        def cleanup(exception):
            cleanup_stuff.append(exception)

        try:
            raise Exception('dummy')
        except Exception:
            pass

        with app.app_context():
            pass
        self.assert_equal(cleanup_stuff, [None])
        return

    def test_custom_app_ctx_globals_class(self):

        class CustomRequestGlobals(object):

            def __init__(self):
                self.spam = 'eggs'

        app = flask.Flask(__name__)
        app.app_ctx_globals_class = CustomRequestGlobals
        with app.app_context():
            self.assert_equal(flask.render_template_string('{{ g.spam }}'), 'eggs')

    def test_context_refcounts(self):
        called = []
        app = flask.Flask(__name__)

        @app.teardown_request
        def teardown_req(error=None):
            called.append('request')

        @app.teardown_appcontext
        def teardown_app(error=None):
            called.append('app')

        @app.route('/')
        def index():
            with flask._app_ctx_stack.top:
                with flask._request_ctx_stack.top:
                    pass
            self.assert_true(flask._request_ctx_stack.top.request.environ['werkzeug.request'] is not None)
            return ''

        c = app.test_client()
        c.get('/')
        self.assertEqual(called, ['request', 'app'])
        return


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(AppContextTestCase))
    return suite