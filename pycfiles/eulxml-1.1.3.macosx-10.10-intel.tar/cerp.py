# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rsutton/workarea/env/eulxml/lib/python2.7/site-packages/eulxml/xmlmap/cerp.py
# Compiled at: 2016-05-23 17:04:57
from __future__ import unicode_literals
import codecs, datetime, email, logging, os, six
from eulxml import xmlmap
from eulxml.utils.compat import u
logger = logging.getLogger(__name__)

class _BaseCerp(xmlmap.XmlObject):
    """Common CERP namespace declarations"""
    ROOT_NS = b'http://www.archives.ncdcr.gov/mail-account'
    ROOT_NAMESPACES = {b'xm': ROOT_NS}


class Parameter(_BaseCerp):
    ROOT_NAME = b'Parameter'
    name = xmlmap.StringField(b'xm:Name')
    value = xmlmap.StringField(b'xm:Value')

    def __str__(self):
        return b'%s=%s' % (self.name, self.value)

    def __repr__(self):
        return b'<%s %s>' % (self.__class__.__name__, str(self))


class Header(_BaseCerp):
    ROOT_NAME = b'Header'
    name = xmlmap.StringField(b'xm:Name')
    value = xmlmap.StringField(b'xm:Value')
    comments = xmlmap.StringListField(b'xm:Comments')

    def __str__(self):
        return b'%s: %s' % (self.name, self.value)

    def __repr__(self):
        return b'<%s %s>' % (self.__class__.__name__, self.name)


class _BaseBody(_BaseCerp):
    """Common email header elements"""
    content_type_list = xmlmap.StringListField(b'xm:ContentType')
    charset_list = xmlmap.StringListField(b'xm:Charset')
    content_name_list = xmlmap.StringListField(b'xm:ContentName')
    content_type_comments_list = xmlmap.StringListField(b'xm:ContentTypeComments')
    content_type_param_list = xmlmap.NodeListField(b'xm:ContentTypeParam', Parameter)
    transfer_encoding_list = xmlmap.StringListField(b'xm:TransferEncoding')
    transfer_encoding_comments_list = xmlmap.StringListField(b'xm:TransferEncodingComments')
    content_id_list = xmlmap.StringListField(b'xm:ContentId')
    content_id_comments_list = xmlmap.StringListField(b'xm:ContentIdComments')
    description_list = xmlmap.StringListField(b'xm:Description')
    description_comments_list = xmlmap.StringListField(b'xm:DescriptionComments')
    disposition_list = xmlmap.StringListField(b'xm:Disposition')
    disposition_file_name_list = xmlmap.StringListField(b'xm:DispositionFileName')
    disposition_comments_list = xmlmap.StringListField(b'xm:DispositionComments')
    disposition_params = xmlmap.NodeListField(b'xm:DispositionParams', Parameter)
    other_mime_headers = xmlmap.NodeListField(b'xm:OtherMimeHeader', Header)


class Hash(_BaseCerp):
    ROOT_NAME = b'Hash'
    HASH_FUNCTION_CHOICES = [b'MD5', b'WHIRLPOOL', b'SHA1', b'SHA224',
     b'SHA256', b'SHA384', b'SHA512', b'RIPEMD160']
    value = xmlmap.StringField(b'xm:Value')
    function = xmlmap.StringField(b'xm:Function', choices=HASH_FUNCTION_CHOICES)

    def __str__(self):
        return self.value

    def __repr__(self):
        return b'<%s %s>' % (self.__class__.__name__, self.function)


class _BaseExternal(_BaseCerp):
    """Common external entity reference elements"""
    EOL_CHOICES = [
     b'CR', b'LF', b'CRLF']
    rel_path = xmlmap.StringField(b'xm:RelPath')
    eol = xmlmap.StringField(b'xm:Eol', choices=EOL_CHOICES)
    hash = xmlmap.NodeField(b'xm:Hash', Hash)


class _BaseContent(_BaseCerp):
    """Common content encoding elements"""
    charset_list = xmlmap.StringListField(b'xm:CharSet')
    transfer_encoding_list = xmlmap.StringListField(b'xm:TransferEncoding')


class BodyContent(_BaseContent):
    ROOT_NAME = b'BodyContent'
    content = xmlmap.StringField(b'xm:Content')


class ExtBodyContent(_BaseExternal, _BaseContent):
    ROOT_NAME = b'ExtBodyContent'
    local_id = xmlmap.IntegerField(b'xm:LocalId')
    xml_wrapped = xmlmap.SimpleBooleanField(b'xm:XMLWrapped', true=b'1', false=b'0')


