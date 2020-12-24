# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /rbpowerpack/reports/resources.py
# Compiled at: 2019-06-17 15:11:31
from __future__ import unicode_literals
from django.utils import six
from djblets.webapi.decorators import webapi_login_required, webapi_request_fields, webapi_response_errors
from djblets.webapi.errors import DOES_NOT_EXIST, DUPLICATE_ITEM, NOT_LOGGED_IN, PERMISSION_DENIED
from djblets.webapi.responses import WebAPIResponsePaginated
from reviewboard.webapi.decorators import webapi_check_local_site
from reviewboard.webapi.resources import WebAPIResource
from rbpowerpack.reports.queries import UserQuery

class SavedUserQueryResponsePaginated(WebAPIResponsePaginated):
    """A custom paginated response that doesn't use querysets."""

    def __init__(self, request, results_list=None, *args, **kwargs):
        self.results_list = results_list
        super(SavedUserQueryResponsePaginated, self).__init__(request, *args, **kwargs)

    def get_results(self):
        """Return the results for this page.

        Returns:
            list:
            A list of items for the current page.
        """
        return self.results_list[self.start:self.start + self.max_results]

    def get_total_results(self):
        """Return the total number of results across all pages.

        Returns:
            int:
            The total number of results.
        """
        return len(self.results_list)


