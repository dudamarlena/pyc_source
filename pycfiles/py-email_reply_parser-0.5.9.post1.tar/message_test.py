# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/oleiade/Dev/Sandbox/Python/py-elevator/tests/message_test.py
# Compiled at: 2012-10-23 05:10:23
import unittest2, msgpack
from nose.tools import raises
from pyelevator.message import Request, Response, ResponseHeader, MessageFormatError

class RequestTest(unittest2.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @raises(MessageFormatError)
    def test_request_with_missing_mandatory_arg(self):
        Request(**{'meta': {}, 'db_uid': '123-456-789', 
           'args': []})

    def test_request_with_all_args(self):
        try:
            Request(**{'meta': {}, 'db_uid': '123-456-789', 
               'command': 'GET', 
               'args': []})
        except MessageFormatError:
            self.fail('Request() raised MessageFormatError unexpectedly!')

    def test_request_without_db_uid_arg(self):
        try:
            req = Request(**{'meta': {}, 'command': 'GET', 
               'args': []})
        except MessageFormatError:
            self.fail('Request() raised MessageFormatError unexpectedly!')

        unpacked_req = msgpack.unpackb(req)
        self.assertIsNone(unpacked_req['uid'])

    @raises(MessageFormatError)
    def test_response_header_with_missing_mandatory_arg(self):
        raw_header = msgpack.packb({'status': -1, 
           'err_code': 0})
        ResponseHeader(raw_header)

    def test_response_header_with_all_args(self):
        try:
            raw_header = msgpack.packb({'status': -1, 
               'err_code': 0, 
               'err_msg': ''})
            resp = ResponseHeader(raw_header)
        except MessageFormatError:
            self.fail('ResponseHeader() raised MessageFormatError unexpectedly!')

        self.assertTrue(hasattr(resp, 'status'))
        self.assertTrue(hasattr(resp, 'err_code'))
        self.assertTrue(hasattr(resp, 'err_msg'))

    @raises(MessageFormatError)
    def test_response_with_missing_mandatory_arg(self):
        raw_resp = msgpack.packb({})
        ResponseHeader(raw_resp)