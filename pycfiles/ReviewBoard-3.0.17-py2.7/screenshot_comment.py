# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/webapi/resources/screenshot_comment.py
# Compiled at: 2020-02-11 04:03:57
from __future__ import unicode_literals
from djblets.util.decorators import augment_method_from
from reviewboard.webapi.decorators import webapi_check_local_site
from reviewboard.webapi.resources.base_screenshot_comment import BaseScreenshotCommentResource

class ScreenshotCommentResource(BaseScreenshotCommentResource):
    """Provides information on screenshots comments made on a review request.

    The list of comments cannot be modified from this resource. It's meant
    purely as a way to see existing comments that were made on a screenshot.
    These comments will span all public reviews.
    """
    model_parent_key = b'screenshot'
    uri_object_key = None

    def get_queryset(self, request, screenshot_id, *args, **kwargs):
        q = super(ScreenshotCommentResource, self).get_queryset(request, *args, **kwargs)
        q = q.filter(screenshot=screenshot_id)
        return q

    @webapi_check_local_site
    @augment_method_from(BaseScreenshotCommentResource)
    def get_list(self, *args, **kwargs):
        """Returns the list of screenshot comments on a screenshot.

        This list of comments will cover all comments made on this
        screenshot from all reviews.
        """
        pass


screenshot_comment_resource = ScreenshotCommentResource()