class SingleBody(_BaseBody):
    ROOT_NAME = b'SingleBody'
    body_content = xmlmap.NodeField(b'xm:BodyContent', BodyContent)
    ext_body_content = xmlmap.NodeField(b'xm:ExtBodyContent', ExtBodyContent)
    child_message = xmlmap.NodeField(b'xm:ChildMessage', None)

    @property
    def content(self):
        return self.body_content or self.ext_body_content or self.child_message

    phantom_body = xmlmap.StringField(b'xm:PhantomBody')


class MultiBody(_BaseCerp):
    ROOT_NAME = b'MultiBody'
    preamble = xmlmap.StringField(b'xm:Preamble')
    epilogue = xmlmap.StringField(b'xm:Epilogue')
    single_body = xmlmap.NodeField(b'xm:SingleBody', SingleBody)
    multi_body = xmlmap.NodeField(b'xm:MultiBody', b'self')

    @property
    def body(self):
        return self.single_body or self.multi_body


class Incomplete(_BaseCerp):
    ROOT_NAME = b'Incomplete'
    error_type = xmlmap.StringField(b'xm:ErrorType')
    error_location = xmlmap.StringField(b'xm:ErrorLocation')

    def __repr__(self):
        return b'<%s %s>' % (self.__class__.__name__, self.error_type)


class _BaseMessage(_BaseCerp):
    """Common message elements"""
    local_id = xmlmap.IntegerField(b'xm:LocalId')
    message_id = xmlmap.StringField(b'xm:MessageId')
    message_id_supplied = xmlmap.SimpleBooleanField(b'xm:MessageId/@Supplied', true=b'1', false=None)
    mime_version = xmlmap.StringField(b'xm:MimeVersion')
    orig_date_list = xmlmap.StringListField(b'xm:OrigDate')
    from_list = xmlmap.StringListField(b'xm:From')
    sender_list = xmlmap.StringListField(b'xm:Sender')
    to_list = xmlmap.StringListField(b'xm:To')
    cc_list = xmlmap.StringListField(b'xm:Cc')
    bcc_list = xmlmap.StringListField(b'xm:Bcc')
    in_reply_to_list = xmlmap.StringListField(b'xm:InReplyTo')
    references_list = xmlmap.StringListField(b'xm:References')
    subject_list = xmlmap.StringListField(b'xm:Subject')
    comments_list = xmlmap.StringListField(b'xm:Comments')
    keywords_list = xmlmap.StringListField(b'xm:Keywords')
    headers = xmlmap.NodeListField(b'xm:Header', Header)
    single_body = xmlmap.NodeField(b'xm:SingleBody', SingleBody)
    multi_body = xmlmap.NodeField(b'xm:MultiBody', MultiBody)

    @property
    def body(self):
        return self.single_body or self.multi_body

    incomplete_list = xmlmap.NodeField(b'xm:Incomplete', Incomplete)

    def __repr__(self):
        return b'<%s %s>' % (self.__class__.__name__,
         self.message_id or self.local_id or b'(no id)')


