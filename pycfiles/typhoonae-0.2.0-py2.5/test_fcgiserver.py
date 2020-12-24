# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/typhoonae/tests/test_fcgiserver.py
# Compiled at: 2010-12-12 04:36:57
"""Unit tests for the FastCGI server module."""
import StringIO, os, sys, tempfile, typhoonae.fcgiserver, unittest

class TestCase(unittest.TestCase):
    """Tests our FastCGI server module."""

    def setUp(self):
        """Loads the sample application."""
        app_root = os.path.join(os.path.dirname(__file__), 'sample')
        os.chdir(app_root)
        sys.path.insert(0, os.getcwd())

    def testServer(self):
        """Tests the main FastCGI server loop."""
        import fcgiapp

        class Options:
            debug_mode = False
            login_url = '/_ah/login'
            logout_url = '/_ah/logout'

        self.assertRaises(fcgiapp.error, typhoonae.fcgiserver.serve, typhoonae.getAppConfig(), Options())

    def testLoadModule(self):
        """Tries to load a CGI script."""
        handler_path = 'app.py'
        cgi_path = os.path.join(os.path.dirname(__file__), 'sample', handler_path)
        module_cache = {}
        typhoonae.fcgiserver.load_module(handler_path, cgi_path, module_cache)
        self.assertEqual(['app'], module_cache.keys())
        mod_obj = module_cache['app']
        typhoonae.fcgiserver.load_module(handler_path, cgi_path, module_cache)
        self.assertEqual(mod_obj, module_cache['app'])

    def testRunModule(self):
        """Tries to load and run a python module."""
        handler_path = 'app.py'
        cgi_path = os.path.join(os.path.dirname(__file__), 'sample', handler_path)

        def request(uri, method='GET'):
            """Fakes a get request."""
            buffer = StringIO.StringIO()
            sys.stdout = buffer
            os.environ['PATH_INFO'] = uri
            os.environ['REQUEST_METHOD'] = method
            typhoonae.fcgiserver.run_module(handler_path, cgi_path)
            sys.stdout = sys.__stdout__
            del os.environ['PATH_INFO']
            del os.environ['REQUEST_METHOD']
            return buffer

        buffer = request('/')
        assert buffer.getvalue().startswith('Status: 200 OK')
        buffer = request('/unknown')
        assert buffer.getvalue().startswith('Status: 404 Not Found')

    def testCGIHandlerChain(self):
        """Tests if our CGI handler chain works."""
        chain = typhoonae.fcgiserver.CGIHandlerChain(lambda x, y: True)
        fp = StringIO.StringIO()
        chain(fp, {})
        fp.close()

    def testCGIInAdapter(self):
        """Tests the FastCGI input strem adapter."""
        stdin = StringIO.StringIO('sample data\nfoobar')
        adapted_stdin = typhoonae.fcgiserver.CGIInAdapter(stdin)
        self.assertEqual('sample data\nfoobar', adapted_stdin.read())
        adapted_stdin.seek(0)
        self.assertEqual('sample data\n', adapted_stdin.readline())
        adapted_stdin.close()

    def testCGIOutAdapter(self):
        """Tests the FastCGI output strem adapter."""
        stdout = StringIO.StringIO()
        adapted_stdout = typhoonae.fcgiserver.CGIOutAdapter(stdout)
        adapted_stdout.write('foobar')
        adapted_stdout.flush()

        class BrokenFastCGIOutStream:

            def write(self, data):
                raise IOError

        stdout = BrokenFastCGIOutStream()
        adapted_stdout = typhoonae.fcgiserver.CGIOutAdapter(stdout)
        adapted_stdout.write('foobar')
        adapted_stdout.flush()