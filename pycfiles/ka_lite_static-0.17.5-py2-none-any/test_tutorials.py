# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/cherrypy/cherrypy/test/test_tutorials.py
# Compiled at: 2018-07-11 18:15:31
import sys, cherrypy
from cherrypy.test import helper

class TutorialTest(helper.CPWebCase):

    def setup_server(cls):
        conf = cherrypy.config.copy()

        def load_tut_module(name):
            """Import or reload tutorial module as needed."""
            cherrypy.config.reset()
            cherrypy.config.update(conf)
            target = 'cherrypy.tutorial.' + name
            if target in sys.modules:
                module = reload(sys.modules[target])
            else:
                module = __import__(target, globals(), locals(), [''])
            app = cherrypy.tree.apps['']
            app.root.load_tut_module = load_tut_module
            app.root.sessions = sessions
            app.root.traceback_setting = traceback_setting
            cls.supervisor.sync_apps()

        load_tut_module.exposed = True

        def sessions():
            cherrypy.config.update({'tools.sessions.on': True})

        sessions.exposed = True

        def traceback_setting():
            return repr(cherrypy.request.show_tracebacks)

        traceback_setting.exposed = True

        class Dummy:
            pass

        root = Dummy()
        root.load_tut_module = load_tut_module
        cherrypy.tree.mount(root)

    setup_server = classmethod(setup_server)

    def test01HelloWorld(self):
        self.getPage('/load_tut_module/tut01_helloworld')
        self.getPage('/')
        self.assertBody('Hello world!')

    def test02ExposeMethods(self):
        self.getPage('/load_tut_module/tut02_expose_methods')
        self.getPage('/show_msg')
        self.assertBody('Hello world!')

    def test03GetAndPost(self):
        self.getPage('/load_tut_module/tut03_get_and_post')
        self.getPage('/greetUser?name=Bob')
        self.assertBody("Hey Bob, what's up?")
        self.getPage('/greetUser')
        self.assertBody('Please enter your name <a href="./">here</a>.')
        self.getPage('/greetUser?name=')
        self.assertBody('No, really, enter your name <a href="./">here</a>.')
        self.getPage('/greetUser', method='POST', body='name=Bob')
        self.assertBody("Hey Bob, what's up?")
        self.getPage('/greetUser', method='POST', body='name=')
        self.assertBody('No, really, enter your name <a href="./">here</a>.')

    def test04ComplexSite(self):
        self.getPage('/load_tut_module/tut04_complex_site')
        msg = '\n            <p>Here are some extra useful links:</p>\n\n            <ul>\n                <li><a href="http://del.icio.us">del.icio.us</a></li>\n                <li><a href="http://www.cherrypy.org">CherryPy</a></li>\n            </ul>\n\n            <p>[<a href="../">Return to links page</a>]</p>'
        self.getPage('/links/extra/')
        self.assertBody(msg)

    def test05DerivedObjects(self):
        self.getPage('/load_tut_module/tut05_derived_objects')
        msg = '\n            <html>\n            <head>\n                <title>Another Page</title>\n            <head>\n            <body>\n            <h2>Another Page</h2>\n\n            <p>\n            And this is the amazing second page!\n            </p>\n\n            </body>\n            </html>\n        '
        msg = msg.replace('</h2>\n\n', '</h2>\n        \n')
        msg = msg.replace('</p>\n\n', '</p>\n        \n')
        self.getPage('/another/')
        self.assertBody(msg)

    def test06DefaultMethod(self):
        self.getPage('/load_tut_module/tut06_default_method')
        self.getPage('/hendrik')
        self.assertBody('Hendrik Mans, CherryPy co-developer & crazy German (<a href="./">back</a>)')

    def test07Sessions(self):
        self.getPage('/load_tut_module/tut07_sessions')
        self.getPage('/sessions')
        self.getPage('/')
        self.assertBody("\n            During your current session, you've viewed this\n            page 1 times! Your life is a patio of fun!\n        ")
        self.getPage('/', self.cookies)
        self.assertBody("\n            During your current session, you've viewed this\n            page 2 times! Your life is a patio of fun!\n        ")

    def test08GeneratorsAndYield(self):
        self.getPage('/load_tut_module/tut08_generators_and_yield')
        self.getPage('/')
        self.assertBody('<html><body><h2>Generators rule!</h2><h3>List of users:</h3>Remi<br/>Carlos<br/>Hendrik<br/>Lorenzo Lamas<br/></body></html>')

    def test09Files(self):
        self.getPage('/load_tut_module/tut09_files')
        filesize = 5
        h = [('Content-type', 'multipart/form-data; boundary=x'),
         (
          'Content-Length', str(105 + filesize))]
        b = '--x\nContent-Disposition: form-data; name="myFile"; filename="hello.txt"\r\nContent-Type: text/plain\r\n\r\n'
        b += 'a' * filesize + '\n' + '--x--\n'
        self.getPage('/upload', h, 'POST', b)
        self.assertBody('<html>\n        <body>\n            myFile length: %d<br />\n            myFile filename: hello.txt<br />\n            myFile mime-type: text/plain\n        </body>\n        </html>' % filesize)
        self.getPage('/download')
        self.assertStatus('200 OK')
        self.assertHeader('Content-Type', 'application/x-download')
        self.assertHeader('Content-Disposition', 'attachment; filename="pdf_file.pdf"')
        self.assertEqual(len(self.body), 85698)

    def test10HTTPErrors(self):
        self.getPage('/load_tut_module/tut10_http_errors')
        self.getPage('/')
        self.assertInBody('<a href="toggleTracebacks">')
        self.assertInBody('<a href="/doesNotExist">')
        self.assertInBody('<a href="/error?code=403">')
        self.assertInBody('<a href="/error?code=500">')
        self.assertInBody('<a href="/messageArg">')
        self.getPage('/traceback_setting')
        setting = self.body
        self.getPage('/toggleTracebacks')
        self.assertStatus((302, 303))
        self.getPage('/traceback_setting')
        self.assertBody(str(not eval(setting)))
        self.getPage('/error?code=500')
        self.assertStatus(500)
        self.assertInBody('The server encountered an unexpected condition which prevented it from fulfilling the request.')
        self.getPage('/error?code=403')
        self.assertStatus(403)
        self.assertInBody("<h2>You can't do that!</h2>")
        self.getPage('/messageArg')
        self.assertStatus(500)
        self.assertInBody("If you construct an HTTPError with a 'message'")