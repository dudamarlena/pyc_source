# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/twiddler/output/MTText.py
# Compiled at: 2008-07-24 14:48:01
from email.Charset import Charset
from email.MIMEText import MIMEText as OriginalMIMEText
from email.MIMENonMultipart import MIMENonMultipart

class MTText(OriginalMIMEText):

    def __init__(self, _text, _subtype='plain', _charset='us-ascii'):
        if not isinstance(_charset, Charset):
            _charset = Charset(_charset)
        if isinstance(_text, unicode):
            _text = _text.encode(_charset.input_charset)
        MIMENonMultipart.__init__(self, 'text', _subtype, **{'charset': _charset.input_charset})
        self.set_payload(_text, _charset)