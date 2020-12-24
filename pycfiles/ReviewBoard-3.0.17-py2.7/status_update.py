# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/webapi/resources/status_update.py
# Compiled at: 2020-02-11 04:03:57
from __future__ import unicode_literals
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.utils import six
from djblets.util.decorators import augment_method_from
from djblets.webapi.decorators import webapi_login_required, webapi_request_fields, webapi_response_errors
from djblets.webapi.errors import DOES_NOT_EXIST, INVALID_FORM_DATA, NOT_LOGGED_IN, PERMISSION_DENIED
from reviewboard.changedescs.models import ChangeDescription
from reviewboard.reviews.features import status_updates_feature
from reviewboard.reviews.models import Review, StatusUpdate
from reviewboard.webapi.base import ImportExtraDataError, WebAPIResource
from reviewboard.webapi.decorators import webapi_check_local_site
from reviewboard.webapi.resources import resources

class StatusUpdateResource(WebAPIResource):
    """Provides status updates on review requests.

    A status update is a way for a third-party service or extension to mark
    some kind of status on a review request. Examples of this could include
    static analysis tools or continuous integration services.

    Status updates may optionally be associated with a
    :ref:`change description <webapi2.0-change-resource>`, in which case they
    will be shown in that change description box on the review request page.
    Otherwise, the status update will be shown in a box immediately below the
    review request details.
    """
    required_features = [
     status_updates_feature]
    model = StatusUpdate
    name = b'status_update'
    fields = {b'change': {b'type': b'reviewboard.webapi.resources.change.ChangeResource', 
                   b'description': b'The change to a review request which this status update applies to (for example, the change adding a diff that was built by CI). If this is blank, the status update is for the review request as initially published.'}, 
       b'description': {b'type': six.text_type, 
                        b'description': b'A user-visible description of the status update.'}, 
       b'extra_data': {b'type': dict, 
                       b'description': b'Extra data as part of the status update. This can be set by the API or extensions.'}, 
       b'id': {b'type': int, 
               b'description': b'The ID of the status update.'}, 
       b'review': {b'type': b'reviewboard.webapi.resources.review.ReviewResource', 
                   b'description': b'A review which corresponds to this status update.'}, 
       b'service_id': {b'type': six.text_type, 
                       b'description': b'A unique identifier for the service providing the status update.'}, 
       b'state': {b'type': ('pending', 'done_success', 'done_failure', 'error', 'timed-out'), 
                  b'description': b'The current state of the status update.'}, 
       b'summary': {b'type': six.text_type, 
                    b'description': b'A user-visible short summary of the status update.'}, 
       b'timeout': {b'type': int, 
                    b'description': b'An optional timeout for pending status updates, measured in seconds.'}, 
       b'url': {b'type': six.text_type, 
                b'description': b'An optional URL to link to for more details about the status update.'}, 
       b'url_text': {b'type': six.text_type, 
                     b'description': b'The text to use for the link.'}}
    uri_object_key = b'status_update_id'
    model_parent_key = b'review_request'
    allowed_methods = ('GET', 'POST', 'PUT', 'DELETE')
    added_in = b'3.0'

    def has_access_permissions(self, request, status_update, *args, **kwargs):
        """Return whether the user has permissions to access the status update.

        Args:
            request (django.http.HttpRequest):
                The current HTTP request.

            status_update (reviewboard.reviews.models.StatusUpdate):
                The status update to check permissions for.

            *args (tuple):
                Additional arguments (unused).

            **kwargs (dict):
                Additional keyword arguments (unused).

        Returns:
            boolean:
            Whether the user making the request has read access for the status
            update.
        """
        return status_update.review_request.is_accessible_by(request.user)

    def has_modify_permissions(self, request, status_update, *args, **kwargs):
        """Return whether the user has permissions to modify the status update.

        Args:
            request (django.http.HttpRequest):
                The current HTTP request.

            status_update (reviewboard.reviews.models.StatusUpdate):
                The status update to check permissions for.

            *args (tuple):
                Additional arguments (unused).

            **kwargs (dict):
                Additional keyword arguments (unused).

        Returns:
            boolean:
            Whether the user making the request has modify access for the
            status update.
        """
        return status_update.is_mutable_by(request.user)

    def has_delete_permissions(self, request, status_update, *args, **kwargs):
        """Return whether the user has permissions to delete the status update.

        Args:
            request (django.http.HttpRequest):
                The current HTTP request.

            status_update (reviewboard.reviews.models.StatusUpdate):
                The status update to check permissions for.

            *args (tuple):
                Additional arguments (unused).

            **kwargs (dict):
                Additional keyword arguments (unused).

        Returns:
            boolean:
            Whether the user making the request has delete access for the
            status update.
        """
        return status_update.is_mutable_by(request.user)

    def serialize_change_field(self, obj, **kwargs):
        """Return a serialized version of the ``change`` field.

        Args:
            obj (reviewboard.reviews.models.StatusUpdate):
                The status update being serialized.

            **kwargs (dict):
                Additional keyword arguments (unused).

        Returns:
            reviewboard.changedescs.models.ChangeDescription:
            The change description object. This will get serialized as a link
            to the relevant resource.
        """
        return obj.change_description

    def serialize_state_field(self, obj, **kwargs):
        """Return a serialized version of the ``state`` field.

        Args:
            obj (reviewboard.reviews.models.StatusUpdate):
                The status update being serialized.

            **kwargs (dict):
                Additional keyword arguments (unused).

        Returns:
            unicode:
            The serialized state.
        """
        return StatusUpdate.state_to_string(obj.effective_state)

    @webapi_check_local_site
    @webapi_request_fields(optional={b'change': {b'type': int, 
                   b'description': b'The change description to get status updates for.'}, 
       b'service-id': {b'type': six.text_type, 
                       b'description': b'The service ID to query for.'}, 
       b'state': {b'type': ('pending', 'done-success', 'done-failure', 'error'), 
                  b'description': b'The state to query for.'}})
    @augment_method_from(WebAPIResource)
    def get_list(self, *args, **kwargs):
        """Returns a list of status updates on a review request.

        By default, this returns all status updates for the review request.
        """
        pass

    @augment_method_from(WebAPIResource)
    def get(self, *args, **kwargs):
        """Returns information on a single status update."""
        pass

    def get_queryset(self, request, is_list=False, *args, **kwargs):
        """Return a queryset for StatusUpdate models.

        Args:
            request (django.http.HttpRequest):
                The HTTP request.

            is_list (boolean):
                Whether this query is for the list resource (which supports
                additional query options).

            *args (tuple):
                Additional arguments to be passed to parent resources.

            **kwargs (dict):
                Additional keyword arguments to be passed to parent resources.

        Returns:
            django.db.models.query.QuerySet:
            A QuerySet containing the matching status updates.
        """
        review_request = resources.review_request.get_object(request, *args, **kwargs)
        q = Q()
        if is_list:
            if b'change' in request.GET:
                q = q & Q(change_description=int(request.GET.get(b'change')))
            if b'service-id' in request.GET:
                q = q & Q(service_id=request.GET.get(b'service-id'))
            if b'state' in request.GET:
                q = q & Q(state=StatusUpdate.string_to_state(request.GET.get(b'state')))
        return review_request.status_updates.filter(q)

    @webapi_check_local_site
    @webapi_login_required
    @webapi_response_errors(DOES_NOT_EXIST, NOT_LOGGED_IN, PERMISSION_DENIED)
    @webapi_request_fields(required={b'service_id': {b'type': six.text_type, 
                       b'description': b'A unique identifier for the service providing the status update.'}, 
       b'summary': {b'type': six.text_type, 
                    b'description': b'A user-visible short summary of the status update.'}}, optional={b'change_id': {b'type': int, 
                      b'description': b'The change to a review request which this status update applies to (for example, the change adding a diff that was built by CI). If this is blank, the status update is for the review request as initially published.'}, 
       b'description': {b'type': six.text_type, 
                        b'description': b'A user-visible description of the status update.'}, 
       b'review_id': {b'type': int, 
                      b'description': b'A review which corresponds to this status update.'}, 
       b'state': {b'type': ('pending', 'done-success', 'done-failure', 'error'), 
                  b'description': b'The current state of the status update.'}, 
       b'timeout': {b'type': int, 
                    b'description': b'An optional timeout for pending status updates, measured in seconds.'}, 
       b'url': {b'type': six.text_type, 
                b'description': b'A URL to link to for more details about the status update.'}, 
       b'url_text': {b'type': six.text_type, 
                     b'description': b'The text to use for the link.'}}, allow_unknown=True)
    def create(self, request, state=b'pending', extra_fields={}, *args, **kwargs):
        """Creates a new status update.

        At a minimum, the service ID and a summary must be provided.

        If desired, the new status update can be associated with a change
        description and/or a review. If a change description is included, this
        status update will be displayed in the review request page within that
        change description's box. If a review is attached, once that review is
        published, it will appear alongside the status update.

        Extra data can be stored later lookup. See
        :ref:`webapi2.0-extra-data` for more information.
        """
        try:
            review_request = resources.review_request.get_object(request, *args, **kwargs)
        except ObjectDoesNotExist:
            return DOES_NOT_EXIST

        status_update = self.model(review_request=review_request, user=request.user)
        return self._update_status(status_update, extra_fields, state=state, **kwargs)

    @webapi_check_local_site
    @webapi_login_required
    @webapi_response_errors(DOES_NOT_EXIST, NOT_LOGGED_IN, PERMISSION_DENIED)
    @webapi_request_fields(optional={b'change_id': {b'type': int, 
                      b'description': b'The change to a review request which this status update applies to (for example, the change adding a diff that was built by CI). If this is blank, the status update is for the review request as initially published.'}, 
       b'description': {b'type': six.text_type, 
                        b'description': b'A user-visible description of the status update.'}, 
       b'review_id': {b'type': int, 
                      b'description': b'A review which corresponds to this status update.'}, 
       b'service_id': {b'type': six.text_type, 
                       b'description': b'A unique identifier for the service providing the status update.'}, 
       b'state': {b'type': ('pending', 'done-success', 'done-failure', 'error'), 
                  b'description': b'The current state of the status update.'}, 
       b'summary': {b'type': six.text_type, 
                    b'description': b'A user-visible short summary of the status update.'}, 
       b'timeout': {b'type': int, 
                    b'description': b'An optional timeout for pending status updates, measured in seconds.'}, 
       b'url': {b'type': six.text_type, 
                b'description': b'A URL to link to for more details about the status update.'}, 
       b'url_text': {b'type': six.text_type, 
                     b'description': b'The text to use for the link.'}}, allow_unknown=True)
    def update(self, request, extra_fields={}, *args, **kwargs):
        """Updates the status update.

        Only the owner of a status update can make changes. One or more fields
        can be updated at once.

        Extra data can be stored later lookup. See
        :ref:`webapi2.0-extra-data` for more information.
        """
        try:
            status_update = self.get_object(request, *args, **kwargs)
        except ObjectDoesNotExist:
            return DOES_NOT_EXIST

        if not self.has_modify_permissions(request, status_update):
            return self.get_no_access_error(request)
        return self._update_status(status_update, extra_fields, **kwargs)

    def _update_status(self, status_update, extra_fields, **kwargs):
        """Update the fields of the StatusUpdate model.

        Args:
            status_update (reviewboard.reviews.models.StatusUpdate):
                The status update to modify.

            extra_fields (dict):
                Any additional fields to update into the status update's
                ``extra_data`` field.

            **kwargs (dict):
                A dictionary of field names and new values to update.
        """
        for field_name in ('description', 'service_id', 'summary', 'timeout', 'url',
                           'url_text'):
            if field_name in kwargs:
                setattr(status_update, field_name, kwargs[field_name])

        if b'state' in kwargs:
            status_update.state = StatusUpdate.string_to_state(kwargs[b'state'])
        if b'change_id' in kwargs:
            try:
                status_update.change_description = ChangeDescription.objects.get(pk=kwargs[b'change_id'])
            except ChangeDescription.DoesNotExist:
                return (
                 INVALID_FORM_DATA,
                 {b'fields': {b'change_id': [
                                             b'Invalid change description ID']}})

        if b'review_id' in kwargs:
            try:
                status_update.review = Review.objects.get(pk=kwargs[b'review_id'])
            except Review.DoesNotExist:
                return (
                 INVALID_FORM_DATA,
                 {b'fields': {b'review_id': [
                                             b'Invalid review ID']}})

        try:
            self.import_extra_data(status_update, status_update.extra_data, extra_fields)
        except ImportExtraDataError as e:
            return e.error_payload

        if status_update.pk is None:
            code = 201
        else:
            code = 200
        status_update.save()
        return (
         code,
         {self.item_result_key: status_update})

    @webapi_check_local_site
    @webapi_login_required
    @webapi_response_errors(DOES_NOT_EXIST, NOT_LOGGED_IN, PERMISSION_DENIED)
    def delete(self, request, *args, **kwargs):
        """Deletes the status update permanently.

        After a successful delete, this will return :http:`204`.
        """
        try:
            status_update = self.get_object(request, *args, **kwargs)
        except ObjectDoesNotExist:
            return DOES_NOT_EXIST

        if not self.has_delete_permissions(request, status_update, *args, **kwargs):
            return self.get_no_access_error(request)
        status_update.delete()
        return (
         204, {})


status_update_resource = StatusUpdateResource()