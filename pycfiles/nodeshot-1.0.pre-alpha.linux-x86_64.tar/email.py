# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/nodeshot/core/metrics/email.py
# Compiled at: 2015-03-25 12:20:02
from djcelery_email.backends import CeleryEmailBackend
from .utils import write

class CeleryInfluxDbEmailBackend(CeleryEmailBackend):

    def send_messages(self, email_messages):
        result_tasks = super(CeleryInfluxDbEmailBackend, self).send_messages(email_messages)
        write(name='emails_sent', values={'value': len(email_messages)})
        return result_tasks