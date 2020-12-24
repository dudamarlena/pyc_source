# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/webapi/resources/search.py
# Compiled at: 2020-02-11 04:03:57
from __future__ import unicode_literals
from django.db.models.query import Q
from django.utils import six
from djblets.webapi.decorators import webapi_request_fields
from djblets.webapi.resources.user import UserResource as DjbletsUserResource
from reviewboard.reviews.models import Group, ReviewRequest
from reviewboard.search import search_backend_registry
from reviewboard.search.forms import RBSearchForm
from reviewboard.webapi.base import WebAPIResource
from reviewboard.webapi.decorators import webapi_check_login_required, webapi_check_local_site

class SearchResource(WebAPIResource, DjbletsUserResource):
    """
    Provides information on users, groups and review requests.

    This is the resource for the autocomplete widget for quick search. This
    resource helps filter for users, groups and review requests.
    """
    added_in = b'1.6'
    name = b'search'
    singleton = True
    MIN_SUMMARY_LEN = 4

    def has_access_permissions(self, *args, **kwargs):
        """Return whether or not users have access to this resource.

        This resource is accessible to any users that have access to the API.

        Args:
            *args (tuple):
                Ignored positional arguments.

            **kwargs (dict):
                Ignored keyword arguments.

        Returns:
            bool:
            Always ``True``.
        """
        return True

    @webapi_request_fields(optional={b'q': {b'type': six.text_type, 
              b'description': b'The text to search for.'}, 
       b'displayname': {b'type': bool, 
                        b'description': b'This field is deprecated and ignored. It will be removed in a future release of Review Board.'}, 
       b'fullname': {b'type': bool, 
                     b'description': b'Whether or not to include users whose full name includes the search text.'}, 
       b'id': {b'type': int, 
               b'description': b'A specific review request ID to search for.'}, 
       b'max_results': {b'type': int, 
                        b'description': b'The maximum number of results to return for each type of matching object. By default, this is 25. There is a hard limit of 200.'}}, allow_unknown=True)
    @webapi_check_local_site
    @webapi_check_login_required
    def get(self, request, max_results=None, *args, **kwargs):
        """Returns information on users, groups and review requests.

        This is used by the autocomplete widget for quick search to get
        information on users, groups and review requests. This function returns
        users' first name, last name and username, groups' name and display
        name, and review requests' ID and summary.
        """
        max_results = min(max_results or 25, 200)
        try:
            kwargs[b'id_q'] = kwargs.pop(b'id')
        except KeyError:
            pass

        return (
         200,
         {self.name: {b'users': self._search_users(request=request, max_results=max_results, *args, **kwargs), 
                        b'groups': self._search_groups(request=request, max_results=max_results, *args, **kwargs), 
                        b'review_requests': self._search_review_requests(request=request, max_results=max_results, *args, **kwargs)}})

    def _search_users(self, request, max_results, local_site=None, fullname=None, q=None, id_q=None, *args, **kwargs):
        """Search for users and return the results.

        Args:
            request (django.http.HttpRequest):
                The current request.

            max_results (int):
                The maximum number of results to return.

            local_site (reviewboard.site.models.LocalSite, optional):
                The current local site.

            fullname (bool, optional):
                Whether or not to perform a search against the users' full
                names.

            q (unicode, optional):
                The search text.

            id_q (int, optional):
                An optional ID to search against user IDs.

            *args (tuple):
                Ignored positional arguments.

            **kwargs (dict):
                Ignored keyword arguments.

        Returns:
            django.db.models.query.QuerySet or list:
            A query set for users matching the given arguments.
        """
        if search_backend_registry.search_enabled and search_backend_registry.on_the_fly_indexing_enabled:
            form = RBSearchForm(user=request.user, local_site=local_site, data={b'q': q, 
               b'id_q': id_q, 
               b'model_filter': [
                               RBSearchForm.FILTER_USERS]})
            results = []
            for result in form.search()[:max_results]:
                raw_user = {b'id': result.pk, 
                   b'username': result.username, 
                   b'url': result.url}
                if not result.is_profile_private:
                    raw_user[b'fullname'] = result.full_name
                results.append(raw_user)

            return results
        if local_site:
            users = local_site.users.filter(is_active=True)
        else:
            users = self.model.objects.filter(is_active=True)
        if q:
            parts = q.split(b' ', 1)
            if len(parts) > 1:
                query = Q(first_name__istartswith=parts[0]) & Q(last_name__istartswith=parts[1]) | Q(first_name__istartswith=parts[1]) & Q(last_name__istartswith=parts[0])
                if fullname:
                    query |= Q(first_name__istartswith=q) | Q(last_name__istartswith=q)
                query &= Q(profile__is_private=False)
            else:
                query = Q(username__istartswith=q) | Q(profile__is_private=False) & (Q(first_name__istartswith=q) | Q(last_name__istartswith=q))
            users = users.filter(query)
        return users[:max_results]

    def _search_groups(self, request, max_results, local_site=None, q=None, *args, **kwargs):
        """Search for review groups and return the results.

        Args:
            request (django.http.HttpRequest):
                The current HTTP request.

            max_results (int):
                The maximum number of results to return.

            local_site (reviewboard.site.models.LocalSite, optional):
                The current local site.

            q (unicode, optional):
                The search text.

            *args (tuple):
                Ignored positional arguments.

            **kwargs (dict):
                Ignored keyword arguments.

        Returns:
            django.db.models.query.QuerySet:
            A query set for review groups matching the given arguments.
        """
        groups = Group.objects.accessible(request.user, local_site=local_site)
        if q:
            groups = groups.filter(Q(name__istartswith=q) | Q(display_name__istartswith=q))
        return groups.filter(visible=True)[:max_results]

    def _search_review_requests(self, request, max_results, local_site=None, q=None, id_q=None, *args, **kwargs):
        """Search for a review request and return the results.

        If indexed search is enabled, this will use the search index. Otherwise
        it will query against the database.

        Args:
            local_site (reviewboard.site.models.LocalSite, optional):
                The current local site.

            max_results (int):
                The maximum number of results to return.

            q (unicode, optional):
                The search text.

            id_q (int, optional):
                An optional ID to search against review request IDs.

            *args (tuple):
                Ignored positional arguments.

            **kwargs (dict):
                Ignored keyword arguments.

        Returns:
            django.db.models.query.QuerySet or haystack.query.SearchQuerySet:
            A query for review requests matching the given arguments.
        """
        if search_backend_registry.search_enabled and search_backend_registry.on_the_fly_indexing_enabled:
            form = RBSearchForm(user=request.user, local_site=local_site, data={b'q': q, 
               b'id': id_q, 
               b'model_filter': [
                               RBSearchForm.FILTER_REVIEW_REQUESTS]})
            return [ {b'id': result.review_request_id, b'public': True, b'summary': result.summary} for result in form.search()[:max_results]
                   ]
        else:
            review_requests = ReviewRequest.objects.public(filter_private=True, user=request.user, local_site=local_site, status=None)
            query = Q()
            if q:
                if local_site:
                    query |= Q(local_id__istartswith=q)
                else:
                    query |= Q(id__startswith=q)
                if len(q) >= self.MIN_SUMMARY_LEN:
                    query |= Q(summary__istartswith=q)
            if id_q:
                if local_site:
                    query |= Q(local_id__startswith=id_q)
                else:
                    query |= Q(id__startswith=id_q)
            return review_requests.filter(query)[:max_results]


search_resource = SearchResource()