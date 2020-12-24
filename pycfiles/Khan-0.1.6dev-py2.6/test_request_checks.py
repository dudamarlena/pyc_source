# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/khan/tests/test_utils/test_request_checks.py
# Compiled at: 2010-05-12 10:25:54
from khan.utils.testing import *
from khan.utils import *
from khan.utils.request_checks import *
from khan.utils.decorator import HTTPStatusOnInvalid
from khan.httpstatus import HTTPStatus

class TestRequestChecks(TestCase):

    def test_request_check(self):

        def App(environ, start_response):
            return HTTPStatus(200)(environ, start_response)

        app = TestApp(reqchecker(Equal(request_method='get', case_sensitive=True), HTTPStatusOnInvalid(404))(App))
        self.failUnlessEqual(app.get('/', status='*').status_int, 404)
        app = TestApp(reqchecker(Equal(request_method='GET'))(App))
        self.failUnlessEqual(app.get('/', status='*').status_int, 200)
        app = TestApp(reqchecker(Equal(request_method='get'))(App))
        self.failUnlessEqual(app.get('/', status='*').status_int, 200)
        app = TestApp(reqchecker(Equal(request_method='get', case_sensitive=True))(App))
        self.failUnlessEqual(app.get('/', status='*').status_int, 400)
        app = TestApp(reqchecker(Equal(not_exists='not exists'))(App))
        self.failUnlessEqual(app.get('/', status='*').status_int, 400)
        app = TestApp(reqchecker(Equal(request_method='GET') | Equal(request_method='POST') | Equal(request_method='PUT'))(App))
        self.failUnlessEqual(app.get('/', status='*').status_int, 200)
        self.failUnlessEqual(app.post('/', status='*').status_int, 200)
        self.failUnlessEqual(app.put('/', status='*').status_int, 200)
        app = TestApp(reqchecker(Equal(request_method='GET') & Equal(path_info='/'))(App))
        self.failUnlessEqual(app.get('/', status='*').status_int, 200)
        self.failUnlessEqual(app.get('/path_info', status='*').status_int, 400)
        self.failUnlessEqual(app.post('/', status='*').status_int, 400)
        app = TestApp(reqchecker(~Equal(request_method='GET'))(App))
        self.failUnlessEqual(app.get('/', status='*').status_int, 400)
        self.failUnlessEqual(app.post('/', status='*').status_int, 200)


if __name__ == '__main__':
    unittest.main()