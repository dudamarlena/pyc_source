# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/webapi/resources/api_token.py
# Compiled at: 2020-02-11 04:03:57
from __future__ import unicode_literals
import json
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.utils import six
from django.utils.translation import ugettext as _
from djblets.util.decorators import augment_method_from
from djblets.webapi.decorators import webapi_login_required, webapi_request_fields, webapi_response_errors
from djblets.webapi.errors import DOES_NOT_EXIST, INVALID_FORM_DATA, NOT_LOGGED_IN, PERMISSION_DENIED, WebAPITokenGenerationError
from reviewboard.webapi.base import ImportExtraDataError, WebAPIResource
from reviewboard.webapi.decorators import webapi_check_local_site
from reviewboard.webapi.errors import TOKEN_GENERATION_FAILED
from reviewboard.webapi.models import WebAPIToken
from reviewboard.webapi.resources import resources

class APITokenResource(WebAPIResource):
    """Manages the tokens used to access the API.

    This resource allows callers to retrieve their list of tokens, register
    new tokens, delete old ones, and update information on existing tokens.
    """
    model = WebAPIToken
    name = b'api_token'
    verbose_name = b'API Token'
    api_token_access_allowed = False
    oauth2_token_access_allowed = False
    added_in = b'2.5'
    fields = {b'id': {b'type': six.text_type, 
               b'description': b'The numeric ID of the token entry.'}, 
       b'token': {b'type': six.text_type, 
                  b'description': b'The token value.'}, 
       b'time_added': {b'type': six.text_type, 
                       b'description': b'The date and time that the token was added (in ``YYYY-MM-DD HH:MM:SS`` format).'}, 
       b'last_updated': {b'type': six.text_type, 
                         b'description': b'The date and time that the token was last updated (in ``YYYY-MM-DD HH:MM:SS`` format).'}, 
       b'note': {b'type': six.text_type, 
                 b'description': b'The note explaining the purpose of this token.'}, 
       b'policy': {b'type': dict, 
                   b'description': b'The access policies defined for this token.'}, 
       b'extra_data': {b'type': dict, 
                       b'description': b'Extra data as part of the token. This can be set by the API or extensions.'}}
    uri_object_key = b'api_token_id'
    last_modified_field = b'last_updated'
    model_parent_key = b'user'
    allowed_methods = ('GET', 'POST', 'PUT', 'DELETE')

    def get_queryset(self, request, local_site_name=None, *args, **kwargs):
        user = resources.user.get_object(request, local_site_name=local_site_name, *args, **kwargs)
        local_site = self._get_local_site(local_site_name)
        return self.model.objects.filter(user=user, local_site=local_site)

    def has_list_access_permissions(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return True
        user = resources.user.get_object(request, *args, **kwargs)
        return user == request.user

    def has_access_permissions(self, request, token, *args, **kwargs):
        return token.is_accessible_by(request.user)

    def has_modify_permissions(self, request, token, *args, **kwargs):
        return token.is_mutable_by(request.user)

    def has_delete_permissions(self, request, token, *args, **kwargs):
        return token.is_deletable_by(request.user)

    @webapi_check_local_site
    @webapi_login_required
    @webapi_response_errors(DOES_NOT_EXIST, INVALID_FORM_DATA, NOT_LOGGED_IN, PERMISSION_DENIED, TOKEN_GENERATION_FAILED)
    @webapi_request_fields(required={b'note': {b'type': six.text_type, 
                 b'description': b'The note explaining the purpose of this token.'}, 
       b'policy': {b'type': six.text_type, 
                   b'description': b'The token access policy, encoded as a JSON string.'}}, allow_unknown=True)
    def create(self, request, note, policy, extra_fields={}, local_site_name=None, *args, **kwargs):
        """Registers a new API token.

        The token value be generated and returned in the payload.

        Callers are expected to provide a note and a policy.

        Note that this may, in theory, fail due to too many token collisions.
        If that happens, please re-try the request.

        Extra data can be stored later lookup. See
        :ref:`webapi2.0-extra-data` for more information.
        """
        try:
            user = resources.user.get_object(request, *args, **kwargs)
        except ObjectDoesNotExist:
            return DOES_NOT_EXIST

        if not self.has_list_access_permissions(request, *args, **kwargs):
            return self.get_no_access_error(request)
        try:
            self._validate_policy(policy)
        except ValueError as e:
            return (
             INVALID_FORM_DATA,
             {b'fields': {b'policy': six.text_type(e)}})

        local_site = self._get_local_site(local_site_name)
        try:
            token = WebAPIToken.objects.generate_token(user, note=note, policy=policy, local_site=local_site)
        except WebAPITokenGenerationError as e:
            return TOKEN_GENERATION_FAILED.with_message(six.text_type(e))

        if extra_fields:
            try:
                self.import_extra_data(token, token.extra_data, extra_fields)
            except ImportExtraDataError as e:
                return e.error_payload

            token.save(update_fields=('extra_data', ))
        return (201,
         {self.item_result_key: token})

    @webapi_check_local_site
    @webapi_login_required
    @webapi_response_errors(DOES_NOT_EXIST, INVALID_FORM_DATA, NOT_LOGGED_IN, PERMISSION_DENIED)
    @webapi_request_fields(optional={b'note': {b'type': six.text_type, 
                 b'description': b'The note explaining the purpose of this token.'}, 
       b'policy': {b'type': six.text_type, 
                   b'description': b'The token access policy, encoded as a JSON string.'}}, allow_unknown=True)
    def update(self, request, extra_fields={}, *args, **kwargs):
        """Updates the information on an existing API token.

        The note, policy, and extra data on the token may be updated.
        See :ref:`webapi2.0-extra-data` for more information.
        """
        try:
            token = self.get_object(request, *args, **kwargs)
        except ObjectDoesNotExist:
            return DOES_NOT_EXIST

        if not self.has_access_permissions(request, token, *args, **kwargs):
            return self.get_no_access_error(request)
        if b'note' in kwargs:
            token.note = kwargs[b'note']
        if b'policy' in kwargs:
            try:
                token.policy = self._validate_policy(kwargs[b'policy'])
            except ValidationError as e:
                return (
                 INVALID_FORM_DATA,
                 {b'fields': {b'policy': e.message}})

        if extra_fields:
            try:
                self.import_extra_data(token, token.extra_data, extra_fields)
            except ImportExtraDataError as e:
                return e.error_payload

        token.save()
        return (
         200,
         {self.item_result_key: token})

    @augment_method_from(WebAPIResource)
    def delete(self, *args, **kwargs):
        """Delete the API token, invalidating all clients using it.

        The API token will be removed from the user's account, and will no
        longer be usable for authentication.

        After deletion, this will return a :http:`204`.
        """
        pass

    @webapi_check_local_site
    @augment_method_from(WebAPIResource)
    def get_list(self, *args, **kwargs):
        """Retrieves a list of API tokens belonging to a user.

        If accessing this API on a Local Site, the results will be limited
        to those associated with that site.

        This can only be accessed by the owner of the tokens, or superusers.
        """
        pass

    @webapi_check_local_site
    @augment_method_from(WebAPIResource)
    def get(self, *args, **kwargs):
        """Retrieves information on a particular API token.

        This can only be accessed by the owner of the tokens, or superusers.
        """
        pass

    def _validate_policy(self, policy_str):
        try:
            policy = json.loads(policy_str)
        except Exception as e:
            raise ValidationError(_(b'The policy is not valid JSON: %s') % six.text_type(e))

        self.model.validate_policy(policy)
        return policy


api_token_resource = APITokenResource()