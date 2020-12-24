# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/matt/Development/django-sms-gateway/sms/tasks.py
# Compiled at: 2012-12-03 00:30:00
from celery.task import Task
import logging
from sms.models import Message, Gateway

class SendMessage(Task):
    max_retries = 3
    default_retry_delay = 3

    def run(self, message_id, gateway_id=None, **kwargs):
        logging.debug('About to send a message.')
        try:
            message = Message.objects.get(pk=message_id)
        except Exception as exc:
            raise SendMessage.retry(exc=exc)

        if not gateway_id:
            if hasattr(message.billee, 'sms_gateway'):
                gateway = message.billee.sms_gateway
            else:
                gateway = Gateway.objects.all()[0]
        else:
            gateway = Gateway.objects.get(pk=gateway_id)
        response = gateway._send(message)
        logging.debug('Done sending message.')