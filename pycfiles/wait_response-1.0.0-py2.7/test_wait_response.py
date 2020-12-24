# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/test_wait_response.py
# Compiled at: 2017-10-31 07:25:54
import unittest, responses
from wait_response import wait_response_status

class TestWaitResponse(unittest.TestCase):

    def test_wait_response_status_until_max_attempts(self):
        result = wait_response_status('http://localhost:8080/someWrongUrl', 2, 1, 'UP')
        self.assertEqual(result, 1)

    @responses.activate
    def test_wait_response_status_up(self):
        responses.add(responses.GET, 'http://localhost:8080/health', json={'status': 'UP'}, status=200)
        result = wait_response_status('http://localhost:8080/health', 2, 1, 'UP')
        self.assertEqual(result, 0)


if __name__ == '__main__':
    unittest.main()