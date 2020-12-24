# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/webapi/resources/base_file_attachment.py
# Compiled at: 2020-02-11 04:03:57
from __future__ import unicode_literals
from django.utils import six
from reviewboard.attachments.models import FileAttachment
from reviewboard.webapi.base import WebAPIResource

class BaseFileAttachmentResource(WebAPIResource):
    """A base resource representing file attachments."""
    added_in = b'1.6'
    model = FileAttachment
    name = b'file_attachment'
    fields = {b'id': {b'type': int, 
               b'description': b'The numeric ID of the file.'}, 
       b'caption': {b'type': six.text_type, 
                    b'description': b"The file's descriptive caption."}, 
       b'filename': {b'type': six.text_type, 
                     b'description': b'The name of the file.'}, 
       b'absolute_url': {b'type': six.text_type, 
                         b'description': b'The absolute URL of the file, for downloading purposes.', 
                         b'added_in': b'2.0'}, 
       b'icon_url': {b'type': six.text_type, 
                     b'description': b'The URL to a 24x24 icon representing this file. The use of these icons is deprecated and this property will be removed in a future version.', 
                     b'deprecated_in': b'2.5'}, 
       b'mimetype': {b'type': six.text_type, 
                     b'description': b'The mimetype for the file.', 
                     b'added_in': b'2.0'}, 
       b'thumbnail': {b'type': six.text_type, 
                      b'description': b'A thumbnail representing this file.', 
                      b'added_in': b'1.7'}}
    uri_object_key = b'file_attachment_id'

    def serialize_absolute_url_field(self, obj, request, **kwargs):
        return request.build_absolute_uri(obj.get_absolute_url())

    def serialize_caption_field(self, obj, **kwargs):
        return obj.caption or obj.draft_caption