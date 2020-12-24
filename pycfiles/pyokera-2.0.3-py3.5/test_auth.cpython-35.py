# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/okera/tests/test_auth.py
# Compiled at: 2020-02-27 14:06:57
# Size of source mod 2**32: 3418 bytes
import unittest, pytest, thriftpy
from okera import context
attempts = 0

def bad_then_good_func():
    global attempts
    token = None
    if attempts == 0:
        token = 'foo.bar'
    else:
        token = 'foo'
    attempts += 1
    return token


def bad_twice_then_good_func():
    global attempts
    token = None
    if attempts < 2:
        token = 'foo.bar'
    else:
        raise Exception()
    attempts += 1
    return token


def good_then_bad_func():
    global attempts
    token = None
    if attempts == 0:
        token = 'foo'
    else:
        raise Exception()
    attempts += 1
    return token


def always_bad():
    return 'foo.bar'


class AuthTest(unittest.TestCase):

    @staticmethod
    def _reset_attempts():
        global attempts
        attempts = 0

    def setUp(self):
        AuthTest._reset_attempts()

    def test_token_func_basic(self):
        ctx = context()
        ctx.enable_token_auth(token_func=bad_then_good_func)
        with ctx.connect(host='localhost', port=12050) as (conn):
            results = conn.scan_as_json('okera_sample.whoami')
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0]['user'], 'foo')

    def test_token_func_no_failure(self):
        ctx = context()
        ctx.enable_token_auth(token_func=good_then_bad_func)
        with ctx.connect(host='localhost', port=12050) as (conn):
            results = conn.scan_as_json('okera_sample.whoami')
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0]['user'], 'foo')

    def test_token_func_and_token_str(self):
        ctx = context()
        ctx.enable_token_auth(token_func=always_bad, token_str='foo')
        with ctx.connect(host='localhost', port=12050) as (conn):
            results = conn.scan_as_json('okera_sample.whoami')
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0]['user'], 'foo')

    def test_token_func_never_succeed(self):
        ctx = context()
        ctx.enable_token_auth(token_func=always_bad)
        with pytest.raises(thriftpy.transport.TTransportException):
            with ctx.connect(host='localhost', port=12050):
                raise Exception()

    def test_token_func_retry_once_still_fail(self):
        ctx = context()
        ctx.enable_token_auth(token_func=bad_twice_then_good_func)
        with pytest.raises(thriftpy.transport.TTransportException):
            with ctx.connect(host='localhost', port=12050):
                raise Exception()

    def test_token_func_non_picklable(self):

        def fn():
            return 'foo'

        ctx = context()
        with pytest.raises(ValueError):
            ctx.enable_token_auth(token_func=fn)