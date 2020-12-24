# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/core/mail/message.py
# Compiled at: 2018-07-11 18:15:30
from __future__ import unicode_literals
import mimetypes, os, random, sys, time
from email import charset as Charset, encoders as Encoders
from email.generator import Generator
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.header import Header
from email.utils import formatdate, getaddresses, formataddr, parseaddr
from django.conf import settings
from django.core.mail.utils import DNS_NAME
from django.utils.encoding import force_text
from django.utils import six
Charset.add_charset(b'utf-8', Charset.SHORTEST, None, b'utf-8')
DEFAULT_ATTACHMENT_MIME_TYPE = b'application/octet-stream'

class BadHeaderError(ValueError):
    pass


def make_msgid(idstring=None):
    """Returns a string suitable for RFC 2822 compliant Message-ID, e.g:

    <20020201195627.33539.96671@nightshade.la.mastaler.com>

    Optional idstring if given is a string used to strengthen the
    uniqueness of the message id.
    """
    timeval = time.time()
    utcdate = time.strftime(b'%Y%m%d%H%M%S', time.gmtime(timeval))
    try:
        pid = os.getpid()
    except AttributeError:
        pid = 1

    randint = random.randrange(100000)
    if idstring is None:
        idstring = b''
    else:
        idstring = b'.' + idstring
    idhost = DNS_NAME
    msgid = b'<%s.%s.%s%s@%s>' % (utcdate, pid, randint, idstring, idhost)
    return msgid


ADDRESS_HEADERS = set([
 b'from',
 b'sender',
 b'reply-to',
 b'to',
 b'cc',
 b'bcc',
 b'resent-from',
 b'resent-sender',
 b'resent-to',
 b'resent-cc',
 b'resent-bcc'])

def forbid_multi_line_headers(name, val, encoding):
    """Forbids multi-line headers, to prevent header injection."""
    encoding = encoding or settings.DEFAULT_CHARSET
    val = force_text(val)
    if b'\n' in val or b'\r' in val:
        raise BadHeaderError(b"Header values can't contain newlines (got %r for header %r)" % (val, name))
    try:
        val.encode(b'ascii')
    except UnicodeEncodeError:
        if name.lower() in ADDRESS_HEADERS:
            val = (b', ').join(sanitize_address(addr, encoding) for addr in getaddresses((val,)))
        else:
            val = Header(val, encoding).encode()

    if name.lower() == b'subject':
        val = Header(val).encode()
    return (
     str(name), val)


def sanitize_address(addr, encoding):
    if isinstance(addr, six.string_types):
        addr = parseaddr(force_text(addr))
    nm, addr = addr
    try:
        nm = Header(nm, encoding).encode()
    except UnicodeEncodeError:
        nm = Header(nm, b'utf-8').encode()

    try:
        addr.encode(b'ascii')
    except UnicodeEncodeError:
        if b'@' in addr:
            localpart, domain = addr.split(b'@', 1)
            localpart = str(Header(localpart, encoding))
            domain = domain.encode(b'idna').decode(b'ascii')
            addr = (b'@').join([localpart, domain])
        else:
            addr = Header(addr, encoding).encode()

    return formataddr((nm, addr))


class SafeMIMEText(MIMEText):

    def __init__(self, text, subtype, charset):
        self.encoding = charset
        MIMEText.__init__(self, text, subtype, charset)

    def __setitem__(self, name, val):
        name, val = forbid_multi_line_headers(name, val, self.encoding)
        MIMEText.__setitem__(self, name, val)

    def as_string(self, unixfrom=False):
        """Return the entire formatted message as a string.
        Optional `unixfrom' when True, means include the Unix From_ envelope
        header.

        This overrides the default as_string() implementation to not mangle
        lines that begin with 'From '. See bug #13433 for details.
        """
        fp = six.StringIO()
        g = Generator(fp, mangle_from_=False)
        if sys.version_info < (2, 6, 6) and isinstance(self._payload, six.text_type):
            self._payload = self._payload.encode(self._charset.output_charset)
        g.flatten(self, unixfrom=unixfrom)
        return fp.getvalue()


class SafeMIMEMultipart(MIMEMultipart):

    def __init__(self, _subtype=b'mixed', boundary=None, _subparts=None, encoding=None, **_params):
        self.encoding = encoding
        MIMEMultipart.__init__(self, _subtype, boundary, _subparts, **_params)

    def __setitem__(self, name, val):
        name, val = forbid_multi_line_headers(name, val, self.encoding)
        MIMEMultipart.__setitem__(self, name, val)

    def as_string(self, unixfrom=False):
        """Return the entire formatted message as a string.
        Optional `unixfrom' when True, means include the Unix From_ envelope
        header.

        This overrides the default as_string() implementation to not mangle
        lines that begin with 'From '. See bug #13433 for details.
        """
        fp = six.StringIO()
        g = Generator(fp, mangle_from_=False)
        g.flatten(self, unixfrom=unixfrom)
        return fp.getvalue()


