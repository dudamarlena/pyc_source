# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/webapi/resources/hosting_service_account.py
# Compiled at: 2020-02-11 04:03:57
from __future__ import unicode_literals
from django.utils import six
from djblets.util.decorators import augment_method_from
from djblets.webapi.decorators import webapi_login_required, webapi_response_errors, webapi_request_fields
from djblets.webapi.errors import INVALID_FORM_DATA, NOT_LOGGED_IN, PERMISSION_DENIED
from reviewboard.hostingsvcs.errors import AuthorizationError
from reviewboard.hostingsvcs.models import HostingServiceAccount
from reviewboard.hostingsvcs.service import get_hosting_service
from reviewboard.webapi.base import WebAPIResource
from reviewboard.webapi.decorators import webapi_check_login_required, webapi_check_local_site
from reviewboard.webapi.errors import BAD_HOST_KEY, HOSTINGSVC_AUTH_ERROR, REPO_AUTHENTICATION_ERROR, SERVER_CONFIG_ERROR, UNVERIFIED_HOST_CERT, UNVERIFIED_HOST_KEY
from reviewboard.webapi.resources import resources

class HostingServiceAccountResource(WebAPIResource):
    """Provides information and allows linking of hosting service accounts.

    The list of accounts tied to hosting services can be retrieved, and new
    accounts can be linked through an HTTP POST.
    """
    item_resource_added_in = b'1.6.7'
    list_resource_added_in = b'2.5'
    name = b'hosting_service_account'
    model = HostingServiceAccount
    fields = {b'id': {b'type': int, 
               b'description': b'The numeric ID of the hosting service account.'}, 
       b'username': {b'type': six.text_type, 
                     b'description': b'The username of the account.'}, 
       b'service': {b'type': six.text_type, 
                    b'description': b'The ID of the service this account is on.'}}
    uri_object_key = b'account_id'
    allowed_methods = ('GET', 'POST')
    item_child_resources = [
     resources.remote_repository]

    @webapi_check_login_required
    def get_queryset(self, request, local_site_name=None, is_list=False, *args, **kwargs):
        local_site = self._get_local_site(local_site_name)
        queryset = self.model.objects.accessible(visible_only=True, local_site=local_site)
        if is_list:
            if b'username' in request.GET:
                queryset = queryset.filter(username=request.GET[b'username'])
            if b'service' in request.GET:
                queryset = queryset.filter(service_name=request.GET[b'service'])
        return queryset

    def has_access_permissions(self, request, account, *args, **kwargs):
        return account.is_accessible_by(request.user)

    def has_modify_permissions(self, request, account, *args, **kwargs):
        return account.is_mutable_by(request.user)

    def has_delete_permissions(self, request, account, *args, **kwargs):
        return account.is_mutable_by(request.user)

    def get_links(self, items, obj=None, *args, **kwargs):
        links = super(HostingServiceAccountResource, self).get_links(items, obj=obj, *args, **kwargs)
        if obj:
            service = obj.service
            if not service.supports_list_remote_repositories:
                del links[b'remote_repositories']
        return links

    @webapi_check_local_site
    @webapi_request_fields(optional={b'username': {b'type': six.text_type, 
                     b'description': b'Filter accounts by username.', 
                     b'added_in': b'2.5'}, 
       b'service': {b'type': six.text_type, 
                    b'description': b'Filter accounts by the hosting service ID.', 
                    b'added_in': b'2.5'}})
    @augment_method_from(WebAPIResource)
    def get_list(self, request, *args, **kwargs):
        """Retrieves the list of accounts on the server.

        This will only list visible accounts. Any account that the
        administrator has hidden will be excluded from the list.
        """
        pass

    @webapi_check_local_site
    @augment_method_from(WebAPIResource)
    def get(self, *args, **kwargs):
        """Retrieves information on a particular account.

        This will only return very basic information on the account.
        Authentication information is not provided.
        """
        pass

    def serialize_service_field(self, obj, **kwargs):
        return obj.service_name

    @webapi_check_local_site
    @webapi_login_required
    @webapi_response_errors(BAD_HOST_KEY, INVALID_FORM_DATA, NOT_LOGGED_IN, PERMISSION_DENIED, REPO_AUTHENTICATION_ERROR, SERVER_CONFIG_ERROR, UNVERIFIED_HOST_CERT, UNVERIFIED_HOST_KEY)
    @webapi_request_fields(required={b'username': {b'type': six.text_type, 
                     b'description': b'The username on the account.'}, 
       b'service_id': {b'type': six.text_type, 
                       b'description': b'The registered ID of the service for the account.'}}, optional={b'hosting_url': {b'type': six.text_type, 
                        b'description': b'The hosting URL on the account, if the hosting service is self-hosted.', 
                        b'added_in': b'1.7.8'}, 
       b'password': {b'type': six.text_type, 
                     b'description': b'The password on the account, if the hosting service needs it.'}})
    def create(self, request, username, service_id, password=None, hosting_url=None, local_site_name=None, *args, **kwargs):
        """Creates a hosting service account.

        The ``service_id`` is a registered HostingService ID. This must be
        known beforehand, and can be looked up in the Review Board
        administration UI.
        """
        local_site = self._get_local_site(local_site_name)
        if not HostingServiceAccount.objects.can_create(request.user, local_site):
            return self.get_no_access_error(request)
        service = get_hosting_service(service_id)
        if not service:
            return (INVALID_FORM_DATA,
             {b'fields': {b'service': [
                                       b'This is not a valid service name']}})
        if service.self_hosted and not hosting_url:
            return (INVALID_FORM_DATA,
             {b'fields': {b'hosting_url': [
                                           b'This field is required']}})
        account = HostingServiceAccount(service_name=service_id, username=username, hosting_url=hosting_url, local_site=local_site)
        service = account.service
        if service.needs_authorization:
            try:
                service.authorize(request, username, password, hosting_url, local_site_name)
            except AuthorizationError as e:
                return (
                 HOSTINGSVC_AUTH_ERROR,
                 {b'reason': six.text_type(e)})

        account.save()
        return (
         201,
         {self.item_result_key: account})


hosting_service_account_resource = HostingServiceAccountResource()