# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/robograph/datamodel/nodes/lib/email.py
# Compiled at: 2016-07-13 17:51:17
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP
from robograph.datamodel.base import node

class SmtpClient:
    """
    Utility class representing an SMTP client
    """

    def __init__(self, server_hostname, server_port, username, password, use_tls=True):
        self._server_hostname = server_hostname
        self._server_port = server_port
        self._username = username
        self._password = password
        self._use_tls = use_tls

    def send(self, subject, body, recipients_list, sender, mime='html'):
        if mime == 'text':
            msg = MIMEText(body)
        else:
            msg = MIMEMultipart('alternative')
            msg.attach(MIMEText(body, 'html'))
        msg['Subject'] = subject
        server = SMTP(self._server_hostname + ':' + str(self._server_port))
        if self._use_tls:
            server.starttls()
        server.login(self._username, self._password)
        server.sendmail(sender, recipients_list, msg.as_string())
        server.quit()


class SmtpEmail(node.Node):
    """
    This node sends an e-mail message via SMTP
    Requirements:
      server_hostname --> str, SMTP server hostname
      server_port --> int, SMTP server port
      username --> str, SMTP server username
      password --> str, SMTP server password
      use_tls --> bool, use TLS to encrypt communication with the SMTP server
      sender --> str, e-mail address of the email sender
      recipients_list --> list of str, recipients e-mail address list
      subject --> subject of the email
      body --> body of the email
      mime_type --> MIME type of the email body (optional)
    """
    _reqs = [
     'server_hostname', 'server_port', 'username', 'password', 'sender',
     'recipients_list', 'subject', 'body', 'mime_type']

    def output(self):
        smtp_client = SmtpClient(self._params['server_hostname'], self._params['server_port'], self._params['username'], self._params['password'], self._params['use_tls'])
        if self._params['mime_type'] is None:
            mime = 'html'
        else:
            mime = self._params['mime_type']
        smtp_client.send(self._params['subject'], self._params['body'], self._params['recipients_list'], self._params['sender'], mime)
        return