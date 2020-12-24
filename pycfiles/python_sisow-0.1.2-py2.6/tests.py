# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tests/tests.py
# Compiled at: 2012-10-21 14:36:02
"""General tests on general functions in python-sisow
"""
from unittest import TestCase
from hashlib import sha1
from sisow import _signature
from sisow import _sha1_signature

class TestSignature(TestCase):

    def setUp(self):
        self.keys = ('trxid', 'shopid', 'merchantid')
        self.signature = '%(trxid)s%(shopid)s%(merchantid)s'
        self.data = {'trxid': 'abcdef0123456789', 
           'shopid': '3', 
           'merchantid': '132435'}

    def test_empty(self):
        self.assertEqual(_signature([]), '')

    def test_multiple(self):
        self.assertEqual(_signature(self.keys), self.signature)

    def test_sha1_empty(self):
        outcome = sha1('').hexdigest()
        self.assertEquals(_sha1_signature('', {}, ''), outcome)

    def test_sha1(self):
        signature = _signature(self.keys)
        outcome = sha1(self.signature % self.data).hexdigest()
        self.assertEquals(_sha1_signature(self.signature, self.data, ''), outcome)

    def test_sha1_secret(self):
        secret = 'geheim'
        signature = _signature(self.keys)
        outcome = sha1(self.signature % self.data)
        outcome.update(secret)
        outcome = outcome.hexdigest()
        self.assertEquals(_sha1_signature(self.signature, self.data, secret), outcome)