# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpDcc/libs/python/web.py
# Compiled at: 2020-05-02 23:38:35
# Size of source mod 2**32: 2551 bytes
"""
Module that contains utility functions related with email
"""
import email, smtplib, webbrowser
try:
    import urllib2 as urllib
except ImportError:
    import urllib

class Email(object):
    __doc__ = '\n    Base class that represents an email\n    '

    def __init__(self, user=None, password=None):
        super(Email, self).__init__()
        self.user = user
        self.password = password
        self.emails_list = list()
        self.server = None
        self._setup_message()

    def set_subject(self, subject):
        self.message['Subject'] = subject

    def add_message(self, text):
        self.message.attach(email.MIMEText(text))

    def send(self, emails_list):
        joined = email.Utils.COMMASPACE.join(emails_list)
        self.message['To'] = joined
        self._setup_server()
        if self.server:
            self.server.sendemail(self.user, emails_list, self.message.as_string())
            self.server.quit()

    def _setup_message(self):
        self.message = email.MIMEMultipart.MIMEMultipart()
        self.message['From'] = self.user
        self.message['Subject'] = ''
        self.message['To'] = list()

    def _setup_server(self):
        self.server = smtplib.SMTP()
        self.server.set_debuglevel(1)


class Gmail(Email, object):

    def __init__(self, user=None, password=None):
        super(Gmail, self).__init__(user=user, password=password)

    def _setup_server(self):
        super(Gmail, self)._setup_server()
        smtp_host = 'smtp.gmail.com'
        smtp_port = 587
        self.server.connect(smtp_host, smtp_port)
        self.server.ehlo()
        self.server.starttls()
        self.server.login(self.user, self.password)


class LocalHost(Email, object):

    def __init__(self, user):
        super(LocalHost, self).__init__(user=user, password='')

    def _setup_server(self):
        self.server = smtplib.SMTP('localhost')


def open_web(url):
    """
    Open given web URL in user web browser
    :param url: str
    """
    webbrowser.open(url)


def safe_open_url(url):
    """
    Opens given URL in a safe way
    :param url: str
    :return:
    """
    try:
        result = urllib.urlopen(url)
    except urllib.HTTPError as exc:
        raise Exception('{} : {}'.format(exc, exc.url))

    return result