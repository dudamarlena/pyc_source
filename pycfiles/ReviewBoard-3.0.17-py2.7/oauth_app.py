# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/webapi/resources/oauth_app.py
# Compiled at: 2020-02-11 04:03:57
"""The OAuth2 application resource."""
from __future__ import unicode_literals
from collections import defaultdict
from itertools import chain
from django.contrib.auth.models import User
from django.db.models.query import Q
from django.utils import six
from django.utils.six.moves import filter
from django.utils.translation import ugettext_lazy as _
from djblets.util.decorators import augment_method_from
from djblets.webapi.decorators import webapi_login_required, webapi_request_fields, webapi_response_errors
from djblets.webapi.errors import DOES_NOT_EXIST, INVALID_FORM_DATA
from oauth2_provider.generators import generate_client_secret
from reviewboard.oauth.forms import ApplicationChangeForm, ApplicationCreationForm
from reviewboard.oauth.models import Application
from reviewboard.webapi.base import WebAPIResource
from reviewboard.webapi.decorators import webapi_check_local_site
from reviewboard.webapi.mixins import UpdateFormMixin

class OAuthApplicationResource(UpdateFormMixin, WebAPIResource):
    """Manage OAuth2 applications."""
    model = Application
    name = b'oauth_app'
    verbose_name = _(b'OAuth2 Applications')
    uri_object_key = b'app_id'
    form_class = ApplicationChangeForm
    add_form_class = ApplicationCreationForm
    allowed_methods = ('GET', 'POST', 'PUT', 'DELETE')
    added_in = b'3.0'
    fields = {b'authorization_grant_type': {b'type': (
                                             Application.GRANT_AUTHORIZATION_CODE,
                                             Application.GRANT_CLIENT_CREDENTIALS,
                                             Application.GRANT_IMPLICIT,
                                             Application.GRANT_PASSWORD), 
                                     b'description': b'How the authorization is granted to the application. This will be one of %s, %s, %s, or %s.' % (
                                                    Application.GRANT_AUTHORIZATION_CODE,
                                                    Application.GRANT_CLIENT_CREDENTIALS,
                                                    Application.GRANT_IMPLICIT,
                                                    Application.GRANT_PASSWORD)}, 
       b'client_id': {b'type': six.text_type, 
                      b'description': b'The client ID. This will be used by your application to identify itself to Review Board.'}, 
       b'client_secret': {b'type': six.text_type, 
                          b'description': b'The client secret. This should only be known to Review Board and the application.'}, 
       b'client_type': {b'type': (
                                Application.CLIENT_CONFIDENTIAL,
                                Application.CLIENT_PUBLIC), 
                        b'description': b'The type of client. Confidential clients must be able to keep user password secure.\n\nThis will be one of %s or %s.' % (
                                       Application.CLIENT_CONFIDENTIAL,
                                       Application.CLIENT_PUBLIC)}, 
       b'enabled': {b'type': bool, 
                    b'description': b'Whether or not this application is enabled.\n\nIf disabled, authentication and API access will not be available for clients using this application.'}, 
       b'extra_data': {b'type': dict, 
                       b'description': b'Extra information associated with the application.'}, 
       b'id': {b'type': int, 
               b'description': b'The application ID. This uniquely identifies the application when communicating with the Web API.'}, 
       b'name': {b'type': six.text_type, 
                 b'description': b'The application name.'}, 
       b'redirect_uris': {b'type': [
                                  six.text_type], 
                          b'description': b'The list of allowed URIs to redirect to.'}, 
       b'skip_authorization': {b'type': bool, 
                               b'description': b'Whether or not users will be prompted for authentication.\n\nThis field is only editable by administrators.'}, 
       b'user': {b'type': b'reviewboard.webapi.resources.user.UserResource', 
                 b'description': b'The user who created the application.'}}
    CREATE_REQUIRED_FIELDS = {b'authorization_grant_type': {b'type': (
                                             Application.GRANT_AUTHORIZATION_CODE,
                                             Application.GRANT_CLIENT_CREDENTIALS,
                                             Application.GRANT_IMPLICIT,
                                             Application.GRANT_PASSWORD), 
                                     b'description': b'How authorization is granted to the application.'}, 
       b'client_type': {b'type': (
                                Application.CLIENT_CONFIDENTIAL,
                                Application.CLIENT_PUBLIC), 
                        b'description': b'The client type. Confidential clients must be able to keep user passwords secure.'}, 
       b'name': {b'type': six.text_type, 
                 b'description': b'The application name.'}}
    CREATE_OPTIONAL_FIELDS = {b'enabled': {b'type': bool, 
                    b'description': b'Whether or not the application will be enabled.\n\nIf disabled, authentication and API access will not be available for clients using this application.\n\nDefaults to true when creating a new Application.'}, 
       b'redirect_uris': {b'type': six.text_type, 
                          b'description': b'A comma-separated list of allowed URIs to redirect to.'}, 
       b'skip_authorization': {b'type': bool, 
                               b'description': b'Whether or not users will be prompted for authentication.'}, 
       b'user': {b'type': six.text_type, 
                 b'description': b'The user who owns the application.\n\nThis field is only available to super users.'}}
    UPDATE_OPTIONAL_FIELDS = {b'regenerate_client_secret': {b'type': bool, 
                                     b'description': b'The identifier of the LocalSite to re-assign this Application to.\n\nThe Application will be limited to users belonging to that Local Site and will only be editable via the API for that LocalSite.\n\nIf this is set to the empty string, the Application will become unassigned from all Local Sites and will be available globally.'}}

    def serialize_redirect_uris_field(self, obj, **kwargs):
        """Serialize the ``redirect_uris`` field to a list.

        Args:
            obj (reviewboard.oauth.models.Application):
                The application being serialized.

            **kwargs (dict):
                Ignored keyword arguments

        Returns:
            list of unicode:
            The list of allowable redirect URIs.
        """
        return list(filter(len, obj.redirect_uris.split()))

    def has_access_permissions(self, request, obj, local_site=None, *args, **kwargs):
        """Return whether or not the user has permission to access this object.

        See :py:meth:`Application.is_accessible_by()
        <reviewboard.oauth.models.Application.is_accessible_by>` for details of
        when a user has access permissions.

        Args:
            request (django.http.HttpRequest):
                The current HTTP request.

            obj (reviewboard.oauth.models.Application):
                The application to check for delete permission against.

            local_site (reviewboard.site.models.LocalSite, optional):
                The current Local Site, if any.

            *args (tuple):
                Ignored positional arguments.

            **kwargs (dict):
                Ignored keyword arguments.

        Returns:
            bool:
            Whether or not the user has delete permissions.
        """
        return obj.is_accessible_by(request.user, local_site=local_site)

    def has_modify_permissions(self, request, obj, local_site=None, *args, **kwargs):
        """Return whether or not the user has modify permissions.

        See :py:meth:`Application.is_mutable_by()
        <reviewboard.oauth.models.Application.is_mutable_by>` for details of
        when a user has modify permissions.

        Args:
            request (django.http.HttpRequest):
                The current HTTP request.

            obj (reviewboard.oauth.models.Application):
                The application to check for delete permission against.

            local_site (reviewboard.site.models.LocalSite, optional):
                The current LocalSite, if any.

            *args (tuple):
                Ignored positional arguments.

            **kwargs (dict):
                Ignored keyword arguments.

        Returns:
            bool:
            Whether or not the user has modify permissions.
        """
        return obj.is_mutable_by(request.user, local_site=local_site)

    def has_delete_permissions(self, request, obj, local_site=None, *args, **kwargs):
        """Return whether or not the user has delete permissions.

        See :py:meth:`Application.is_mutable_by()
        <reviewboard.oauth.models.Application.is_mutable_by>` for details of
        when a user has delete permissions.

        Args:
            request (django.http.HttpRequest):
                The current HTTP request.

            obj (reviewboard.oauth.models.Application):
                The application to check for delete permission against.

            local_site (reviewboard.site.models.LocalSite, optional):
                The current LocalSite, if any.

            *args (tuple):
                Ignored positional arguments.

            **kwargs (dict):
                Ignored keyword arguments.

        Returns:
            bool:
            Whether or not the user has delete permissions.
        """
        return obj.is_mutable_by(request.user, local_site=local_site)

    def get_queryset(self, request, is_list=False, local_site=None, *args, **kwargs):
        """Return the queryset for filtering responses.

        If the ``username`` GET field is set, the returned applications will be
        limited to the those owned by that user.

        Args:
            request (django.http.HttpRequest):
                The current HTTP request.

            is_list (bool, optional):
                Whether or not the list resource is being accessed.

            local_site (reviewboard.site.models.LocalSite, optional):
                The current LocalSite, if any.

            *args (tuple):
                Additional positional arguments.

            **kwargs (dict):
                Additional keyword arguments.

        Returns:
            django.db.models.query.QuerySet:
            The applications the user has access to.
        """
        if not request.user.is_authenticated():
            return Application.objects.none()
        q = Q(local_site=local_site)
        if not (request.user.is_superuser or local_site and local_site.admins.filter(pk=request.user.pk).exists()):
            q &= Q(user=request.user)
        username = request.GET.get(b'username')
        if username:
            q &= Q(user__username=username)
        return Application.objects.filter(q)

    @webapi_check_local_site
    @webapi_login_required
    @augment_method_from(WebAPIResource)
    def get(self, *args, **kwargs):
        """Return information on a particular OAuth2 application.

        The client's logged in user must either own the app in question or
        be an administrator.
        """
        pass

    @webapi_check_local_site
    @webapi_login_required
    @webapi_request_fields(optional={b'username': {b'type': six.text_type, 
                     b'description': b'If present, the results will be filtered to Applications owned by the specified user.\n\nOnly administrators have access to Applications owned by other users.'}})
    @augment_method_from(WebAPIResource)
    def get_list(self, *args, **kwargs):
        """Return information about all OAuth2 applications.

        This will be limited to the client's logged in user's applications
        unless the user is an administrator.
        """
        pass

    @webapi_check_local_site
    @webapi_login_required
    @webapi_response_errors(DOES_NOT_EXIST)
    @webapi_request_fields(required=CREATE_REQUIRED_FIELDS, optional=CREATE_OPTIONAL_FIELDS, allow_unknown=True)
    def create(self, request, parsed_request_fields, extra_fields, local_site=None, *args, **kwargs):
        """Create a new OAuth2 application.

        The ``client_secret`` and ``client_id`` fields will be auto-generated
        and returned in the response (providing the request is successful).

        Extra data can be stored later lookup. See
        :ref:`webapi2.0-extra-data` for more information.
        """
        return self._create_or_update(request, parsed_request_fields, extra_fields, None, local_site)

    @webapi_check_local_site
    @webapi_login_required
    @webapi_response_errors(INVALID_FORM_DATA)
    @webapi_request_fields(optional=dict(chain(six.iteritems(CREATE_REQUIRED_FIELDS), six.iteritems(CREATE_OPTIONAL_FIELDS), six.iteritems(UPDATE_OPTIONAL_FIELDS))), allow_unknown=True)
    def update(self, request, parsed_request_fields, extra_fields, local_site=None, *args, **kwargs):
        """Update an OAuth2 application.

        Extra data can be stored later lookup. See
        :ref:`webapi2.0-extra-data` for more information.
        """
        try:
            app = self.get_object(request, local_site=local_site, *args, **kwargs)
        except Application.DoesNotExist:
            return DOES_NOT_EXIST

        if not self.has_modify_permissions(request, app, local_site=local_site):
            return self.get_no_access_error(request)
        try:
            regenerate_secret = parsed_request_fields.pop(b'regenerate_client_secret')
        except KeyError:
            regenerate_secret = False

        return self._create_or_update(request, parsed_request_fields, extra_fields, app, local_site, regenerate_secret=regenerate_secret)

    @webapi_login_required
    @webapi_check_local_site
    def delete(self, request, local_site=None, *args, **kwargs):
        """Delete the OAuth2 application.

        After a successful delete, this will return :http:`204`.
        """
        try:
            app = self.get_object(request, local_site=local_site, *args, **kwargs)
        except Application.DoesNotExist:
            return DOES_NOT_EXIST

        if not self.has_delete_permissions(request, app, local_site):
            return self.get_no_access_error(request)
        app.delete()
        return (
         204, {})

    def _create_or_update(self, request, parsed_request_fields, extra_fields, instance, local_site, regenerate_secret=False):
        """Create or update an application.

        Args:
            request (django.http.HttpRequest):
                The current HTTP request.

            parsed_request_fields (dict):
                The parsed request fields.

            extra_fields (dict):
                Extra data fields.

            instance (reviewboard.oauth.models.Application):
                The current application to update or ``None`` if we are
                creating a new application.

            local_site (reviewboard.site.models.LocalSite):
                The LocalSite the API is being accessed through.

            regenerate_secret (bool, optional):
                Whether or not the secret on the

        Returns:
            tuple:
            A 2-tuple of:

            * The HTTP status (:py:class:`int` or
              :py:class:`djblets.webapi.error.WebAPIError`).
            * The response body to encode (:py:class:`dict`).
        """
        try:
            username = parsed_request_fields.pop(b'user')
        except KeyError:
            username = None

        skip_authorization = parsed_request_fields.get(b'skip_authorization', False)
        change_owner = username is not None and username != request.user.username
        errors = defaultdict(list)
        user_pk = None
        if skip_authorization or change_owner:
            if not (request.user.is_authenticated() and (request.user.is_superuser or request.local_site is not None and request.local_site.is_mutable_by(request.user))):
                err_msg = b'You do not have permission to set this field.'
                if skip_authorization:
                    errors[b'skip_authorization'].append(err_msg)
                if change_owner:
                    errors[b'user'].append(err_msg)
            elif change_owner:
                try:
                    if request.local_site:
                        qs = local_site.users
                    else:
                        qs = User.objects
                    user_pk = qs.values_list(b'pk', flat=True).get(username=username)
                except User.DoesNotExist:
                    errors[b'user'].append(b'The user "%s" does not exist.' % username)

        if errors:
            return (INVALID_FORM_DATA,
             {b'fields': errors})
        else:
            form_data = parsed_request_fields.copy()
            if user_pk is None and instance is None:
                if not not change_owner:
                    raise AssertionError
                    user_pk = request.user.pk
                if user_pk is not None:
                    form_data[b'user'] = user_pk
                instance or form_data.setdefault(b'enabled', True)
                if local_site:
                    form_data[b'local_site'] = local_site.pk
            elif regenerate_secret:
                instance.client_secret = generate_client_secret()
                instance.original_user = None
            return self.handle_form_request(data=form_data, request=request, instance=instance, extra_fields=extra_fields)


oauth_app_resource = OAuthApplicationResource()