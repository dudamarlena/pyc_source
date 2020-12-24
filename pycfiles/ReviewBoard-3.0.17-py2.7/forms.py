# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/search/forms.py
# Compiled at: 2020-02-11 04:03:56
"""Forms for searching Review Board."""
from __future__ import unicode_literals
from collections import OrderedDict
from django import forms
from django.contrib.auth.models import User
from django.utils import six
from django.utils.translation import ugettext_lazy as _
from haystack.forms import ModelSearchForm
from haystack.inputs import Raw
from haystack.query import SQ
from reviewboard.reviews.models import Group, ReviewRequest
from reviewboard.scmtools.models import Repository
from reviewboard.search.indexes import BaseSearchIndex

class RBSearchForm(ModelSearchForm):
    """The Review Board search form.

    This form is capable of searching for :py:class:`ReviewRequests
    <reviewboard.reviews.models.review_request.ReviewRequest>` and
    :py:class:`Users <django.contrib.auth.models.User>`.
    """
    FILTER_ALL = b''
    FILTER_REVIEW_REQUESTS = b'reviewrequests'
    FILTER_USERS = b'users'
    FILTER_TYPES = OrderedDict([
     (
      FILTER_ALL,
      {b'models': [
                   ReviewRequest, User], 
         b'name': _(b'All results')}),
     (
      FILTER_REVIEW_REQUESTS,
      {b'models': [
                   ReviewRequest], 
         b'name': _(b'Review Requests')}),
     (
      FILTER_USERS,
      {b'models': [
                   User], 
         b'name': _(b'Users')})])
    model_filter = forms.MultipleChoiceField(choices=((filter_id, filter_type[b'name']) for filter_id, filter_type in six.iteritems(FILTER_TYPES)), required=False)
    id = forms.IntegerField(required=False)

    def __init__(self, user=None, local_site=None, **kwargs):
        """Initialize the search form.

        Args:
            user (django.contrib.auth.models.User):
                The user performing the search.

                Results will be limited to those visible to the user.

            local_site (reviewboard.site.models.LocalSite):
                The Local Site the search is being performed on.

                Results will be limited to those on the LocalSite.

            **kwargs (dict):
                Additional keyword arguments to forward to the parent form.
        """
        super(RBSearchForm, self).__init__(**kwargs)
        self.user = user
        self.local_site = local_site

    def clean_q(self):
        """Clean the ``q`` field.

        The field will be stripped of leading and trailing whitespace.

        Returns:
            unicode:
            The stripped query.
        """
        return self.cleaned_data[b'q'].strip()

    def clean_model_filter(self):
        """Clean the ``model_filter`` field.

        If no filter is provided, the default (all models) will be used.

        Returns:
            list of unicode:
            The cleaned ``filter`` field.
        """
        return self.cleaned_data[b'model_filter'] or [b'']

    def search(self):
        """Perform a search.

        Returns:
            haystack.query.SearchQuerySet:
            The search results.
        """
        if not self.is_valid():
            return self.no_query_found()
        user = self.user
        q = self.cleaned_data[b'q']
        id_q = self.cleaned_data.get(b'id')
        model_filters = set()
        for filter_type in self.cleaned_data.get(b'model_filter', [b'']):
            model_filters.update(self.FILTER_TYPES[filter_type][b'models'])

        model_filters = list(model_filters)
        sqs = self.searchqueryset.filter(content=Raw(q)).models(*model_filters)
        if id_q:
            sqs = sqs.filter_or(SQ(id=q))
        if self.local_site:
            local_site_id = self.local_site.pk
        else:
            local_site_id = BaseSearchIndex.NO_LOCAL_SITE_ID
        sqs = sqs.filter_and(local_sites__contains=local_site_id)
        if not user.is_superuser:
            private_sq = SQ(django_ct=b'reviews.reviewrequest') & SQ(private=True)
            if user.is_authenticated():
                accessible_repo_ids = list(Repository.objects.accessible_ids(user, visible_only=False, local_site=self.local_site))
                accessible_group_ids = Group.objects.accessible_ids(user, visible_only=False)
                repository_sq = SQ(private_repository_id__in=[
                 0] + accessible_repo_ids)
                target_groups_sq = SQ(private_target_groups__contains=0)
                for pk in accessible_group_ids:
                    target_groups_sq |= SQ(private_target_groups__contains=pk)

                target_users_sq = SQ(target_users__contains=user.pk)
                private_sq &= ~(SQ(username=user.username) | repository_sq & (target_users_sq | target_groups_sq))
            sqs = sqs.exclude(private_sq)
        return sqs.order_by(b'-last_updated')