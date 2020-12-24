# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.4/site-packages/kite_mail/mail.py
# Compiled at: 2015-07-05 09:16:51
# Size of source mod 2**32: 926 bytes
import re, pyzmail

class kiteMail(object):

    def __init__(self, raw_mail):
        self.raw_mail = raw_mail
        self.factory = self._migrate_mailfactory()
        self.content_encode = self._get_content_encode()

    def _migrate_mailfactory(self):
        return pyzmail.PyzMessage.factory(self.raw_mail)

    def _get_content_encode(self):
        header_content_type = self.factory.get_decoded_header('content-type')
        _result = re.search('charset=(\\S+)', header_content_type)
        return _result.group(1).lower()

    def get_mailpart(self):
        msg = self.factory
        if msg.text_part:
            _result = msg.text_part.get_payload()
        elif msg.text_html:
            _result = msg.html_part.get_payload()
        if not self.content_encode == None:
            return _result.decode(self.content_encode)
        return _result