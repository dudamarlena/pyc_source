# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/webapi/resources/base_review.py
# Compiled at: 2020-02-11 04:03:57
from __future__ import unicode_literals
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.utils import six
from djblets.util.decorators import augment_method_from
from djblets.webapi.decorators import webapi_login_required, webapi_response_errors, webapi_request_fields
from djblets.webapi.errors import DOES_NOT_EXIST, NOT_LOGGED_IN, PERMISSION_DENIED
from reviewboard.reviews.errors import PublishError
from reviewboard.reviews.models import Review
from reviewboard.webapi.base import ImportExtraDataError, WebAPIResource
from reviewboard.webapi.decorators import webapi_check_local_site
from reviewboard.webapi.errors import PUBLISH_ERROR
from reviewboard.webapi.mixins import MarkdownFieldsMixin
from reviewboard.webapi.resources import resources
from reviewboard.webapi.resources.user import UserResource

class BaseReviewResource(MarkdownFieldsMixin, WebAPIResource):
    """Base class for review resources.

    Provides common fields and functionality for all review resources.
    """
    model = Review
    fields = {b'absolute_url': {b'type': six.text_type, 
                         b'description': b"The absolute URL to the review request's page on the site.", 
                         b'added_in': b'3.0'}, 
       b'body_bottom': {b'type': six.text_type, 
                        b'description': b'The review content below the comments.', 
                        b'supports_text_types': True}, 
       b'body_bottom_text_type': {b'type': MarkdownFieldsMixin.TEXT_TYPES, 
                                  b'description': b'The current or forced text type for the ``body_bottom`` field.', 
                                  b'added_in': b'2.0.12'}, 
       b'body_top': {b'type': six.text_type, 
                     b'description': b'The review content above the comments.', 
                     b'supports_text_types': True}, 
       b'body_top_text_type': {b'type': MarkdownFieldsMixin.TEXT_TYPES, 
                               b'description': b'The current or forced text type for the ``body_top`` field.', 
                               b'added_in': b'2.0.12'}, 
       b'extra_data': {b'type': dict, 
                       b'description': b'Extra data as part of the review. This can be set by the API or extensions.', 
                       b'added_in': b'2.0'}, 
       b'id': {b'type': int, 
               b'description': b'The numeric ID of the review.'}, 
       b'public': {b'type': bool, 
                   b'description': b'Whether or not the review is currently visible to other users.'}, 
       b'ship_it': {b'type': bool, 
                    b'description': b'Whether or not the review has been marked "Ship It!"'}, 
       b'text_type': {b'type': MarkdownFieldsMixin.TEXT_TYPES, 
                      b'description': b'Formerly responsible for indicating the text type for text fields. Replaced by ``body_top_text_type`` and ``body_bottom_text_type`` in 2.0.12.', 
                      b'added_in': b'2.0', 
                      b'deprecated_in': b'2.0.12'}, 
       b'timestamp': {b'type': six.text_type, 
                      b'description': b'The date and time that the review was posted (in ``YYYY-MM-DD HH:MM:SS`` format).'}, 
       b'user': {b'type': UserResource, 
                 b'description': b'The user who wrote the review.'}}
    allowed_methods = ('GET', 'POST', 'PUT', 'DELETE')
    CREATE_UPDATE_OPTIONAL_FIELDS = {b'ship_it': {b'type': bool, 
                    b'description': b'Whether or not to mark the review "Ship It!"'}, 
       b'body_top': {b'type': six.text_type, 
                     b'description': b'The review content above the comments.', 
                     b'supports_text_types': True}, 
       b'body_top_text_type': {b'type': MarkdownFieldsMixin.SAVEABLE_TEXT_TYPES, 
                               b'description': b'The text type used for the ``body_top`` field.', 
                               b'added_in': b'2.0.12'}, 
       b'body_bottom': {b'type': six.text_type, 
                        b'description': b'The review content below the comments.', 
                        b'supports_text_types': True}, 
       b'body_bottom_text_type': {b'type': MarkdownFieldsMixin.SAVEABLE_TEXT_TYPES, 
                                  b'description': b'The text type used for the ``body_bottom`` field.', 
                                  b'added_in': b'2.0.12'}, 
       b'force_text_type': {b'type': MarkdownFieldsMixin.TEXT_TYPES, 
                            b'description': b'The text type, if any, to force for returned text fields. The contents will be converted to the requested type in the payload, but will not be saved as that type.', 
                            b'added_in': b'2.0.9'}, 
       b'public': {b'type': bool, 
                   b'description': b'Whether or not to make the review public. If a review is public, it cannot be made private again.'}, 
       b'text_type': {b'type': MarkdownFieldsMixin.SAVEABLE_TEXT_TYPES, 
                      b'description': b'The mode for the ``body_top`` and ``body_bottom`` text fields.\n\nThis is deprecated. Please use ``body_top_text_type`` and ``body_bottom_text_type`` instead.', 
                      b'added_in': b'2.0', 
                      b'deprecated_in': b'2.0.12'}, 
       b'publish_to_owner_only': {b'type': bool, 
                                  b'description': b'If true, the review will only send an e-mail to the owner of the review request.', 
                                  b'added_in': b'3.0'}}

    def get_queryset(self, request, is_list=False, *args, **kwargs):
        review_request = resources.review_request.get_object(request, *args, **kwargs)
        q = Q(review_request=review_request) & Q(**self.get_base_reply_to_field(*args, **kwargs))
        if is_list:
            q = q & Q(public=True)
        return self.model.objects.filter(q)

    def get_base_reply_to_field(self):
        raise NotImplementedError

    def has_access_permissions(self, request, review, *args, **kwargs):
        return review.is_accessible_by(request.user)

    def has_modify_permissions(self, request, review, *args, **kwargs):
        return review.is_mutable_by(request.user)

    def has_delete_permissions(self, request, review, *args, **kwargs):
        return review.is_mutable_by(request.user)

    def serialize_absolute_url_field(self, obj, request, **kwargs):
        return request.build_absolute_uri(obj.get_absolute_url())

    def serialize_body_top_text_type_field(self, obj, **kwargs):
        return

    def serialize_body_bottom_text_type_field(self, obj, **kwargs):
        return

    @webapi_check_local_site
    @webapi_login_required
    @webapi_response_errors(DOES_NOT_EXIST, NOT_LOGGED_IN, PERMISSION_DENIED)
    @webapi_request_fields(optional=CREATE_UPDATE_OPTIONAL_FIELDS, allow_unknown=True)
    def create(self, request, *args, **kwargs):
        """Creates a new review.

        The new review will start off as private. Only the author of the
        review (the user who is logged in and issuing this API call) will
        be able to see and interact with the review.

        Initial data for the review can be provided by passing data for
        any number of the fields. If nothing is provided, the review will
        start off as blank.

        If the user submitting this review already has a pending draft review
        on this review request, then this will update the existing draft and
        return :http:`303`. Otherwise, this will create a new draft and
        return :http:`201`. Either way, this request will return without
        a payload and with a ``Location`` header pointing to the location of
        the new draft review.
        """
        try:
            review_request = resources.review_request.get_object(request, *args, **kwargs)
        except ObjectDoesNotExist:
            return DOES_NOT_EXIST

        review, is_new = Review.objects.get_or_create(review_request=review_request, user=request.user, public=False, **self.get_base_reply_to_field(*args, **kwargs))
        if is_new:
            status_code = 201
        else:
            status_code = 303
        result = self.update_review(request, review, *args, **kwargs)
        if not isinstance(result, tuple) or result[0] != 200:
            return result
        return (status_code, result[1],
         {b'Location': self.get_href(review, request, *args, **kwargs)})

    @webapi_check_local_site
    @webapi_login_required
    @webapi_response_errors(DOES_NOT_EXIST, NOT_LOGGED_IN, PERMISSION_DENIED)
    @webapi_request_fields(optional=CREATE_UPDATE_OPTIONAL_FIELDS, allow_unknown=True)
    def update(self, request, *args, **kwargs):
        """Updates the fields of an unpublished review.

        Only the owner of a review can make changes. One or more fields can
        be updated at once.

        The only special field is ``public``, which, if set to true, will
        publish the review. The review will then be made publicly visible. Once
        public, the review cannot be modified or made private again
        with the exception of removing a ship it from review.
        """
        try:
            resources.review_request.get_object(request, *args, **kwargs)
            review = resources.review.get_object(request, *args, **kwargs)
        except ObjectDoesNotExist:
            return DOES_NOT_EXIST

        return self.update_review(request, review, *args, **kwargs)

    @webapi_check_local_site
    @augment_method_from(WebAPIResource)
    def delete(self, *args, **kwargs):
        """Deletes the draft review.

        This only works for draft reviews, not public reviews. It will
        delete the review and all comments on it. This cannot be undone.

        Only the user who owns the draft can delete it.

        Upon deletion, this will return :http:`204`.
        """
        pass

    @webapi_check_local_site
    @augment_method_from(WebAPIResource)
    def get(self, *args, **kwargs):
        """Returns information on a particular review.

        If the review is not public, then the client's logged in user
        must either be the owner of the review. Otherwise, an error will
        be returned.
        """
        pass

    def update_review(self, request, review, public=None, publish_to_owner_only=False, extra_fields={}, ship_it=None, **kwargs):
        """Update an existing review based on the requested data.

        This will modify a review, setting new fields requested by the
        caller.

        Args:
            request (django.http.HttpRequest):
                The HTTP request from the client.

            review (reviewboard.reviews.models.review.Review):
                The review being modified.

            public (bool, optional):
                Whether the review is being made public for the first
                time.

            publish_to_owner_only (bool, optional):
                Whether an e-mail for the published review should only be
                sent to the owner of the review request. This is ignored if
                ``public`` is not ``True``.

            extra_fields (dict, optional):
                Extra fields from the request not otherwise handled by the
                API resource. Any ``extra_data`` modifications from this will
                be applied to the comment.

            ship_it (bool, optional):
                The new Ship It state for the review.

            **kwargs (dict):
                Keyword arguments representing additional fields handled by
                the API resource.

        Returns:
            tuple or djblets.webapi.errors.WebAPIError:
            Either a successful payload containing the review, or an error
            payload.
        """
        if not self.has_modify_permissions(request, review):
            return self.get_no_access_error(request)
        else:
            if ship_it is not None:
                review.ship_it = ship_it
            self.set_text_fields(review, b'body_top', **kwargs)
            self.set_text_fields(review, b'body_bottom', **kwargs)
            try:
                self.import_extra_data(review, review.extra_data, extra_fields)
            except ImportExtraDataError as e:
                return e.error_payload

            review.save()
            if public:
                try:
                    review.publish(user=request.user, to_owner_only=publish_to_owner_only, request=request)
                except PublishError as e:
                    return PUBLISH_ERROR.with_message(six.text_type(e))

            return (
             200,
             {self.item_result_key: review})