# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/webapi/resources/base_screenshot_comment.py
# Compiled at: 2020-02-11 04:03:57
from __future__ import unicode_literals
from django.db.models import Q
from django.template.defaultfilters import timesince
from django.utils import six
from djblets.util.decorators import augment_method_from
from reviewboard.reviews.models import ScreenshotComment
from reviewboard.webapi.base import WebAPIResource
from reviewboard.webapi.decorators import webapi_check_local_site
from reviewboard.webapi.resources import resources
from reviewboard.webapi.resources.base_comment import BaseCommentResource

class BaseScreenshotCommentResource(BaseCommentResource):
    """A base resource for screenshot comments."""
    model = ScreenshotComment
    name = b'screenshot_comment'
    fields = dict({b'screenshot': {b'type': b'reviewboard.webapi.resources.screenshot.ScreenshotResource', 
                       b'description': b'The screenshot the comment was made on.'}, 
       b'x': {b'type': int, 
              b'description': b'The X location of the comment region on the screenshot.'}, 
       b'y': {b'type': int, 
              b'description': b'The Y location of the comment region on the screenshot.'}, 
       b'w': {b'type': int, 
              b'description': b'The width of the comment region on the screenshot.'}, 
       b'h': {b'type': int, 
              b'description': b'The height of the comment region on the screenshot.'}, 
       b'thumbnail_url': {b'type': six.text_type, 
                          b'description': b'The URL to an image showing what was commented on.', 
                          b'added_in': b'1.7.10'}}, **BaseCommentResource.fields)
    uri_object_key = b'comment_id'
    allowed_methods = ('GET', )

    def get_queryset(self, request, *args, **kwargs):
        review_request = resources.review_request.get_object(request, *args, **kwargs)
        return self.model.objects.filter(Q(screenshot__review_request=review_request) | Q(screenshot__inactive_review_request=review_request), review__isnull=False)

    def serialize_public_field(self, obj, **kwargs):
        return obj.review.get().public

    def serialize_timesince_field(self, obj, **kwargs):
        return timesince(obj.timestamp)

    def serialize_user_field(self, obj, **kwargs):
        return obj.review.get().user

    def serialize_thumbnail_url_field(self, obj, **kwargs):
        return obj.get_image_url()

    @webapi_check_local_site
    @augment_method_from(WebAPIResource)
    def get(self, *args, **kwargs):
        """Returns information on the comment.

        This contains the comment text, time the comment was made,
        and the location of the comment region on the screenshot, amongst
        other information. It can be used to reconstruct the exact
        position of the comment for use as an overlay on the screenshot.
        """
        pass