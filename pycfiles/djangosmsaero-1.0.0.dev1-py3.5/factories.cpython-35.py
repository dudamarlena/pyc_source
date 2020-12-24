# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/smsaero/factories.py
# Compiled at: 2016-11-05 20:43:08
# Size of source mod 2**32: 596 bytes
import factory
from .models import Signature
from .models import SMSMessage

class SignatureF(factory.Factory):

    class Meta:
        model = Signature

    name = factory.Sequence(lambda n: 'Name{0}'.format(n))


class SMSMessageF(factory.Factory):

    class Meta:
        model = SMSMessage

    sms_id = factory.Sequence(lambda n: n)
    phone = factory.Sequence(lambda n: '7123456789{0}'.format(n))
    signature = factory.LazyAttribute(lambda a: SignatureF())
    text = factory.Sequence(lambda n: 'Message{0}'.format(n))
    status = SMSMessage.STATUS_ACCEPTED