# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/khan/tests/test_static.py
# Compiled at: 2010-05-12 10:25:54
import os, unittest
from khan.utils.testing import TestCase, TestApp
from tempfile import mktemp
from khan.static import *

class FileTester(TestCase):

    def test_basic(self):
        filename = mktemp()
        fobj = file(filename, 'w')
        fobj.close()
        headers = [('X-KK', 'kk')]
        content_type = 'text/test'
        app = File(filename, headers=headers, content_type=content_type)
        app = TestApp(app)
        resp = app.get('/', status='*')
        assert resp.content_type == content_type
        assert 'X-KK' in resp.headers
        if os.path.isfile(filename):
            os.remove(filename)


if __name__ == '__main__':
    unittest.main()