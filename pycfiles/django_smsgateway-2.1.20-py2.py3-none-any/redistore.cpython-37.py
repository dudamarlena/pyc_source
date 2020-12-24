# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tim/unleashed/django-smsgateway/smsgateway/tests/backends/redistore.py
# Compiled at: 2019-04-19 04:31:39
# Size of source mod 2**32: 1544 bytes
from __future__ import absolute_import
from django.conf import settings
import django.test as DjangoTestCase
from smsgateway.backends.redistore import RedistoreBackend
from smsgateway.sms import SMSRequest
from smsgateway.utils import check_cell_phone_number, truncate_sms
from six.moves import zip
req_data = {'to':'32045000001;32045000002;32045000003', 
 'msg':'text of the message', 
 'signature':'cropped to 11 chars'}

class RedistoreBackendTestCase(DjangoTestCase):

    def setUp(self):
        self.backend = RedistoreBackend()
        self.conf = settings.SMSGATEWAY_ACCOUNTS['redistore']

    def test_init(self):
        for key in ('redis_key_prefix', 'redis_pool', 'redis_conn', 'reference', 'sender',
                    'sms_data_iter', 'sent_smses'):
            assert key in list(self.backend.__dict__.keys())

    def test_initialize_without_sms_request(self):
        assert self.backend._initialize(None, self.conf) is False

    def test_initialize_with_sms_request(self):
        sms_request = SMSRequest(**req_data)
        assert self.backend._initialize(sms_request, self.conf) is True

    def test_get_sms_list(self):
        sms_list = self.backend._get_sms_list(SMSRequest(**req_data))
        assert len(sms_list) == 3
        for to, sms in zip(req_data['to'].split(';'), sms_list):
            assert sms.to[0] == check_cell_phone_number(to)
            assert sms.msg == truncate_sms(req_data['msg'])
            assert sms.signature == req_data['signature'][:len(sms.signature)]