# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\bzETL\util\emailer.py
# Compiled at: 2013-11-22 17:13:18
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib, sys
from .struct import nvl

class Emailer:

    def __init__(self, settings):
        self.settings = settings

    def send_email(self, from_address=None, to_addrs=None, subject='No Subject', text_data=None, html_data=None):
        """Sends an email.

        from_addr is an email address; to_addrs is a list of email adresses.
        Addresses can be plain (e.g. "jsmith@example.com") or with real names
        (e.g. "John Smith <jsmith@example.com>").

        text_data and html_data are both strings.  You can specify one or both.
        If you specify both, the email will be sent as a MIME multipart
        alternative, i.e., the recipient will see the HTML content if his
        viewer supports it; otherwise he'll see the text content.
        """
        settings = self.settings
        from_address = nvl(from_address, settings.from_address)
        if not from_address or not to_addrs:
            raise Exception('Both from_addr and to_addrs must be specified')
        if not text_data and not html_data:
            raise Exception('Must specify either text_data or html_data')
        if settings.use_ssl:
            server = smtplib.SMTP_SSL(settings.host, settings.port)
        else:
            server = smtplib.SMTP(settings.host, settings.port)
        if settings.username and settings.password:
            server.login(settings.username, settings.password)
        if not html_data:
            msg = MIMEText(text_data)
        elif not text_data:
            msg = MIMEMultipart()
            msg.preamble = subject
            msg.attach(MIMEText(html_data, 'html'))
        else:
            msg = MIMEMultipart('alternative')
            msg.attach(MIMEText(text_data, 'plain'))
            msg.attach(MIMEText(html_data, 'html'))
        msg['Subject'] = subject
        msg['From'] = from_address
        msg['To'] = (', ').join(to_addrs)
        server.sendmail(from_address, to_addrs, msg.as_string())
        server.quit()


if sys.hexversion < 33948656:
    import socket, ssl

    def _get_socket_fixed(self, host, port, timeout):
        if self.debuglevel > 0:
            print >> sys.stderr, 'connect:', (host, port)
        new_socket = socket.create_connection((host, port), timeout)
        new_socket = ssl.wrap_socket(new_socket, self.keyfile, self.certfile)
        self.file = smtplib.SSLFakeFile(new_socket)
        return new_socket


    smtplib.SMTP_SSL._get_socket = _get_socket_fixed