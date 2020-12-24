# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mailutil.py
# Compiled at: 2019-12-05 15:34:38
# Size of source mod 2**32: 3164 bytes
"""
Helper module for using smtplib for secured connections

Author: Michael Ströder <michael@stroeder.com>

mainly a wrapper around smtplib.SMTP etc.
"""
__version__ = '0.4.0'
import socket, smtplib, email, email.mime.text, ssl, urllib.parse
urllib.parse.uses_query.extend(['smtp', 'smtps'])
SMTP_SOCKET = socket.socket

class SMTPHelper:
    __doc__ = '\n    Mix-in class with convenience methods\n    '

    def send_simple_message(self, from_addr, to_addr, charset, headers, msg):
        """
        Send a simple text/plain message
        """
        e_mail = email.mime.text.MIMEText(msg, 'plain', charset)
        e_mail.set_charset(charset)
        for header_name, header_value in headers:
            e_mail[header_name] = header_value

        self.sendmail(from_addr, to_addr, e_mail.as_string())


class SMTP(smtplib.SMTP, SMTPHelper):
    __doc__ = '\n    SMTP connection class\n    '


class SMTP_SSL(smtplib.SMTP_SSL, SMTPHelper):
    __doc__ = '\n    SMTPS connection class\n    '


def smtp_connection(smtp_url, local_hostname=None, ca_certs=None, timeout=60, debug_level=0):
    """
    This function opens a SMTP connection specified by `smtp_url'.

    It also invokes `SMTP.starttls()' or `SMTP.login()' if URL contains
    appropriate parameters.
    """

    def smtp_tls_context(ca_certs):
        ctx = ssl.SSLContext()
        ctx.verify_mode = ssl.CERT_REQUIRED
        ctx.check_hostname = True
        ctx.load_verify_locations(ca_certs, capath=None, cadata=None)
        return ctx

    smtp_url_obj = urllib.parse.urlparse(smtp_url)
    query_obj = urllib.parse.parse_qs((smtp_url_obj.query),
      keep_blank_values=True,
      strict_parsing=False)
    if smtp_url_obj.scheme == 'smtp':
        smtp_conn = SMTP(host=(smtp_url_obj.hostname),
          port=(smtp_url_obj.port),
          local_hostname=local_hostname,
          timeout=timeout)
        if 'STARTTLS' in query_obj:
            smtp_conn.starttls(context=(smtp_tls_context(ca_certs)))
    elif smtp_url_obj.scheme == 'smtps':
        smtp_conn = SMTP_SSL(host=(smtp_url_obj.hostname),
          port=(smtp_url_obj.port),
          local_hostname=local_hostname,
          timeout=timeout,
          context=(smtp_tls_context(ca_certs)))
    else:
        raise ValueError('Unsupported URL scheme %r' % smtp_url_obj.scheme)
    if smtp_url_obj.username:
        if smtp_url_obj.password:
            smtp_conn.login(smtp_url_obj.username, smtp_url_obj.password)
    smtp_conn.set_debuglevel(debug_level)
    return smtp_conn