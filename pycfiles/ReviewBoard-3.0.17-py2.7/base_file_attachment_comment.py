# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/webapi/resources/base_file_attachment_comment.py
# Compiled at: 2020-02-11 04:03:57
from __future__ import unicode_literals
from django.db.models import Q
from django.template.defaultfilters import timesince
from django.utils import six
from djblets.util.decorators import augment_method_from
from reviewboard.reviews.models import FileAttachmentComment
from reviewboard.webapi.base import WebAPIResource
from reviewboard.webapi.decorators import webapi_check_local_site
from reviewboard.webapi.resources import resources
from reviewboard.webapi.resources.base_comment import BaseCommentResource

class BaseFileAttachmentCommentResource(BaseCommentResource):
    """A base resource for file comments."""
    added_in = b'1.6'
    model = FileAttachmentComment
    name = b'file_attachment_comment'
    fields = dict({b'diff_against_file_attachment': {b'type': b'reviewboard.webapi.resources.file_attachment.FileAttachmentResource', 
                                         b'description': b'The file changes were made against in a diff.', 
                                         b'added_in': b'2.0'}, 
       b'file_attachment': {b'type': b'reviewboard.webapi.resources.file_attachment.FileAttachmentResource', 
                            b'description': b'The file the comment was made on.'}, 
       b'link_text': {b'type': six.text_type, 
                      b'description': b'The text used to describe a link to the file. This may differ depending on the comment.', 
                      b'added_in': b'1.7.10'}, 
       b'review_url': {b'type': six.text_type, 
                       b'description': b'The URL to the review UI for the comment on this file attachment.', 
                       b'added_in': b'1.7.10'}, 
       b'thumbnail_html': {b'type': six.text_type, 
                           b'description': b'The HTML representing a thumbnail, if any, for this comment.', 
                           b'added_in': b'1.7.10'}}, **BaseCommentResource.fields)
    uri_object_key = b'comment_id'
    allowed_methods = ('GET', )

    def get_queryset(self, request, *args, **kwargs):
        review_request = resources.review_request.get_object(request, *args, **kwargs)
        return self.model.objects.filter((Q(file_attachment__review_request=review_request) | Q(file_attachment__inactive_review_request=review_request)) & Q(review__isnull=False))

    def serialize_link_text_field(self, obj, **kwargs):
        return obj.get_link_text()

    def serialize_public_field(self, obj, **kwargs):
        return obj.review.get().public

    def serialize_review_url_field(self, obj, **kwargs):
        return obj.get_review_url()

    def serialize_thumbnail_html_field(self, obj, **kwargs):
        return obj.thumbnail

    def serialize_timesince_field(self, obj, **kwargs):
        return timesince(obj.timestamp)

    def serialize_user_field(self, obj, **kwargs):
        return obj.review.get().user

    @webapi_check_local_site
    @augment_method_from(WebAPIResource)
    def get(self, *args, **kwargs):
        """Returns information on the comment.

        This contains the comment text, time the comment was made,
        and the file the comment was made on, amongst other information.
        """
        pass