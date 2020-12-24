# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/underdog/github/flask-json-multidict/flask_json_multidict/test/test.py
# Compiled at: 2015-03-03 18:31:24
# Size of source mod 2**32: 206 bytes
from unittest import TestCase
from flask_json_multidict import flask_json_multidict

class TestRunFunction(TestCase):

    def test_run_exists(self):
        self.assertTrue(bool(flask_json_multidict.run))