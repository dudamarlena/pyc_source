# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/search/views.py
# Compiled at: 2020-02-11 04:03:56
"""Views for searching."""
from __future__ import unicode_literals
from collections import OrderedDict
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import six
from haystack.generic_views import SearchView
from reviewboard.accounts.mixins import CheckLoginRequiredViewMixin, UserProfileRequiredViewMixin
from reviewboard.avatars import avatar_services
from reviewboard.reviews.models import ReviewRequest
from reviewboard.search import search_backend_registry
from reviewboard.search.forms import RBSearchForm
from reviewboard.site.urlresolvers import local_site_reverse
from reviewboard.site.mixins import CheckLocalSiteAccessViewMixin

class RBSearchView(CheckLoginRequiredViewMixin, CheckLocalSiteAccessViewMixin, UserProfileRequiredViewMixin, SearchView):
    """The Review Board search view."""
    template_name = b'search/results.html'
    disabled_template_name = b'search/search_disabled.html'
    form_class = RBSearchForm
    load_all = False
    ADJACENT_PAGES = 5

    @property
    def paginate_by(self):
        """The number of search results per page."""
        return search_backend_registry.results_per_page

    def dispatch(self, request, local_site=None, *args, **kwargs):
        """Dispatch the view.

        If search is disabled, the search will not be performed and the user
        will be informed.

        Args:
            request (django.http.HttpRequest):
                The current HTTP request.

            local_site (reviewboard.site.models.LocalSite):
                The LocalSite on which the search is being performed.

            *args (tuple, unused):
                Ignored positional arguments.

            **kwargs (dict, unused):
                Ignored keyword arguments.

        Returns:
            django.http.HttpResponse:
            The HTTP response for the search.
        """
        if not search_backend_registry.search_enabled:
            return render(request, self.disabled_template_name)
        form_class = self.get_form_class()
        form = form_class(user=request.user, local_site=local_site, **self.get_form_kwargs())
        if not form.is_valid():
            return self.form_invalid(form)
        query = form.cleaned_data.get(self.search_field, b'')
        if not query:
            return HttpResponseRedirect(local_site_reverse(b'all-review-requests', local_site=local_site))
        if query.isdigit():
            try:
                review_request = ReviewRequest.objects.for_id(query, local_site)
            except ReviewRequest.DoesNotExist:
                pass
            else:
                if review_request.is_accessible_by(self.request.user, local_site=local_site, request=request):
                    return HttpResponseRedirect(review_request.get_absolute_url())

        return self.form_valid(form)

    def get_context_data(self, form=None, **kwargs):
        """Return context data for rendering the view.

        Args:
            form (reviewboard.search.forms.RBSearchForm):
                The search form instance.

                This will be included in the returned dictionary.

            **kwargs (dict):
                Additional context to be added to the returned dictionary.

        Returns:
            dict:
            The context dictionary.
        """
        context = super(RBSearchView, self).get_context_data(form=form, **kwargs)
        paginator = context[b'paginator']
        page_obj = context[b'page_obj']
        object_list = context[b'object_list']
        page_nums = range(max(1, page_obj.number - self.ADJACENT_PAGES), min(paginator.num_pages, page_obj.number + self.ADJACENT_PAGES) + 1)
        active_filters = form.cleaned_data.get(b'model_filter', [
         form.FILTER_ALL])
        context.update({b'filter_types': OrderedDict((filter_id, dict(active=(filter_id in active_filters), **filter_type)) for filter_id, filter_type in six.iteritems(form.FILTER_TYPES)), 
           b'hits_returned': len(object_list), 
           b'page_numbers': page_nums, 
           b'show_first_page': 1 not in page_nums, 
           b'show_last_page': paginator.num_pages not in page_nums})
        return context

    def render_to_response(self, context, **response_kwargs):
        """Render the search page.

        Args:
            context (dict):
                A dictionary of context from :py:meth:`get_context_data`.

            **response_kwargs (dict);
                Keyword arguments to be passed to the response class.

        Returns:
            django.http.HttpResponse:
            The rendered response.
        """
        show_users = False
        if avatar_services.avatars_enabled:
            show_users = any(filter_type[b'active'] and User in filter_type[b'models'] for filter_type in six.itervalues(context[b'filter_types']))
        if show_users:
            page_obj = context[b'page_obj']
            user_pks = {int(result.pk) for result in page_obj if result.content_type() == b'auth.user' if result.content_type() == b'auth.user'}
            users = {user.pk:user for user in User.objects.filter(pk__in=user_pks).select_related(b'profile')}
            for result in page_obj:
                if result.content_type() == b'auth.user':
                    result.user = users[int(result.pk)]

        return super(RBSearchView, self).render_to_response(context, **response_kwargs)