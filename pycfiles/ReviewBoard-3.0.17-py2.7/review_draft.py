# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/webapi/resources/review_draft.py
# Compiled at: 2020-02-11 04:03:57
from __future__ import unicode_literals
from django.core.exceptions import ObjectDoesNotExist
from djblets.webapi.decorators import webapi_login_required
from djblets.webapi.errors import DOES_NOT_EXIST
from reviewboard.webapi.base import WebAPIResource
from reviewboard.webapi.decorators import webapi_check_local_site
from reviewboard.webapi.resources import resources

class ReviewDraftResource(WebAPIResource):
    """A redirecting resource that points to the current draft review."""
    name = b'review_draft'
    singleton = True
    uri_name = b'draft'

    @webapi_check_local_site
    @webapi_login_required
    def get(self, request, *args, **kwargs):
        """Returns an HTTP redirect to the current draft review."""
        try:
            review_request = resources.review_request.get_object(request, *args, **kwargs)
            review = review_request.get_pending_review(request.user)
        except ObjectDoesNotExist:
            return DOES_NOT_EXIST

        if not review:
            return DOES_NOT_EXIST
        return (302, {},
         {b'Location': self._build_redirect_with_args(request, resources.review.get_href(review, request, *args, **kwargs))})


review_draft_resource = ReviewDraftResource()