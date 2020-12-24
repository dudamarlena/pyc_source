# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/twiddler/output/emailer.py
# Compiled at: 2008-07-24 14:48:01
from email.Charset import Charset, QP
from email.MIMEMultipart import MIMEMultipart
from email.Utils import make_msgid, formatdate
from new import classobj
from smtplib import SMTP
from twiddler.interfaces import IOutput
from twiddler.output.default import _render
from twiddler.output.MTMultipart import MTMultipart
from twiddler.output.MTText import MTText
from zope.interface import implements
default_charset = Charset('utf-8')
default_charset.body_encoding = QP

class DummySMTP:

    def __init__(self, *args):
        pass

    def sendmail(self, mfrom, mto, msgstr):
        print 'Dummy SMTP send from %r to %r' % (mfrom, mto)
        print msgstr

    def quit(self):
        pass


class Email:
    implements(IOutput)

    def __init__(self, smtp_host='localhost', smtp_port='25', mfrom=None, mto=None, mcc=None, mbcc=None, subject=None, content_type='text/plain', charset=default_charset, headers=None):
        self.charset = charset
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.mfrom = mfrom
        self.mto = mto
        self.mcc = mcc
        self.mbcc = mbcc
        self.subject = subject
        self.content_type = content_type
        self.headers = headers or {}

    def _process(self, root, kw):
        charset = kw.get('charset', self.charset)
        content_type = kw.get('content_type', self.content_type)
        output = []
        _render(output, root._root, {})
        text = ('').join(output)
        msg = MTText(text.replace('\r', ''), content_type.split('/')[1], charset)
        headers = {}
        values = {}
        headers['Date'] = formatdate()
        headers['Message-ID'] = make_msgid()
        headers.update(self.headers)
        headers_param = kw.get('headers', {})
        headers.update(headers_param)
        for (key, header) in (('mfrom', 'From'),
         ('mto', 'To'),
         ('mcc', 'Cc'),
         ('mbcc', 'Bcc'),
         ('subject', 'Subject')):
            value = kw.get(key, headers_param.get(header, getattr(self, key) or headers.get(header)))
            if value is not None:
                values[key] = value
                if isinstance(value, tuple) or isinstance(value, list):
                    value = (', ').join(value)
                headers[header] = value

        errors = []
        for param in ('mfrom', 'mto', 'subject'):
            if not values.get(param):
                errors.append(param)

        if errors:
            raise TypeError('The following parameters were required by not specified: ' + (', ').join(errors))
        keys = headers.keys()
        keys.sort()
        return (msg, values, [ (key, headers[key]) for key in keys ])

    def _send(self, mfrom, mto, msg):
        if isinstance(self.smtp_host, classobj):
            klass = self.smtp_host
        else:
            klass = SMTP
        server = klass(self.smtp_host, self.smtp_port)
        server.sendmail(mfrom, mto, msg.as_string())
        server.quit()

    def __call__(self, root, *args, **kw):
        if kw.get('as_message'):
            (msg, values, headers) = self._process(root, kw)
            multipart_kw = {}
            subtype = kw.get('subtype')
            if subtype:
                multipart_kw['_subtype'] = subtype
            boundary = kw.get('boundary')
            if boundary:
                multipart_kw['boundary'] = boundary
            multipart = MTMultipart(self, values['mfrom'], values['mto'], **multipart_kw)
            multipart.set_charset(msg.get_charset())
            for (header, value) in headers:
                multipart[header] = value

            multipart.attach(msg)
            return multipart
        else:
            (msg, values, headers) = self._process(root, kw)
            for (header, value) in headers:
                msg[header] = value

            self._send(values['mfrom'], values['mto'], msg)