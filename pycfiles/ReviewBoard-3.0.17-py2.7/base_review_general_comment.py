# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/webapi/resources/base_review_general_comment.py
# Compiled at: 2020-02-11 04:03:57
from __future__ import unicode_literals
from django.db.models import Q
from django.template.defaultfilters import timesince
from djblets.util.decorators import augment_method_from
from reviewboard.reviews.features import general_comments_feature
from reviewboard.reviews.models import GeneralComment
from reviewboard.webapi.base import WebAPIResource
from reviewboard.webapi.decorators import webapi_check_local_site
from reviewboard.webapi.resources import resources
from reviewboard.webapi.resources.base_comment import BaseCommentResource

class BaseReviewGeneralCommentResource(BaseCommentResource):
    """Provides information on general comments made on a review request.

    The list of comments cannot be modified from this resource. It's meant
    purely as a way to see existing comments that were made on a review.
    These comments will span all public reviews.
    """
    model = GeneralComment
    name = b'general_comment'
    model_parent_key = b'review_request'
    uri_object_key = b'comment_id'
    allowed_methods = ('GET', )
    required_features = [
     general_comments_feature]

    def get_queryset(self, request, *args, **kwargs):
        review_request = resources.review_request.get_object(request, *args, **kwargs)
        return self.model.objects.filter(Q(review__review_request=review_request), review__isnull=False)

    def serialize_public_field(self, obj, **kwargs):
        return obj.review.get().public

    def serialize_timesince_field(self, obj, **kwargs):
        return timesince(obj.timestamp)

    def serialize_user_field(self, obj, **kwargs):
        return obj.review.get().user

    @webapi_check_local_site
    @augment_method_from(WebAPIResource)
    def get(self, *args, **kwargs):
        """Returns information on the comment.

        This contains the comment text and the date/time the comment was
        made.
        """
        pass

    @webapi_check_local_site
    @augment_method_from(WebAPIResource)
    def get_list(self, *args, **kwargs):
        """Returns the list of general comments on a review request.

        This list of comments will cover all comments from all reviews
        on this review request.
        """
        pass