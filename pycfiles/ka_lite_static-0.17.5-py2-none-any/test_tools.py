# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/cherrypy/cherrypy/test/test_tools.py
# Compiled at: 2018-07-11 18:15:31
"""Test the various means of instantiating and invoking tools."""
import gzip, sys, unittest
from cherrypy._cpcompat import BytesIO, copyitems, itervalues
from cherrypy._cpcompat import IncompleteRead, ntob, ntou, py3k, xrange
from cherrypy._cpcompat import bytestr, unicodestr
import time
timeout = 0.2
import types, cherrypy
from cherrypy import tools
europoundUnicode = ntou(b'\x80\xa3')
from cherrypy.test import helper

class ToolTests(helper.CPWebCase):

    def setup_server():
        myauthtools = cherrypy._cptools.Toolbox('myauth')

        def check_access(default=False):
            if not getattr(cherrypy.request, 'userid', default):
                raise cherrypy.HTTPError(401)

        myauthtools.check_access = cherrypy.Tool('before_request_body', check_access)

        def numerify():

            def number_it(body):
                for chunk in body:
                    for k, v in cherrypy.request.numerify_map:
                        chunk = chunk.replace(k, v)

                    yield chunk

            cherrypy.response.body = number_it(cherrypy.response.body)

        class NumTool(cherrypy.Tool):

            def _setup(self):

                def makemap():
                    m = self._merged_args().get('map', {})
                    cherrypy.request.numerify_map = copyitems(m)

                cherrypy.request.hooks.attach('on_start_resource', makemap)

                def critical():
                    cherrypy.request.error_response = cherrypy.HTTPError(502).set_response

                critical.failsafe = True
                cherrypy.request.hooks.attach('on_start_resource', critical)
                cherrypy.request.hooks.attach(self._point, self.callable)

        tools.numerify = NumTool('before_finalize', numerify)

        class NadsatTool:

            def __init__(self):
                self.ended = {}
                self._name = 'nadsat'

            def nadsat(self):

                def nadsat_it_up(body):
                    for chunk in body:
                        chunk = chunk.replace(ntob('good'), ntob('horrorshow'))
                        chunk = chunk.replace(ntob('piece'), ntob('lomtick'))
                        yield chunk

                cherrypy.response.body = nadsat_it_up(cherrypy.response.body)

            nadsat.priority = 0

            def cleanup(self):
                cherrypy.response.body = [
                 ntob('razdrez')]
                id = cherrypy.request.params.get('id')
                if id:
                    self.ended[id] = True

            cleanup.failsafe = True

            def _setup(self):
                cherrypy.request.hooks.attach('before_finalize', self.nadsat)
                cherrypy.request.hooks.attach('on_end_request', self.cleanup)

        tools.nadsat = NadsatTool()

        def pipe_body():
            cherrypy.request.process_request_body = False
            clen = int(cherrypy.request.headers['Content-Length'])
            cherrypy.request.body = cherrypy.request.rfile.read(clen)

        class Rotator(object):

            def __call__(self, scale):
                r = cherrypy.response
                r.collapse_body()
                if py3k:
                    r.body = [
                     bytes([ (x + scale) % 256 for x in r.body[0] ])]
                else:
                    r.body = [ chr((ord(x) + scale) % 256) for x in r.body[0] ]

        cherrypy.tools.rotator = cherrypy.Tool('before_finalize', Rotator())

        def stream_handler(next_handler, *args, **kwargs):
            cherrypy.response.output = o = BytesIO()
            try:
                response = next_handler(*args, **kwargs)
                return o.getvalue()
            finally:
                o.close()

        cherrypy.tools.streamer = cherrypy._cptools.HandlerWrapperTool(stream_handler)

        class Root:

            def index(self):
                return 'Howdy earth!'

            index.exposed = True

            def tarfile(self):
                cherrypy.response.output.write(ntob('I am '))
                cherrypy.response.output.write(ntob('a tarfile'))

            tarfile.exposed = True
            tarfile._cp_config = {'tools.streamer.on': True}

            def euro(self):
                hooks = list(cherrypy.request.hooks['before_finalize'])
                hooks.sort()
                cbnames = [ x.callback.__name__ for x in hooks ]
                assert cbnames == ['gzip'], cbnames
                priorities = [ x.priority for x in hooks ]
                assert priorities == [80], priorities
                yield ntou('Hello,')
                yield ntou('world')
                yield europoundUnicode

            euro.exposed = True

            def pipe(self):
                return cherrypy.request.body

            pipe.exposed = True
            pipe._cp_config = {'hooks.before_request_body': pipe_body}

            def decorated_euro(self, *vpath):
                yield ntou('Hello,')
                yield ntou('world')
                yield europoundUnicode

            decorated_euro.exposed = True
            decorated_euro = tools.gzip(compress_level=6)(decorated_euro)
            decorated_euro = tools.rotator(scale=3)(decorated_euro)

        root = Root()

        class TestType(type):
            """Metaclass which automatically exposes all functions in each
            subclass, and adds an instance of the subclass as an attribute
            of root.
            """

            def __init__(cls, name, bases, dct):
                type.__init__(cls, name, bases, dct)
                for value in itervalues(dct):
                    if isinstance(value, types.FunctionType):
                        value.exposed = True

                setattr(root, name.lower(), cls())

        Test = TestType('Test', (object,), {})

        class Demo(Test):
            _cp_config = {'tools.nadsat.on': True}

            def index(self, id=None):
                return 'A good piece of cherry pie'

            def ended(self, id):
                return repr(tools.nadsat.ended[id])

            def err(self, id=None):
                raise ValueError()

            def errinstream(self, id=None):
                yield 'nonconfidential'
                raise ValueError()
                yield 'confidential'

            def restricted(self):
                return 'Welcome!'

            restricted = myauthtools.check_access()(restricted)
            userid = restricted

            def err_in_onstart(self):
                return 'success!'

            def stream(self, id=None):
                for x in xrange(100000000):
                    yield str(x)

            stream._cp_config = {'response.stream': True}

        conf = {'/demo': {'tools.numerify.on': True, 
                     'tools.numerify.map': {ntob('pie'): ntob('3.14159')}}, 
           '/demo/restricted': {'request.show_tracebacks': False}, 
           '/demo/userid': {'request.show_tracebacks': False, 
                            'myauth.check_access.default': True}, 
           '/demo/errinstream': {'response.stream': True}, 
           '/demo/err_in_onstart': {'tools.numerify.map': 'pie->3.14159'}, 
           '/euro': {'tools.gzip.on': True, 
                     'tools.encode.on': True}, 
           '/decorated_euro/subpath': {'tools.gzip.priority': 10}, 
           '/tarfile': {'tools.streamer.on': True}}
        app = cherrypy.tree.mount(root, config=conf)
        app.request_class.namespaces['myauth'] = myauthtools
        if sys.version_info >= (2, 5):
            from cherrypy.test import _test_decorators
            root.tooldecs = _test_decorators.ToolExamples()

    setup_server = staticmethod(setup_server)

    def testHookErrors(self):
        self.getPage('/demo/?id=1')
        self.assertBody('A horrorshow lomtick of cherry 3.14159')
        time.sleep(0.1)
        self.getPage('/demo/ended/1')
        self.assertBody('True')
        valerr = '\n    raise ValueError()\nValueError'
        self.getPage('/demo/err?id=3')
        self.assertErrorPage(502, pattern=valerr)
        time.sleep(0.1)
        self.getPage('/demo/ended/3')
        self.assertBody('True')
        if cherrypy.server.protocol_version == 'HTTP/1.0' or getattr(cherrypy.server, 'using_apache', False):
            self.getPage('/demo/errinstream?id=5')
            self.assertStatus('200 OK')
            self.assertBody('nonconfidential')
        else:
            self.assertRaises((ValueError, IncompleteRead), self.getPage, '/demo/errinstream?id=5')
        time.sleep(0.1)
        self.getPage('/demo/ended/5')
        self.assertBody('True')
        self.getPage('/demo/restricted')
        self.assertErrorPage(401)
        self.getPage('/demo/userid')
        self.assertBody('Welcome!')

    def testEndRequestOnDrop(self):
        old_timeout = None
        try:
            httpserver = cherrypy.server.httpserver
            old_timeout = httpserver.timeout
        except (AttributeError, IndexError):
            return self.skip()

        try:
            httpserver.timeout = timeout
            self.persistent = True
            try:
                conn = self.HTTP_CONN
                conn.putrequest('GET', '/demo/stream?id=9', skip_host=True)
                conn.putheader('Host', self.HOST)
                conn.endheaders()
            finally:
                self.persistent = False

            time.sleep(timeout * 2)
            self.getPage('/demo/ended/9')
            self.assertBody('True')
        finally:
            if old_timeout is not None:
                httpserver.timeout = old_timeout

        return

    def testGuaranteedHooks(self):
        self.getPage('/demo/err_in_onstart')
        self.assertErrorPage(502)
        self.assertInBody("AttributeError: 'str' object has no attribute 'items'")

    def testCombinedTools(self):
        expectedResult = (ntou('Hello,world') + europoundUnicode).encode('utf-8')
        zbuf = BytesIO()
        zfile = gzip.GzipFile(mode='wb', fileobj=zbuf, compresslevel=9)
        zfile.write(expectedResult)
        zfile.close()
        self.getPage('/euro', headers=[
         ('Accept-Encoding', 'gzip'),
         ('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.7')])
        self.assertInBody(zbuf.getvalue()[:3])
        zbuf = BytesIO()
        zfile = gzip.GzipFile(mode='wb', fileobj=zbuf, compresslevel=6)
        zfile.write(expectedResult)
        zfile.close()
        self.getPage('/decorated_euro', headers=[('Accept-Encoding', 'gzip')])
        self.assertInBody(zbuf.getvalue()[:3])
        self.getPage('/decorated_euro/subpath', headers=[
         ('Accept-Encoding', 'gzip')])
        if py3k:
            self.assertInBody(bytes([ (x + 3) % 256 for x in zbuf.getvalue() ]))
        else:
            self.assertInBody(('').join([ chr((ord(x) + 3) % 256) for x in zbuf.getvalue()
                                        ]))

    def testBareHooks(self):
        content = 'bit of a pain in me gulliver'
        self.getPage('/pipe', headers=[
         (
          'Content-Length', str(len(content))),
         ('Content-Type', 'text/plain')], method='POST', body=content)
        self.assertBody(content)

    def testHandlerWrapperTool(self):
        self.getPage('/tarfile')
        self.assertBody('I am a tarfile')

    def testToolWithConfig(self):
        if not sys.version_info >= (2, 5):
            return self.skip('skipped (Python 2.5+ only)')
        self.getPage('/tooldecs/blah')
        self.assertHeader('Content-Type', 'application/data')

    def testWarnToolOn(self):
        try:
            cherrypy.tools.numerify.on
        except AttributeError:
            pass
        else:
            raise AssertionError('Tool.on did not error as it should have.')

        try:
            cherrypy.tools.numerify.on = True
        except AttributeError:
            pass
        else:
            raise AssertionError('Tool.on did not error as it should have.')


class SessionAuthTest(unittest.TestCase):

    def test_login_screen_returns_bytes(self):
        """
        login_screen must return bytes even if unicode parameters are passed.
        Issue 1132 revealed that login_screen would return unicode if the
        username and password were unicode.
        """
        sa = cherrypy.lib.cptools.SessionAuth()
        res = sa.login_screen(None, username=unicodestr('nobody'), password=unicodestr('anypass'))
        self.assertTrue(isinstance(res, bytestr))
        return