class Message(_BaseMessage, _BaseExternal):
    """A single email message in a :class:`Folder`."""
    ROOT_NAME = b'Message'
    STATUS_FLAG_CHOICES = [b'Seen', b'Answered', b'Flagged', b'Deleted',
     b'Draft', b'Recent']
    status_flags = xmlmap.StringListField(b'xm:StatusFlag', choices=STATUS_FLAG_CHOICES)

    @classmethod
    def from_email_message(cls, message, local_id=None):
        """
        Convert an :class:`email.message.Message` or compatible message
        object into a CERP XML :class:`eulxml.xmlmap.cerp.Message`. If an
        id is specified, it will be stored in the Message <LocalId>.

        :param message: `email.message.Message` object
        :param id: optional message id to be set as `local_id`

        :returns: :class:`eulxml.xmlmap.cerp.Message` instance populated
            with message information

        """
        result = cls()
        if local_id is not None:
            result.local_id = id
        message_id = message.get(b'Message-Id')
        if message_id:
            result.message_id_supplied = True
            result.message_id = message_id
        result.mime_version = message.get(b'MIME-Version')
        dates = message.get_all(b'Date', [])
        result.orig_date_list.extend([ parse_mail_date(d) for d in dates ])
        result.from_list.extend(message.get_all(b'From', []))
        result.sender_list.extend(message.get_all(b'From', []))
        try:
            result.to_list.extend(message.get_all(b'To', []))
        except UnicodeError:
            print repr(message[b'To'])
            raise

        result.cc_list.extend(message.get_all(b'Cc', []))
        result.bcc_list.extend(message.get_all(b'Bcc', []))
        result.in_reply_to_list.extend(message.get_all(b'In-Reply-To', []))
        result.references_list.extend(message.get_all(b'References', []))
        result.subject_list.extend(message.get_all(b'Subject', []))
        result.comments_list.extend(message.get_all(b'Comments', []))
        result.keywords_list.extend(message.get_all(b'Keywords', []))
        headers = [ Header(name=key, value=val) for key, val in message.items() ]
        result.headers.extend(headers)
        if not message.is_multipart():
            result.create_single_body()
            if message[b'Content-Type']:
                result.single_body.content_type_list.append(message.get_content_type())
            if message.get_content_charset():
                result.single_body.charset_list.append(message.get_content_charset())
            if message.get_filename():
                result.single_body.content_name_list.append(message.get_filename())
            result.single_body.create_body_content()
            payload = message.get_payload(decode=False)
            if isinstance(payload, six.binary_type):
                charset = message.get_charset()
                if charset is not None:
                    charset_decoder = codecs.getdecoder(str(charset))
                    payload, length = charset_decoder(payload)
                else:
                    payload = u(payload)
            control_char_map = dict.fromkeys(range(32))
            for i in [9, 10, 13]:
                del control_char_map[i]

            payload = u(payload).translate(control_char_map)
            result.single_body.body_content.content = payload
        else:
            logger.warn(b'CERP conversion does not yet handle multipart')
        result.eol = EOLMAP[os.linesep]
        return result


class ChildMessage(_BaseMessage):
    ROOT_NAME = b'ChildMessage'


SingleBody.child_message.node_class = ChildMessage

class Mbox(_BaseExternal):
    ROOT_NAME = b'Mbox'


class Folder(_BaseCerp):
    """A single email folder in an :class:`Account`, composed of multiple
    :class:`Message` objects and associated metadata."""
    ROOT_NAME = b'Folder'
    name = xmlmap.StringField(b'xm:Name')
    messages = xmlmap.NodeListField(b'xm:Message', Message)
    subfolders = xmlmap.NodeListField(b'xm:Folder', b'self')
    mboxes = xmlmap.NodeListField(b'xm:Mbox', Mbox)

    def __repr__(self):
        return b'<%s %s>' % (self.__class__.__name__, self.name)


class ReferencesAccount(_BaseCerp):
    ROOT_NAME = b'ReferencesAccount'
    REF_TYPE_CHOICES = [b'PreviousContent', b'SubsequentContent',
     b'Supplemental', b'SeeAlso', b'SeeInstead']
    href = xmlmap.StringField(b'xm:Href')
    email_address = xmlmap.StringField(b'xm:EmailAddress')
    reference_type = xmlmap.StringField(b'xm:RefType', choices=REF_TYPE_CHOICES)


class Account(_BaseCerp):
    """A single email account associated with a single email address and
    composed of multiple :class:`Folder` objects and additional metadata."""
    ROOT_NAME = b'Account'
    XSD_SCHEMA = b'http://www.history.ncdcr.gov/SHRAB/ar/emailpreservation/mail-account/mail-account.xsd'
    email_address = xmlmap.StringField(b'xm:EmailAddress')
    global_id = xmlmap.StringField(b'xm:GlobalId')
    references_accounts = xmlmap.NodeListField(b'xm:ReferencesAccount', ReferencesAccount)
    folders = xmlmap.NodeListField(b'xm:Folder', Folder)

    def __repr__(self):
        return b'<%s %s>' % (self.__class__.__name__,
         self.global_id or self.email_address or b'(no id)')


def parse_mail_date(datestr):
    """Helper method used by :meth:`Message.from_email_message` to
    convert dates from rfc822 format to iso 8601.

    :param datestr: string containing a date in rfc822 format
    :returns: string with date in iso 8601 format
    """
    time_tuple = email.utils.parsedate_tz(datestr)
    if time_tuple is None:
        return datestr
    else:
        dt = datetime.datetime.fromtimestamp(email.utils.mktime_tz(time_tuple))
        return dt.isoformat()


EOLMAP = {b'\r': b'CR', 
   b'\n': b'LF', 
   b'\r\n': b'CRLF'}