class EmailMessage(object):
    """
    A container for email information.
    """
    content_subtype = b'plain'
    mixed_subtype = b'mixed'
    encoding = None

    def __init__(self, subject=b'', body=b'', from_email=None, to=None, bcc=None, connection=None, attachments=None, headers=None, cc=None):
        """
        Initialize a single email message (which can be sent to multiple
        recipients).

        All strings used to create the message can be unicode strings
        (or UTF-8 bytestrings). The SafeMIMEText class will handle any
        necessary encoding conversions.
        """
        if to:
            assert not isinstance(to, six.string_types), b'"to" argument must be a list or tuple'
            self.to = list(to)
        else:
            self.to = []
        if cc:
            assert not isinstance(cc, six.string_types), b'"cc" argument must be a list or tuple'
            self.cc = list(cc)
        else:
            self.cc = []
        if bcc:
            assert not isinstance(bcc, six.string_types), b'"bcc" argument must be a list or tuple'
            self.bcc = list(bcc)
        else:
            self.bcc = []
        self.from_email = from_email or settings.DEFAULT_FROM_EMAIL
        self.subject = subject
        self.body = body
        self.attachments = attachments or []
        self.extra_headers = headers or {}
        self.connection = connection

    def get_connection(self, fail_silently=False):
        from django.core.mail import get_connection
        if not self.connection:
            self.connection = get_connection(fail_silently=fail_silently)
        return self.connection

    def message(self):
        encoding = self.encoding or settings.DEFAULT_CHARSET
        msg = SafeMIMEText(self.body, self.content_subtype, encoding)
        msg = self._create_message(msg)
        msg[b'Subject'] = self.subject
        msg[b'From'] = self.extra_headers.get(b'From', self.from_email)
        msg[b'To'] = self.extra_headers.get(b'To', (b', ').join(self.to))
        if self.cc:
            msg[b'Cc'] = (b', ').join(self.cc)
        header_names = [ key.lower() for key in self.extra_headers ]
        if b'date' not in header_names:
            msg[b'Date'] = formatdate()
        if b'message-id' not in header_names:
            msg[b'Message-ID'] = make_msgid()
        for name, value in self.extra_headers.items():
            if name.lower() in ('from', 'to'):
                continue
            msg[name] = value

        return msg

    def recipients(self):
        """
        Returns a list of all recipients of the email (includes direct
        addressees as well as Cc and Bcc entries).
        """
        return self.to + self.cc + self.bcc

    def send(self, fail_silently=False):
        """Sends the email message."""
        if not self.recipients():
            return 0
        return self.get_connection(fail_silently).send_messages([self])

    def attach(self, filename=None, content=None, mimetype=None):
        """
        Attaches a file with the given filename and content. The filename can
        be omitted and the mimetype is guessed, if not provided.

        If the first parameter is a MIMEBase subclass it is inserted directly
        into the resulting message attachments.
        """
        if not (isinstance(filename, MIMEBase) and content == mimetype == None):
            raise AssertionError
            self.attachments.append(filename)
        else:
            assert content is not None
            self.attachments.append((filename, content, mimetype))
        return

    def attach_file(self, path, mimetype=None):
        """Attaches a file from the filesystem."""
        filename = os.path.basename(path)
        with open(path, b'rb') as (f):
            content = f.read()
        self.attach(filename, content, mimetype)

    def _create_message(self, msg):
        return self._create_attachments(msg)

    def _create_attachments(self, msg):
        if self.attachments:
            encoding = self.encoding or settings.DEFAULT_CHARSET
            body_msg = msg
            msg = SafeMIMEMultipart(_subtype=self.mixed_subtype, encoding=encoding)
            if self.body:
                msg.attach(body_msg)
            for attachment in self.attachments:
                if isinstance(attachment, MIMEBase):
                    msg.attach(attachment)
                else:
                    msg.attach(self._create_attachment(*attachment))

        return msg

    def _create_mime_attachment(self, content, mimetype):
        """
        Converts the content, mimetype pair into a MIME attachment object.
        """
        basetype, subtype = mimetype.split(b'/', 1)
        if basetype == b'text':
            encoding = self.encoding or settings.DEFAULT_CHARSET
            attachment = SafeMIMEText(content, subtype, encoding)
        else:
            attachment = MIMEBase(basetype, subtype)
            attachment.set_payload(content)
            Encoders.encode_base64(attachment)
        return attachment

    def _create_attachment(self, filename, content, mimetype=None):
        """
        Converts the filename, content, mimetype triple into a MIME attachment
        object.
        """
        if mimetype is None:
            mimetype, _ = mimetypes.guess_type(filename)
            if mimetype is None:
                mimetype = DEFAULT_ATTACHMENT_MIME_TYPE
        attachment = self._create_mime_attachment(content, mimetype)
        if filename:
            try:
                filename.encode(b'ascii')
            except UnicodeEncodeError:
                if not six.PY3:
                    filename = filename.encode(b'utf-8')
                filename = (
                 b'utf-8', b'', filename)

            attachment.add_header(b'Content-Disposition', b'attachment', filename=filename)
        return attachment


class EmailMultiAlternatives(EmailMessage):
    """
    A version of EmailMessage that makes it easy to send multipart/alternative
    messages. For example, including text and HTML versions of the text is
    made easier.
    """
    alternative_subtype = b'alternative'

    def __init__(self, subject=b'', body=b'', from_email=None, to=None, bcc=None, connection=None, attachments=None, headers=None, alternatives=None, cc=None):
        """
        Initialize a single email message (which can be sent to multiple
        recipients).

        All strings used to create the message can be unicode strings (or UTF-8
        bytestrings). The SafeMIMEText class will handle any necessary encoding
        conversions.
        """
        super(EmailMultiAlternatives, self).__init__(subject, body, from_email, to, bcc, connection, attachments, headers, cc)
        self.alternatives = alternatives or []

    def attach_alternative(self, content, mimetype):
        """Attach an alternative content representation."""
        assert content is not None
        assert mimetype is not None
        self.alternatives.append((content, mimetype))
        return

    def _create_message(self, msg):
        return self._create_attachments(self._create_alternatives(msg))

    def _create_alternatives(self, msg):
        encoding = self.encoding or settings.DEFAULT_CHARSET
        if self.alternatives:
            body_msg = msg
            msg = SafeMIMEMultipart(_subtype=self.alternative_subtype, encoding=encoding)
            if self.body:
                msg.attach(body_msg)
            for alternative in self.alternatives:
                msg.attach(self._create_mime_attachment(*alternative))

        return msg