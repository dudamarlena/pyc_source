# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/webapi/resources/review_reply.py
# Compiled at: 2020-02-11 04:03:57
from __future__ import unicode_literals
from django.core.exceptions import ObjectDoesNotExist
from django.utils import six
from djblets.util.decorators import augment_method_from
from djblets.webapi.decorators import webapi_login_required, webapi_response_errors, webapi_request_fields
from djblets.webapi.errors import DOES_NOT_EXIST, NOT_LOGGED_IN, PERMISSION_DENIED
from reviewboard.reviews.errors import PublishError
from reviewboard.reviews.models import Review
from reviewboard.webapi.base import ImportExtraDataError
from reviewboard.webapi.decorators import webapi_check_local_site
from reviewboard.webapi.errors import PUBLISH_ERROR
from reviewboard.webapi.mixins import MarkdownFieldsMixin
from reviewboard.webapi.resources import resources
from reviewboard.webapi.resources.base_review import BaseReviewResource
from reviewboard.webapi.resources.user import UserResource

class ReviewReplyResource(BaseReviewResource):
    """Provides information on a reply to a review.

    A reply is much like a review, but is always tied to exactly one
    parent review. Every comment associated with a reply is also tied to
    a parent comment.
    """
    name = b'reply'
    name_plural = b'replies'
    policy_id = b'review_reply'
    fields = {b'body_bottom': {b'type': six.text_type, 
                        b'description': b'The response to the review content below the comments.', 
                        b'supports_text_types': True}, 
       b'body_bottom_text_type': {b'type': MarkdownFieldsMixin.TEXT_TYPES, 
                                  b'description': b'The current or forced text type for the body_bottom field.', 
                                  b'added_in': b'2.0.12'}, 
       b'body_top': {b'type': six.text_type, 
                     b'description': b'The response to the review content above the comments.', 
                     b'supports_text_types': True}, 
       b'body_top_text_type': {b'type': MarkdownFieldsMixin.TEXT_TYPES, 
                               b'description': b'The current or forced text type for the body_top field.', 
                               b'added_in': b'2.0.12'}, 
       b'extra_data': {b'type': dict, 
                       b'description': b'Extra data as part of the reply. This can be set by the API or extensions.', 
                       b'added_in': b'2.0'}, 
       b'id': {b'type': int, 
               b'description': b'The numeric ID of the reply.'}, 
       b'public': {b'type': bool, 
                   b'description': b'Whether or not the reply is currently visible to other users.'}, 
       b'text_type': {b'type': MarkdownFieldsMixin.TEXT_TYPES, 
                      b'description': b'Formerly responsible for indicating the text type for text fields. Replaced by body_top_text_type and body_bottom_text_type in 2.0.12.', 
                      b'added_in': b'2.0', 
                      b'deprecated_in': b'2.0.12'}, 
       b'timestamp': {b'type': six.text_type, 
                      b'description': b'The date and time that the reply was posted (in YYYY-MM-DD HH:MM:SS format).'}, 
       b'user': {b'type': UserResource, 
                 b'description': b'The user who wrote the reply.'}}
    item_child_resources = [
     resources.review_reply_diff_comment,
     resources.review_reply_screenshot_comment,
     resources.review_reply_file_attachment_comment,
     resources.review_reply_general_comment]
    list_child_resources = [
     resources.review_reply_draft]
    uri_object_key = b'reply_id'
    model_parent_key = b'base_reply_to'
    mimetype_list_resource_name = b'review-replies'
    mimetype_item_resource_name = b'review-reply'
    CREATE_UPDATE_OPTIONAL_FIELDS = {b'body_top': {b'type': six.text_type, 
                     b'description': b'The response to the review content above the comments.', 
                     b'supports_text_types': True}, 
       b'body_top_text_type': {b'type': MarkdownFieldsMixin.SAVEABLE_TEXT_TYPES, 
                               b'description': b'The text type used for the body_top field.', 
                               b'added_in': b'2.0.12'}, 
       b'body_bottom': {b'type': six.text_type, 
                        b'description': b'The response to the review content below the comments.', 
                        b'supports_text_types': True}, 
       b'body_bottom_text_type': {b'type': MarkdownFieldsMixin.SAVEABLE_TEXT_TYPES, 
                                  b'description': b'The text type used for the body_bottom field.', 
                                  b'added_in': b'2.0.12'}, 
       b'force_text_type': {b'type': MarkdownFieldsMixin.TEXT_TYPES, 
                            b'description': b'The text type, if any, to force for returned text fields. The contents will be converted to the requested type in the payload, but will not be saved as that type.', 
                            b'added_in': b'2.0.9'}, 
       b'public': {b'type': bool, 
                   b'description': b'Whether or not to make the reply public. If a reply is public, it cannot be made private again.'}, 
       b'text_type': {b'type': MarkdownFieldsMixin.SAVEABLE_TEXT_TYPES, 
                      b'description': b'The mode for the body_top and body_bottom text fields.\n\nThis is deprecated. Please use body_top_text_type and body_bottom_text_type instead.', 
                      b'added_in': b'2.0', 
                      b'deprecated_in': b'2.0.12'}, 
       b'trivial': {b'type': bool, 
                    b'description': b'If true, the review does not send an email.', 
                    b'added_in': b'2.5'}}

    def get_base_reply_to_field(self, review_id, *args, **kwargs):
        return {b'base_reply_to': Review.objects.get(pk=review_id)}

    def serialize_body_top_text_type_field(self, obj, **kwargs):
        return

    def serialize_body_bottom_text_type_field(self, obj, **kwargs):
        return

    @webapi_check_local_site
    @webapi_login_required
    @webapi_response_errors(DOES_NOT_EXIST, NOT_LOGGED_IN, PERMISSION_DENIED)
    @webapi_request_fields(optional=CREATE_UPDATE_OPTIONAL_FIELDS, allow_unknown=True)
    def create(self, request, *args, **kwargs):
        """Creates a reply to a review.

        The new reply will start off as private. Only the author of the
        reply (the user who is logged in and issuing this API call) will
        be able to see and interact with the reply.

        Initial data for the reply can be provided by passing data for
        any number of the fields. If nothing is provided, the reply will
        start off as blank.

        If the user submitting this reply already has a pending draft reply
        on this review, then this will update the existing draft and
        return :http:`303`. Otherwise, this will create a new draft and
        return :http:`201`. Either way, this request will return without
        a payload and with a ``Location`` header pointing to the location of
        the new draft reply.

        Extra data can be stored later lookup. See
        :ref:`webapi2.0-extra-data` for more information.
        """
        try:
            review_request = resources.review_request.get_object(request, *args, **kwargs)
            review = resources.review.get_object(request, *args, **kwargs)
        except ObjectDoesNotExist:
            return DOES_NOT_EXIST

        reply, is_new = Review.objects.get_or_create(review_request=review_request, user=request.user, public=False, base_reply_to=review)
        if is_new:
            status_code = 201
        else:
            status_code = 303
        result = self._update_reply(request, reply, *args, **kwargs)
        if not isinstance(result, tuple) or result[0] != 200:
            return result
        return (status_code, result[1],
         {b'Location': self.get_href(reply, request, *args, **kwargs)})

    @webapi_check_local_site
    @webapi_login_required
    @webapi_response_errors(DOES_NOT_EXIST, NOT_LOGGED_IN, PERMISSION_DENIED)
    @webapi_request_fields(optional=CREATE_UPDATE_OPTIONAL_FIELDS, allow_unknown=True)
    def update(self, request, *args, **kwargs):
        """Updates a reply.

        This updates the fields of a draft reply. Published replies cannot
        be updated.

        Only the owner of a reply can make changes. One or more fields can
        be updated at once.

        The only special field is ``public``, which, if set to true, will
        publish the reply. The reply will then be made publicly visible. Once
        public, the reply cannot be modified or made private again.

        Extra data can be stored later lookup. See
        :ref:`webapi2.0-extra-data` for more information.
        """
        try:
            resources.review_request.get_object(request, *args, **kwargs)
            resources.review.get_object(request, *args, **kwargs)
            reply = self.get_object(request, *args, **kwargs)
        except ObjectDoesNotExist:
            return DOES_NOT_EXIST

        return self._update_reply(request, reply, *args, **kwargs)

    @webapi_check_local_site
    @augment_method_from(BaseReviewResource)
    def get_list(self, *args, **kwargs):
        """Returns the list of all public replies on a review."""
        pass

    @webapi_check_local_site
    @augment_method_from(BaseReviewResource)
    def get(self, *args, **kwargs):
        """Returns information on a particular reply.

        If the reply is not public, then the client's logged in user
        must either be the owner of the reply. Otherwise, an error will
        be returned.
        """
        pass

    def _update_reply(self, request, reply, public=None, trivial=False, extra_fields={}, *args, **kwargs):
        """Common function to update fields on a draft reply."""
        if not self.has_modify_permissions(request, reply):
            return self.get_no_access_error(request)
        else:
            for field in ('body_top', 'body_bottom'):
                value = kwargs.get(field, None)
                if value is not None:
                    if value == b'':
                        reply_to = None
                    else:
                        reply_to = reply.base_reply_to
                    setattr(reply, b'%s_reply_to' % field, reply_to)

            self.set_text_fields(reply, b'body_top', **kwargs)
            self.set_text_fields(reply, b'body_bottom', **kwargs)
            try:
                self.import_extra_data(reply, reply.extra_data, extra_fields)
            except ImportExtraDataError as e:
                return e.error_payload

            if public:
                try:
                    reply.publish(user=request.user, trivial=trivial)
                except PublishError as e:
                    return PUBLISH_ERROR.with_message(six.text_type(e))

            else:
                reply.save()
            return (200,
             {self.item_result_key: reply},
             {b'Last-Modified': self.get_last_modified(request, reply)})


review_reply_resource = ReviewReplyResource()