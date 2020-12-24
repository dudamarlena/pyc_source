# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/foundation/smtp.py
# Compiled at: 2012-10-12 07:02:39
import smtplib
from email.mime.text import MIMEText
from defaultsmanager import ServerDefaultsManager

class SMTP(object):
    __slots__ = ()

    @staticmethod
    def send(from_address, to_addresses, message, mail_options=[], rcpt_options=[]):
        sd = ServerDefaultsManager()
        config = sd.default_as_dict('SMTPServer')
        hostname = config.get('hostname', 'localhost')
        username = config.get('username', None)
        password = config.get('password', None)
        starttls = config.get('starttls', 'YES').upper()
        server = smtplib.SMTP(hostname)
        if starttls == 'YES':
            server.starttls()
        if username is not None and password is not None:
            server.login(username, password)
        if not isinstance(message, basestring):
            message = message.as_string()
        server.sendmail(from_address, to_addresses, message, mail_options, rcpt_options)
        server.close()
        return