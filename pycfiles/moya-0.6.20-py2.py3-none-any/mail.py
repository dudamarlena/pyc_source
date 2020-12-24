# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/mail.py
# Compiled at: 2016-03-29 05:36:08
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from .logic import MoyaException
from .console import Cell
from .tools import summarize_text
from .compat import text_type, string_types
from smtplib import SMTP, SMTPException
from socket import error as socket_error
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
log = logging.getLogger(b'moya.email')

class Email(object):
    """A single email message"""

    def __init__(self, data=None):
        self.headers = {}
        self.data = data or {}
        self.text = None
        self.html = None
        self.subject = None
        setattr(self, b'from', None)
        self.to = []
        self.cc = []
        self.bcc = []
        self.replyto = None
        self.app = None
        self.email_element = None
        return

    @property
    def to_text(self):
        return (b',').join(self.to)

    @property
    def cc_text(self):
        return (b',').join(self.cc)

    @property
    def bcc_text(self):
        return (b',').join(self.bcc)

    def _append_emails(self, dst, emails):
        if emails is None:
            return
        else:
            if isinstance(emails, string_types):
                emails = [ e.strip() for e in emails.split(b',') ]
            dst.extend(emails)
            return

    def add_to(self, emails):
        self._append_emails(self.to, emails)

    def add_cc(self, emails):
        self._append_emails(self.cc, emails)

    def add_bcc(self, emails):
        self._append_emails(self.bcc, emails)

    def __moyaconsole__(self, console):
        table = []
        table.append([Cell(b'Subject:', bold=True), self.subject or Cell(b'No subject', fg=b'red')])
        if self.to_text:
            table.append([Cell(b'To:', bold=True), self.to_text])
        if self.cc_text:
            table.append([Cell(b'Cc:', bold=True), self.cc_text])
        if self.bcc_text:
            table.append([Cell(b'Bcc:', bold=True), self.bcc_text])
        if self.replyto is not None:
            table.append([Cell(b'Reply-To:', bold=True), self.replyto])
        _from = self.get_from()
        if _from:
            table.append([Cell(b'From:', bold=True), _from])
        if self.text:
            table.append([b'text', summarize_text(self.text, max_length=3000)])
        if self.html:
            table.append([b'html', summarize_text(self.html, max_length=3000)])
        console.table(table, header=False, dividers=False)
        return

    def set_from(self, value):
        setattr(self, b'from', value)

    def get_from(self):
        return getattr(self, b'from')

    def to_msg(self):
        if self.text is not None and self.html is not None:
            msg = MIMEMultipart(b'alternative')
        else:
            msg = MIMEMultipart()
        for k, v in self.headers.items():
            msg[k] = v

        if self.subject is not None:
            msg[b'Subject'] = self.subject
        if self.to:
            msg[b'To'] = (b', ').join(self.to)
        if self.cc:
            msg[b'Cc'] = (b', ').join(self.cc)
        if self.bcc:
            msg[b'Bcc'] = (b', ').join(self.bcc)
        if self.replyto is not None:
            msg[b'Reply-To'] = self.replyto
        if self.text is not None:
            msg.attach(MIMEText(self.text, b'plain', b'utf-8'))
        if self.html is not None:
            msg.attach(MIMEText(self.html, b'html', b'utf-8'))
        return msg.as_string()


class MailServer(object):
    """Stores SMTP server info and handles sending"""

    def __init__(self, host, name=None, default=False, port=None, local_hostname=None, timeout=None, username=None, password=None, sender=None):
        self.name = name
        self.default = default
        self.host = host
        self.port = port
        self.local_hostname = local_hostname
        self.timeout = timeout
        self.username = username
        self.password = password
        self.sender = sender

    def __repr__(self):
        return (b'<smtp "{}:{}" "{}">').format(self.host, self.port, self.name)

    def connect(self):
        """Connect to the smpt server, and login if necessary. Returns an SMTP instance."""
        try:
            smtp = SMTP(self.host, self.port, self.local_hostname, self.timeout)
        except SMTPException as e:
            raise MoyaException(b'email.error', text_type(e))
        except socket_error as e:
            raise MoyaException(b'email.connection-refused', text_type(e))

        if self.username:
            try:
                try:
                    smtp.login(self.username, self.password)
                except smtp.SMTPException as e:
                    raise MoyaException(b'email.auth-fail', text_type(e))

            finally:
                smtp.quit()

        return smtp

    def check(self):
        """Checks connectivity to smtp server. Returns True on success, or throws an exception."""
        smtp = self.connect()
        smtp.quit()
        return True

    def send(self, emails, fail_silently=True):
        """Sends an email, or sequence of emails. Returns the number of failures."""
        if isinstance(emails, Email):
            emails = [
             emails]
        emails = [ (email, email.to_msg()) for email in emails ]
        smtp = self.connect()
        try:
            failures = 0
            for email, msg in emails:
                try:
                    sender = text_type(getattr(email, b'from') or self.sender or b'admin@localhost')
                    smtp.sendmail(sender, (b', ').join(email.to), msg)
                except SMTPException:
                    if not fail_silently:
                        raise
                    failures += 1

        finally:
            try:
                smtp.quit()
            except SMTPException:
                if not fail_silently:
                    raise

        return failures