# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/underdog/github/flask-json-multidict/flask_json_multidict/test/test.py
# Compiled at: 2015-03-03 18:31:24
from unittest import TestCase
from flask_json_multidict import flask_json_multidict

class TestRunFunction(TestCase):

    def test_run_exists(self):
        self.assertTrue(bool(flask_json_multidict.run))