class SavedUserQueryResource(WebAPIResource):
    """A resource for managing saved user queries.

    Parts of the Review Board UI involve searching for users in some form. The
    User Selector is a piece of UI which allows searching for users and groups
    and selecting them. The SavedUserQuery is a way of saving common searches
    with a name.

    At the moment, this is only used for Power Pack reports. The eventual goal
    is to make the User Selector usable for choosing assignees of review
    requests in the main Review Board UI, too.

    This API currently exposes different results depending on which user is
    accessing it. This should be considered experimental API at the moment, and
    is subject to change.
    """
    added_in = b'2.0'
    name = b'saved_user_query'
    name_plural = b'saved_user_queries'
    allowed_methods = ('GET', 'POST', 'PUT', 'DELETE')
    uri_object_key_regex = b'[A-Za-z0-9\\. _-]+'
    uri_object_key = b'query_name'
    fields = {b'name': {b'type': six.text_type, 
                 b'description': b'The name of the query.'}, 
       b'usernames': {b'type': six.text_type, 
                      b'description': b'A comma-separated list of usernames to include in the search.'}, 
       b'group_names': {b'type': six.text_type, 
                        b'description': b'A comma-separated list of group names to include in the search.'}}

    def has_list_access_permissions(self, request, *args, **kwargs):
        """Return whether the user has permissions to GET the list resource.
        """
        return request.user.is_authenticated()

    def has_access_permissions(self, request, obj, *args, **kwargs):
        """Return whether the user has permissions to GET an item."""
        return obj.user == request.user

    def has_modify_permissions(self, request, obj, *args, **kwargs):
        """Return whether the user has permissions to PUT an item."""
        return obj.user == request.user

    def has_delete_permissions(self, request, obj, *args, **kwargs):
        """Return whether the user has permissions to DELETE an item."""
        return obj.user == request.user

    @webapi_login_required
    @webapi_check_local_site
    @webapi_response_errors(DOES_NOT_EXIST, NOT_LOGGED_IN, PERMISSION_DENIED)
    def get(self, request, query_name=None, local_site=None, *args, **kwargs):
        """Return the saved query."""
        try:
            obj = UserQuery.from_profile(request.user, local_site, query_name)
            if not self.has_access_permissions(request, obj, *args, **kwargs):
                return self.get_no_access_error(request, obj=obj, *args, **kwargs)
            return (200,
             {self.item_result_key: obj.to_json()})
        except KeyError:
            return DOES_NOT_EXIST

    @webapi_login_required
    @webapi_check_local_site
    @webapi_response_errors(DOES_NOT_EXIST, NOT_LOGGED_IN, PERMISSION_DENIED)
    @webapi_request_fields(optional={b'start': {b'type': int, 
                  b'description': b'The 0-based index of the first result in the list. The start index is usually the previous start index plus the number of previous results. By default, this is 0.'}, 
       b'max-results': {b'type': int, 
                        b'description': b'The maximum number of results to return in this list. By default, this is 25. There is a hard limit of 200; if you need more than 200 results, you will need to make more than one request, using the "next" pagination link.'}}, allow_unknown=True)
    def get_list(self, request, local_site=None, *args, **kwargs):
        """Return the list of saved queries for the user making the request."""
        if not self.has_list_access_permissions(request, local_site=local_site, *args, **kwargs):
            return self.get_no_access_error(request, *args, **kwargs)
        else:
            rsp = super(SavedUserQueryResource, self).get_list(request, local_site=local_site, *args, **kwargs)
            if type(rsp) is tuple:
                data = rsp[1]
                return SavedUserQueryResponsePaginated(request, results_list=[ query.to_json() for query in UserQuery.find(request.user, local_site)
                                                                             ], results_key=self.list_result_key, extra_data=data, **self.build_response_args(request))
            return rsp

    @webapi_login_required
    @webapi_check_local_site
    @webapi_response_errors(DUPLICATE_ITEM, NOT_LOGGED_IN, PERMISSION_DENIED)
    @webapi_request_fields(required={b'name': {b'type': six.text_type, 
                 b'description': b'The name of the saved query.'}, 
       b'usernames': {b'type': six.text_type, 
                      b'description': b'A comma-separated list of usernames to include in the search.'}, 
       b'group_names': {b'type': six.text_type, 
                        b'description': b'A comma-separated list of group names to include in the search.'}})
    def create(self, request, name=None, usernames=None, group_names=None, local_site=None, *args, **kwargs):
        """Create a new saved query.

        This will be accessible to the user making the request with the given
        name.
        """
        user = request.user
        try:
            UserQuery.from_profile(user, local_site, name)
            return DUPLICATE_ITEM
        except KeyError:
            pass

        query = UserQuery(name=name, user=request.user, local_site=local_site, usernames=[ username for username in usernames.split(b',') if username
                                                                                         ], group_names=[ group_name for group_name in group_names.split(b',') if group_name
                                                                                                        ])
        query.save()
        return (
         201,
         {self.item_result_key: query.to_json()})

    @webapi_login_required
    @webapi_check_local_site
    @webapi_request_fields(optional={b'name': {b'type': six.text_type, 
                 b'description': b'The name of the saved query.'}, 
       b'usernames': {b'type': six.text_type, 
                      b'description': b'A comma-separated list of usernames to include in the search.'}, 
       b'group_names': {b'type': six.text_type, 
                        b'description': b'A comma-separated list of group names to include in the search.'}})
    @webapi_response_errors(DOES_NOT_EXIST, NOT_LOGGED_IN, PERMISSION_DENIED)
    def update(self, request, query_name=None, local_site=None, name=None, usernames=None, group_names=None, *args, **kwargs):
        """Update an existing saved query."""
        try:
            obj = UserQuery.from_profile(request.user, local_site, query_name)
            if not self.has_modify_permissions(request, obj, *args, **kwargs):
                return self.get_no_access_error(request, obj=obj, *args, **kwargs)
            if name is not None:
                obj.name = name
            if usernames is not None:
                obj.usernames = [ username for username in usernames.split(b',') if username
                                ]
            if group_names is not None:
                obj.group_names = [ group_name for group_name in group_names.split(b',') if group_name
                                  ]
            obj.save()
            return (
             200,
             {self.item_result_key: obj.to_json()})
        except KeyError:
            return DOES_NOT_EXIST

        return

    @webapi_login_required
    @webapi_check_local_site
    @webapi_response_errors(DOES_NOT_EXIST, NOT_LOGGED_IN, PERMISSION_DENIED)
    def delete(self, request, query_name=None, local_site=None, *args, **kwargs):
        """Delete a saved query."""
        try:
            obj = UserQuery.from_profile(request.user, local_site, query_name)
            if not self.has_delete_permissions(request, obj, *args, **kwargs):
                return self.get_no_access_error(request, obj=obj, *args, **kwargs)
            obj.delete()
            return (204, {})
        except KeyError:
            return DOES_NOT_EXIST


saved_user_query_resource = SavedUserQueryResource()