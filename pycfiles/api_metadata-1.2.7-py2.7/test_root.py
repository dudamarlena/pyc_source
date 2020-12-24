# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/api_metadata/tests/views/test_root.py
# Compiled at: 2019-02-06 12:21:52
from ..case import APITestCase

class TestApp(APITestCase):

    def test_root(self):
        response = self.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('api', response.json)
        self.assertIn('description', response.json)
        self.assertIn('version', response.json)