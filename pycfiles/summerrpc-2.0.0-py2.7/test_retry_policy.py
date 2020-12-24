# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/summerrpc_tests/test_retry_policy.py
# Compiled at: 2018-07-31 10:42:31
import unittest
from summerrpc.helper import RetryPolicy, MaxRetryCountReached

class TestRetryPolicy(unittest.TestCase):

    def testRetryPolicy(self):
        retry_policy = RetryPolicy.Builder().with_max_retry_count(3).add_retry_exception(RuntimeError).with_retry_interval(1).build()

        def func():
            raise RuntimeError('just for test')

        try:
            retry_policy.run(func)
        except MaxRetryCountReached as ex:
            print ex.exc_info