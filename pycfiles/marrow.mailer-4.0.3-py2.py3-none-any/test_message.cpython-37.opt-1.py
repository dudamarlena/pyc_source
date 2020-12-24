# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /test/test_message.py
# Compiled at: 2019-09-15 20:05:09
# Size of source mod 2**32: 17803 bytes
"""Test the TurboMail Message class."""
from __future__ import print_function, unicode_literals
import calendar
from datetime import datetime, timedelta
import email, sys, re, time, pytest, base64
from unittest import TestCase
from email.mime.text import MIMEText
from email.utils import formatdate, parsedate_tz
from marrow.mailer import Message
from marrow.mailer.address import AddressList
from marrow.util.compat import basestring, unicode

class TestBasicMessage(TestCase):
    __doc__ = 'Test the basic output of the Message class.'
    gif = b'R0lGODlhAQABAJEAAAAAAAAAAP4BAgAAACH5BAQUAP8ALAAAAAABAAEAAAICRAEAOw==\n'

    def build_message(self, **kw):
        return Message(author=('Author', 'author@example.com'), 
         to=('Recipient', 'recipient@example.com'), 
         subject='Test message subject.', 
         plain='This is a test message plain text body.', **kw)

    def test_missing_values(self):
        message = Message()
        with pytest.raises(ValueError):
            unicode(message)
        message.author = 'bob.dole@whitehouse.gov'
        with pytest.raises(ValueError):
            unicode(message)
        message.subject = 'Attn: Bob Dole'
        with pytest.raises(ValueError):
            unicode(message)
        message.to = 'user@example.com'
        with pytest.raises(ValueError):
            unicode(message)
        message.plain = 'Testing!'
        try:
            unicode(message)
        except ValueError:
            assert False, 'Message should be valid.'

    def test_message_id(self):
        msg = self.build_message()
        assert msg._id == None
        id_ = msg.id
        assert msg._id == id_
        assert msg.id == id_

    def test_missing_author(self):
        message = self.build_message()
        message.author = []
        with pytest.raises(ValueError):
            message.envelope

    def test_message_properties(self):
        message = self.build_message()
        assert message.author == [('Author', 'author@example.com')]
        assert unicode(message.author) == 'Author <author@example.com>'
        assert isinstance(message.mime, MIMEText)

    def test_message_string_with_basic(self):
        msg = email.message_from_string(str(self.build_message(encoding='iso-8859-1')))
        assert msg['From'] == 'Author <author@example.com>'
        assert msg['To'] == 'Recipient <recipient@example.com>'
        assert msg['Subject'] == 'Test message subject.'
        assert msg.get_payload() == 'This is a test message plain text body.'

    def test_message_recipients_and_addresses(self):
        message = self.build_message()
        message.cc = 'cc@example.com'
        message.bcc = 'bcc@example.com'
        message.sender = 'sender@example.com'
        message.reply = 'replyto@example.com'
        message.notify = 'disposition@example.com'
        msg = email.message_from_string(unicode(message))
        assert msg['cc'] == 'cc@example.com'
        assert msg['bcc'] == None
        assert msg['sender'] == 'sender@example.com'
        assert msg['reply-to'] == 'replyto@example.com'
        assert msg['disposition-notification-to'] == 'disposition@example.com'

    def test_mime_generation_plain(self):
        message = self.build_message()
        mime = message.mime
        assert message.mime is mime
        message.subject = 'Test message subject.'
        assert message.mime is not mime

    def test_mime_generation_rich(self):
        message = self.build_message()
        message.plain = 'Hello world.'
        message.rich = 'Farewell cruel world.'
        assert 'Hello world.' in str(message)
        assert 'Farewell cruel world.' in str(message)

    def test_mime_generation_rich_embedded(self):
        message = self.build_message()
        message.plain = 'Hello world.'
        message.rich = 'Farewell cruel world.'
        message.attach('hello.txt', b'Fnord.', 'text', 'plain', True)
        assert 'Hello world.' in unicode(message)
        assert 'Farewell cruel world.' in unicode(message)
        assert 'hello.txt' in unicode(message)
        assert 'Rm5vcmQu' in unicode(message)

    def test_mime_attachments(self):
        message = self.build_message()
        message.plain = 'Hello world.'
        message.rich = 'Farewell cruel world.'
        message.attach('hello.txt', b'Fnord.')
        assert 'Hello world.' in unicode(message)
        assert 'Farewell cruel world.' in unicode(message)
        assert 'hello.txt' in unicode(message)
        assert 'Rm5vcmQu' in unicode(message)
        assert 'text/plain\n' in unicode(message)

    def test_mime_attachments_unknown(self):
        message = self.build_message()
        message.plain = 'Hello world.'
        message.rich = 'Farewell cruel world.'
        message.attach('test.xbin', b'Word.')
        assert 'test.xbin' in str(message)
        assert 'application/octet-stream' in str(message)
        with pytest.raises(TypeError):
            message.attach('foo', object())

    def test_non_ascii_attachment_names(self):
        message = self.build_message()
        message.plain = 'Hello world.'
        message.rich = 'Farewell cruel world.'
        message.attach('☃.txt', b'unicode snowman', filename_charset='utf-8')
        assert 'Hello world.' in unicode(message)
        if not 'Farewell cruel world.' in unicode(message):
            raise AssertionError
        elif sys.version_info < (3, 0) and not 'filename*="utf-8\'\'%E2%98%83.txt"' in unicode(message):
            raise AssertionError
        else:
            assert "filename*=utf-8''%E2%98%83.txt" in unicode(message)
        assert 'dW5pY29kZSBzbm93bWFu' in unicode(message)

    def test_language_specification_and_charset_for_attachment_name(self):
        message = self.build_message()
        message.plain = 'Hello world.'
        message.rich = 'Farewell cruel world.'
        message.attach('☃.txt', b'unicode snowman', filename_charset='utf-8', filename_language='en-us')
        assert 'Hello world.' in unicode(message)
        if not 'Farewell cruel world.' in unicode(message):
            raise AssertionError
        elif sys.version_info < (3, 0) and not 'filename*="utf-8\'en-us\'%E2%98%83.txt"' in unicode(message):
            raise AssertionError
        else:
            assert "filename*=utf-8'en-us'%E2%98%83.txt" in unicode(message)
        assert 'dW5pY29kZSBzbm93bWFu' in unicode(message)

    def test_language_specification_but_no_charset_for_attachment_name(self):
        message = self.build_message()
        message.plain = 'Hello world.'
        message.rich = 'Farewell cruel world.'
        message.attach('☃.txt', b'unicode snowman', filename_language='en-us')
        assert 'Hello world.' in unicode(message)
        if not 'Farewell cruel world.' in unicode(message):
            raise AssertionError
        elif sys.version_info < (3, 0) and not 'filename*="utf-8\'en-us\'%E2%98%83.txt"' in unicode(message):
            raise AssertionError
        else:
            assert "filename*=utf-8'en-us'%E2%98%83.txt" in unicode(message)
        assert 'dW5pY29kZSBzbm93bWFu' in unicode(message)

    def test_mime_attachments_file(self):
        import tempfile
        message = self.build_message()
        message.plain = 'Hello world.'
        message.rich = 'Farewell cruel world.'
        with tempfile.NamedTemporaryFile(mode='wb') as (fh):
            fh.write(b'foo')
            fh.flush()
            message.attach(fh.name)
            assert 'application/octet-stream' in str(message)
            assert 'Zm9v' in str(message)

    def test_mime_attachments_filelike(self):

        class Mock(object):

            def read(self):
                return b'foo'

        message = self.build_message()
        message.plain = 'Hello world.'
        message.rich = 'Farewell cruel world.'
        message.attach('test.xbin', Mock())
        assert 'test.xbin' in str(message)
        assert 'application/octet-stream' in str(message)
        assert 'Zm9v' in str(message)

    def test_mime_embed_gif_file(self):
        import tempfile
        message = self.build_message()
        message.plain = 'Hello world.'
        message.rich = 'Farewell cruel world.'
        with tempfile.NamedTemporaryFile() as (fh):
            fh.write(base64.b64decode(self.gif))
            fh.flush()
            message.embed(fh.name)
            result = bytes(message)
            assert b'image/gif' in result
            assert b'R0lGODlh' in result

    def test_mime_embed_gif_bytes(self):
        message = self.build_message()
        message.plain = 'Hello world.'
        message.rich = 'Farewell cruel world.'
        message.embed('test.gif', base64.b64decode(self.gif))
        result = bytes(message)
        assert b'image/gif' in result
        assert b'R0lGODlh' in result

        class Mock(object):

            def read(s):
                return base64.b64decode(self.gif)

        message = self.build_message()
        message.plain = 'Hello world.'
        message.rich = 'Farewell cruel world.'
        message.embed('test.gif', Mock())
        result = bytes(message)
        assert b'image/gif' in result
        assert b'R0lGODlh' in result

    def test_mime_embed_failures(self):
        message = self.build_message()
        message.plain = 'Hello world.'
        message.rich = 'Farewell cruel world.'
        with pytest.raises(TypeError):
            message.embed('test.gif', object())

    def test_that_add_header_and_collapse_header_are_inverses_ascii_filename(self):
        message = self.build_message()
        message.plain = 'Hello world.'
        message.rich = 'Farewell cruel world.'
        message.attach('wat.txt', b'not a unicode snowman')
        attachment = message.attachments[0]
        filename = attachment.get_filename()
        assert filename == 'wat.txt'

    def test_that_add_header_and_collapse_header_are_inverses_non_ascii_filename(self):
        message = self.build_message()
        message.plain = 'Hello world.'
        message.rich = 'Farewell cruel world.'
        message.attach('☃.txt', b'unicode snowman', filename_language='en-us')
        attachment = message.attachments[0]
        filename = attachment.get_param('filename', object(), 'content-disposition')
        if not isinstance(filename, tuple):
            raise AssertionError
        else:
            filename = attachment.get_filename()
            if sys.version_info < (3, 0) and not isinstance(filename, basestring):
                raise AssertionError
            else:
                assert isinstance(filename, str)

    def test_recipients_collection(self):
        message = self.build_message()
        message.cc.append('copied@example.com')
        assert message.recipients.addresses == ['recipient@example.com', 'copied@example.com']

    def test_smtp_from_as_envelope(self):
        message = self.build_message()
        message.sender = 'devnull@example.com'
        assert str(message.envelope) == 'devnull@example.com'

    def test_multiple_authors(self):
        message = self.build_message()
        message.authors = 'authors@example.com'
        assert message.authors == message.author
        message.authors = [
         'bar@example.com', 'baz@example.com']
        message.sender = 'foo@example.com'
        msg = email.message_from_string(str(message))
        from_addresses = re.split(',\\n?\\s+', msg['From'])
        assert from_addresses == ['bar@example.com', 'baz@example.com']

    def test_permit_one_sender_at_most(self):
        with pytest.raises(ValueError):
            message = self.build_message()
            message.sender = AddressList(['bar@example.com', 'baz@example.com'])

    def test_raise_error_for_unknown_kwargs_at_class_instantiation(self):
        with pytest.raises(TypeError):
            Message(invalid_argument=True)

    def test_add_custom_headers_dict(self):
        message = self.build_message()
        message.headers = {'Precedence':'bulk',  'X-User':'Alice'}
        msg = email.message_from_string(str(message))
        assert msg['Precedence'] == 'bulk'
        assert msg['X-User'] == 'Alice'

    def test_add_custom_headers_tuple(self):
        message = self.build_message()
        message.headers = (('Precedence', 'bulk'), ('X-User', 'Alice'))
        msg = email.message_from_string(str(message))
        assert msg['Precedence'] == 'bulk'
        assert msg['X-User'] == 'Alice'

    def test_add_custom_headers_list(self):
        """Test that a custom header (list type) can be attached."""
        message = self.build_message()
        message.headers = [('Precedence', 'bulk'), ('X-User', 'Alice')]
        msg = email.message_from_string(str(message))
        assert msg['Precedence'] == 'bulk'
        assert msg['X-User'] == 'Alice'

    def test_no_sender_header_if_no_sender_required(self):
        message = self.build_message()
        msg = email.message_from_string(str(message))
        assert msg['sender'] is None

    def _date_header_to_utc_datetime(self, date_string):
        """Converts a date_string from the Date header into a naive datetime
                object in UTC."""
        assert date_string != None
        tztime_struct = parsedate_tz(date_string)
        time_tuple, tz_offset = tztime_struct[:9], tztime_struct[9]
        epoch_utc_seconds = calendar.timegm(time_tuple)
        if tz_offset is not None:
            epoch_utc_seconds -= tz_offset
        datetime_obj = datetime.utcfromtimestamp(epoch_utc_seconds)
        return datetime_obj

    def _almost_now(self, date_string):
        """Returns True if the date_string represents a time which is 'almost 
                now'."""
        utc_date = self._date_header_to_utc_datetime(date_string)
        delta = abs(datetime.utcnow() - utc_date)
        return delta < timedelta(seconds=1)

    def test_date_header_added_even_if_date_not_set_explicitely(self):
        message = self.build_message()
        msg = email.message_from_string(str(message))
        assert self._almost_now(msg['Date'])

    def test_date_can_be_set_as_string(self):
        message = self.build_message()
        date_string = 'Fri, 26 Dec 2008 11:19:42 +0530'
        message.date = date_string
        msg = email.message_from_string(str(message))
        assert msg['Date'] == date_string

    def test_date_can_be_set_as_float(self):
        message = self.build_message()
        expected_date = datetime(2008, 12, 26, 12, 55)
        expected_time = time.mktime(expected_date.timetuple())
        message.date = expected_time
        msg = email.message_from_string(str(message))
        header_string = msg['Date']
        header_date = self._date_header_to_utc_datetime(header_string)
        assert header_date == self.localdate_to_utc(expected_date)
        expected_datestring = formatdate(expected_time, localtime=True)
        assert expected_datestring == header_string

    def localdate_to_utc(self, localdate):
        local_epoch_seconds = time.mktime(localdate.timetuple())
        date_string = formatdate(local_epoch_seconds, localtime=True)
        return self._date_header_to_utc_datetime(date_string)

    def test_date_can_be_set_as_datetime(self):
        message = self.build_message()
        expected_date = datetime(2008, 12, 26, 12, 55)
        message.date = expected_date
        msg = email.message_from_string(str(message))
        header_date = self._date_header_to_utc_datetime(msg['Date'])
        assert self.localdate_to_utc(expected_date) == header_date

    def test_date_header_is_set_even_if_reset_to_none(self):
        message = self.build_message()
        message.date = None
        msg = email.message_from_string(str(message))
        assert self._almost_now(msg['Date'])

    def test_recipients_property_includes_cc_and_bcc(self):
        message = self.build_message()
        message.cc = 'cc@example.com'
        message.bcc = 'bcc@example.com'
        expected_recipients = ['recipient@example.com', 'cc@example.com',
         'bcc@example.com']
        recipients = list(map(str, list(message.recipients.addresses)))
        assert recipients == expected_recipients

    def test_can_set_encoding_for_message_explicitely(self):
        message = self.build_message()
        assert 'iso-8859-1' not in unicode(message).lower()
        message.encoding = 'ISO-8859-1'
        msg = email.message_from_string(str(message))
        assert msg['Content-Type'] == 'text/plain; charset="iso-8859-1"'
        assert msg['Content-Transfer-Encoding'] == 'quoted-printable'

    def test_plain_utf8_encoding_uses_qp(self):
        message = self.build_message()
        msg = email.message_from_string(str(message))
        assert msg['Content-Type'] == 'text/plain; charset="utf-8"'
        assert msg['Content-Transfer-Encoding'] == 'quoted-printable'

    def test_callable_bodies(self):
        message = self.build_message()
        message.plain = lambda : 'plain text'
        message.rich = lambda : 'rich text'
        assert 'plain text' in unicode(message)
        assert 'rich text' in unicode(message)