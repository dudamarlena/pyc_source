# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\simulation\test_requests.py
# Compiled at: 2016-04-27 04:45:20
# Size of source mod 2**32: 2015 bytes
from unittest import TestCase
from mock import MagicMock, PropertyMock
from mad.simulation.requests import Request

class RequestTests(TestCase):

    def test_response_time(self):
        examples = [{'sent_at': 10,  'replied_at': 26}, {'sent_at': 10,  'replied_at': 11}, {'sent_at': 10,  'replied_at': 12}, {'sent_at': 10,  'replied_at': 100}]
        for each_example in examples:
            self.do_test_response_time(**each_example)

    def do_test_response_time(self, sent_at, replied_at):
        sender = MagicMock()
        type(sender.schedule).time_now = PropertyMock(side_effect=[sent_at, replied_at])
        request = Request(sender, 0, 'foo_operation', 1)
        recipient = MagicMock()
        request.send_to(recipient)
        request.reply_success()
        self.assertEqual(replied_at - sent_at, request.response_time)

    def test_response_time_on_error(self):
        sender = MagicMock()
        sender.schedule.time = MagicMock(return_value=(5, 10, 15))
        request = Request(sender, 0, 'foo_operation', 1)
        recipient = MagicMock()
        request.send_to(recipient)
        request.reply_error()
        with self.assertRaises(AssertionError):
            request.response_time