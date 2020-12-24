# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /test/test_issue_2.py
# Compiled at: 2019-09-13 21:23:39
# Size of source mod 2**32: 351 bytes
from __future__ import unicode_literals
from marrow.mailer import Mailer

def test_issue_2():
    mail = Mailer({'manager.use':'immediate', 
     'transport.use':'smtp', 
     'transport.host':'secure.emailsrvr.com', 
     'transport.tls':'ssl'})
    mail.start()
    mail.stop()