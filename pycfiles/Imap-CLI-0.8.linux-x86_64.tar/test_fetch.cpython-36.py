# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/site-packages/imap_cli/tests/test_fetch.py
# Compiled at: 2018-04-21 11:53:05
# Size of source mod 2**32: 4471 bytes
"""Test helpers"""
import copy, email, imaplib, sys, unittest, six
from imap_cli import const
from imap_cli import fetch
from imap_cli import tests

class FetchTest(unittest.TestCase):
    reference_mail = {'headers':{'From':'exampleFrom <example@from.org>', 
      'Content-Transfer-Encoding':'quoted-printable', 
      'To':'exampleTo <example@to.org>', 
      'Date':'Tue, 03 Jan 1989 09:42:34 +0200', 
      'Subject':'Mocking IMAP Protocols', 
      'Content-Type':'text/html;\r\n\tcharset="windows-1252"', 
      'MIME-Version':'1.0'}, 
     'parts':[
      {'as_string':'\n'.join([
        'From: exampleFrom <example@from.org>',
        'Date: Tue, 03 Jan 1989 09:42:34 +0200',
        'Subject: Mocking IMAP Protocols',
        'To: exampleTo <example@to.org>',
        'MIME-Version: 1.0',
        'Content-Type: text/html;',
        '\tcharset="windows-1252"',
        'Content-Transfer-Encoding: quoted-printable',
        '',
        'EMAIL BODY CONTENT']), 
       'data':'\n'.join([
        'From: exampleFrom <example@from.org>',
        'Date: Tue, 03 Jan 1989 09:42:34 +0200',
        'Subject: Mocking IMAP Protocols',
        'To: exampleTo <example@to.org>',
        'MIME-Version: 1.0',
        'Content-Type: text/html;',
        '\tcharset="windows-1252"',
        'Content-Transfer-Encoding: quoted-printable',
        '',
        'EMAIL BODY CONTENT']), 
       'content_type':'text/html'}]}

    def setUp(self):
        imaplib.IMAP4_SSL = tests.ImapConnectionMock()

    def test_display(self):
        assert isinstance(fetch.display(self.reference_mail), six.string_types)

    def test_display_in_browser(self):
        assert isinstance(fetch.display((self.reference_mail), browser=True), six.string_types)

    def test_display_attachment(self):
        multipart_mail = copy.deepcopy(self.reference_mail)
        multipart_mail['parts'].append({'content_type':'img/png', 
         'data':'xxxxxx', 
         'filename':'IMGTEST'})
        assert isinstance(fetch.display(multipart_mail), six.string_types)

    def test_fetch_wrong(self):
        self.imap_account = imaplib.IMAP4_SSL()
        if not fetch.fetch(self.imap_account, None) is None:
            raise AssertionError
        elif not fetch.fetch(self.imap_account, []) is None:
            raise AssertionError

    def test_get_charset(self):
        multipart_mail = copy.deepcopy(self.reference_mail)
        multipart_mail['parts'].append({'content_type':'img/png', 
         'data':'xxxxxx', 
         'filename':'IMGTEST'})
        mail = email.message_from_string(self.reference_mail['parts'][0]['data'])
        assert fetch.get_charset(mail) == 'windows-1252'

    def test_read(self):
        self.imap_account = imaplib.IMAP4_SSL()
        mails = list(fetch.read((self.imap_account), 1, directory='INBOX'))
        for mail in mails:
            for header_name, header_value in mail['headers'].items():
                assert self.reference_mail['headers'][header_name] == header_value

            assert len(mail['parts']) == len(self.reference_mail['parts'])

    def test_read_multipart(self):
        self.imap_account = imaplib.IMAP4_SSL()
        mails = fetch.read((self.imap_account), 1, directory='INBOX')
        for mail in mails:
            for header_name, header_value in mail['headers'].items():
                assert self.reference_mail['headers'][header_name] == header_value

            assert len(mail['parts']) == len(self.reference_mail['parts'])

    def test_fetch_cli_tool(self):
        const.DEFAULT_CONFIG_FILE = 'config-example.ini'
        sys.argv = [
         'imap-cli-read', '-c', 'config-example.ini', '1']
        if not fetch.main() == 0:
            raise AssertionError
        else:
            sys.argv = [
             'imap-cli-read', '-d', 'INBOX', '1']
            assert fetch.main() == 0
            sys.argv = [
             'imap-cli-read', '-d', 'INBOX', '1', '-s', '.']
            assert fetch.main() == 0