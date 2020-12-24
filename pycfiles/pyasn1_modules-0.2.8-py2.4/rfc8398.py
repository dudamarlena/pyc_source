# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyasn1_modules/rfc8398.py
# Compiled at: 2019-10-17 01:00:24
from pyasn1.type import char
from pyasn1.type import constraint
from pyasn1.type import univ
from pyasn1_modules import rfc5280
MAX = float('inf')
id_pkix = rfc5280.id_pkix
id_on = id_pkix + (8, )
id_on_SmtpUTF8Mailbox = id_on + (9, )

class SmtpUTF8Mailbox(char.UTF8String):
    __module__ = __name__


SmtpUTF8Mailbox.subtypeSpec = constraint.ValueSizeConstraint(1, MAX)
on_SmtpUTF8Mailbox = rfc5280.AnotherName()
on_SmtpUTF8Mailbox['type-id'] = id_on_SmtpUTF8Mailbox
on_SmtpUTF8Mailbox['value'] = SmtpUTF8Mailbox()
_anotherNameMapUpdate = {id_on_SmtpUTF8Mailbox: SmtpUTF8Mailbox()}
rfc5280.anotherNameMap.update(_anotherNameMapUpdate)