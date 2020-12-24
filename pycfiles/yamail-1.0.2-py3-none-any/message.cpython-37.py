# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/didi/PycharmProjects/nnmail/yamail/message.py
# Compiled at: 2019-11-25 23:08:21
# Size of source mod 2**32: 7100 bytes
import os
from .compat import text_type
from .utils import raw, inline
from .headers import add_subject
from .headers import add_recipients_headers
import email.encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
import mimetypes, base64

def prepare_message(user, useralias, addresses, subject, contents, attachments, headers, encoding, newline_to_break=True):
    """ Prepare a MIME message """
    if isinstance(contents, text_type):
        contents = [
         contents]
    if isinstance(attachments, text_type):
        attachments = [
         attachments]
    if attachments is not None:
        for a in attachments:
            if not os.path.isfile(a):
                raise TypeError("'{0}' is not a valid filepath".format(a))

        contents = attachments if contents is None else contents + attachments
    has_included_images, content_objects = prepare_contents(contents, encoding)
    msg = MIMEMultipart()
    if headers is not None:
        for k, v in headers.items():
            msg[k] = v

    if headers is None or 'Date' not in headers:
        msg['Date'] = formatdate()
    msg_alternative = MIMEMultipart('alternative')
    msg_related = MIMEMultipart('related')
    msg_related.attach('-- HTML goes here --')
    msg.attach(msg_alternative)
    add_subject(msg, subject)
    add_recipients_headers(user, useralias, msg, addresses)
    htmlstr = ''
    altstr = []
    if has_included_images:
        msg.preamble = 'This message is best displayed using a MIME capable email reader.'
    if contents is not None:
        for content_object, content_string in zip(content_objects, contents):
            if content_object['main_type'] == 'image':
                email.encoders.encode_base64(content_object['mime_object'])
                if isinstance(content_string, dict):
                    if len(content_string) == 1:
                        for key in content_string:
                            hashed_ref = str(abs(hash(key)))
                            alias = content_string[key]

                        content_string = key
                    else:
                        alias = os.path.basename(str(content_string))
                        hashed_ref = str(abs(hash(alias)))
                elif type(content_string) == inline:
                    htmlstr += '<img src="cid:{0}" title="{1}"/>'.format(hashed_ref, alias)
                    content_object['mime_object'].add_header('Content-ID', '<{0}>'.format(hashed_ref))
                    altstr.append('-- img {0} should be here -- '.format(alias))
                    msg_related.attach(content_object['mime_object'])
                else:
                    msg.attach(content_object['mime_object'])
            elif content_object['encoding'] == 'base64':
                email.encoders.encode_base64(content_object['mime_object'])
                msg.attach(content_object['mime_object'])
            elif content_object['sub_type'] not in ('html', 'plain'):
                msg.attach(content_object['mime_object'])
            else:
                if newline_to_break:
                    content_string = content_string.replace('\n', '<br>')
                try:
                    htmlstr += '<div>{0}</div>'.format(content_string)
                except UnicodeEncodeError:
                    htmlstr += '<div>{0}</div>'.format(content_string)

                altstr.append(content_string)

    msg_related.get_payload()[0] = MIMEText(htmlstr, 'html', _charset=encoding)
    msg_alternative.attach(MIMEText(('\n'.join(altstr)), _charset=encoding))
    msg_alternative.attach(msg_related)
    return msg


def prepare_contents(contents, encoding):
    mime_objects = []
    has_included_images = False
    if contents is not None:
        for content in contents:
            content_object = get_mime_object(content, encoding)
            if content_object['main_type'] == 'image':
                has_included_images = True
            mime_objects.append(content_object)

    return (
     has_included_images, mime_objects)


def get_mime_object(content_string, encoding):
    content_object = {'mime_object':None, 
     'encoding':None,  'main_type':None,  'sub_type':None}
    if isinstance(content_string, dict):
        for x in content_string:
            content_string, content_name = x, content_string[x]

    else:
        try:
            content_name = os.path.basename(str(content_string))
        except UnicodeEncodeError:
            content_name = os.path.basename(content_string)

        new_file_name = '=?utf-8?b?' + base64.b64encode(content_name.encode()).decode() + '?='
    is_raw = type(content_string) == raw
    try:
        is_file = os.path.isfile(content_string)
    except ValueError:
        is_file = False

    if not is_raw:
        if is_file:
            with open(content_string, 'rb') as (f):
                content_object['encoding'] = 'base64'
                content = f.read()
    else:
        content_object['main_type'] = 'text'
        if is_raw:
            content_object['mime_object'] = MIMEText(content_string, _charset=encoding)
        else:
            content_object['mime_object'] = MIMEText(content_string, 'html', _charset=encoding)
            content_object['sub_type'] = 'html'
        if content_object['sub_type'] is None:
            content_object['sub_type'] = 'plain'
        return content_object
    if content_object['main_type'] is None:
        content_type, _ = mimetypes.guess_type(content_string)
        if content_type is not None:
            content_object['main_type'], content_object['sub_type'] = content_type.split('/')
    if content_object['main_type'] is None or content_object['encoding'] is not None:
        if content_object['encoding'] != 'base64':
            content_object['main_type'] = 'application'
            content_object['sub_type'] = 'octet-stream'
    mime_object = MIMEBase((content_object['main_type']),
      (content_object['sub_type']), name=(encoding, '', content_name))
    mime_object.set_payload(content)
    if new_file_name:
        mime_object['Content-Disposition'] = 'attachment; filename="%s"' % new_file_name
    content_object['mime_object'] = mime_object
    return content_object