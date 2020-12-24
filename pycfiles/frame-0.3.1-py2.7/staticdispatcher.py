# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/frame/testsuite/staticdispatcher.py
# Compiled at: 2013-03-16 04:08:06
import unittest, os
from tempfile import NamedTemporaryFile
from frame.staticdispatcher import StaticDispatcher
from frame._app import app
from frame.errors import Error404, Error401

class TestStaticDispatcher(unittest.TestCase):

    def setUp(self):
        self.temp_file = NamedTemporaryFile(delete=False)
        self.file_data = "This is a dummy test file. There really shouldn't\nbe very much in it. Let's see if this works.\n"
        self.temp_file.write(self.file_data)
        self.temp_file.seek(0)
        self.dir_name, self.file_name = os.path.split(self.temp_file.name)
        self.static_map = StaticDispatcher(app, {'/static': self.dir_name})

    def tearDown(self):
        os.remove(self.temp_file.name)

    def test_read_file(self):
        file_data = self.static_map.read_file(self.temp_file.name)
        self.assertEqual(('').join(file_data), self.file_data)

    def test_found(self):
        environ = {'PATH_INFO': '/static/%s' % self.file_name}
        response = self.static_map.match(environ)
        required_headers = ('Last-Modified', 'Connection', 'Content-Type', 'Server')
        assert response.status == '200 OK'
        assert all(i in response.headers for i in required_headers)
        assert self.file_data == ('').join(response.body)

    def test_not_found(self):
        environ = {'PATH_INFO': '/static/not_found_file.something.txt.asdfsd'}
        with self.assertRaises(Error404):
            match = self.static_map.match(environ)