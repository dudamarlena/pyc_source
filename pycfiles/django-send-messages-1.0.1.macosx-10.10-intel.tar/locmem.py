# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/esperyong/develop/pyprojects/hwbuluo_src/hwbuluo-site/venv/lib/python2.7/site-packages/sms/backends/locmem.py
# Compiled at: 2015-05-11 04:50:36
"""
Backend for test environment.
"""
import sms
from sms.backends.base import BaseSMSBackend

class SMSBackend(BaseSMSBackend):
    """A sms backend for use during test sessions.

    The test connection stores sms messages in a dummy outbox,
    rather than really sending them out.

    The dummy outbox is accessible through the outbox instance attribute.
    """

    def __init__(self, *args, **kwargs):
        super(SMSBackend, self).__init__(*args, **kwargs)
        if not hasattr(sms, 'outbox'):
            sms.outbox = []

    def send_messages(self, messages):
        """Redirect messages to the dummy outbox"""
        for message in messages:
            message.mobile()

        sms.outbox.extend(messages)
        response_examples = [
         '{"code": 0,"msg": "OK","detail": null,"result":{"count":1,"fee":1,"sid":1097}}',
         '{"code": 3,"msg": "账户余额不足","detail":"账户需要充值，请充值后重试"}',
         '{"code": -2,"msg": "API没有权限","detail":"用户没有对应的API权限"}',
         '{"code": -53,"msg": "API没有权限","detail":"提交短信时系统出错"}']
        responses = [ response_examples[i] for i in range(len(messages)) ]
        return (
         len(messages), response_examples)


class SMSAlwaysSuccessBackend(BaseSMSBackend):
    """A sms backend for use during test sessions.

    The test connection stores sms messages in a dummy outbox,
    rather than sending them out on the wire.

    The dummy outbox is accessible through the outbox instance attribute.
    """

    def __init__(self, *args, **kwargs):
        super(SMSAlwaysSuccessBackend, self).__init__(*args, **kwargs)
        if not hasattr(sms, 'outbox'):
            sms.outbox = []

    def send_messages(self, messages):
        """Redirect messages to the dummy outbox"""
        for message in messages:
            message.mobile()

        sms.outbox.extend(messages)
        response_examples = [
         '{"code": 0,"msg": "OK","detail": null,"result":{"count":1,"fee":1,"sid":1097}}']
        responses = [ response_examples[i] for i in range(len(messages)) ]
        return (
         len(messages), response_examples)