# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/datagrids/grids.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
import pytz
from django.contrib.auth.models import User
from django.http import Http404
from django.utils.translation import ugettext_lazy as _
from djblets.datagrid.grids import Column, DateTimeColumn, DataGrid as DjbletsDataGrid, AlphanumericDataGrid as DjbletsAlphanumericDataGrid
from djblets.util.templatetags.djblets_utils import ageid
from reviewboard.accounts.models import LocalSiteProfile, Profile, ReviewRequestVisit
from reviewboard.datagrids.columns import BugsColumn, DateTimeSinceColumn, DiffSizeColumn, DiffUpdatedColumn, DiffUpdatedSinceColumn, FullNameColumn, GroupMemberCountColumn, GroupsColumn, MyCommentsColumn, NewUpdatesColumn, PendingCountColumn, PeopleColumn, RepositoryColumn, ReviewCountColumn, ReviewGroupStarColumn, ReviewRequestCheckboxColumn, ReviewRequestIDColumn, ReviewRequestStarColumn, ReviewSummaryColumn, ShipItColumn, SummaryColumn, ToMeColumn, UsernameColumn
from reviewboard.datagrids.sidebar import Sidebar, DataGridSidebarMixin
from reviewboard.datagrids.builtin_items import IncomingSection, OutgoingSection, UserGroupsItem, UserProfileItem
from reviewboard.reviews.models import Group, ReviewRequest, Review
from reviewboard.site.urlresolvers import local_site_reverse

class ShowClosedReviewRequestsMixin(object):
    """A mixin for showing or hiding closed review requests."""

    def load_extra_state(self, profile, allow_hide_closed=True):
        """Load extra state for the datagrid."""
        if profile:
            self.show_closed = profile.show_closed
        try:
            self.show_closed = int(self.request.GET.get(b'show-closed', self.show_closed)) != 0
        except ValueError:
            pass

        if allow_hide_closed and not self.show_closed:
            self.queryset = self.queryset.filter(**{self.status_query_field: b'P'})
        self.queryset = self.queryset.filter(**{self.site_query_field: self.local_site})
        if profile and self.show_closed != profile.show_closed:
            profile.show_closed = self.show_closed
            return True
        return False


class DataGridJSMixin(object):
    """Mixin that provides enhanced JavaScript support for datagrids.

    This contains additional information on the JavaScript views/models
    to load for the page, allowing for enhanced functionality in datagrids.
    """
    css_bundle_names = []
    js_bundle_names = []
    js_model_class = b'RB.DatagridPage'
    js_view_class = b'RB.DatagridPageView'
    periodic_reload = False
    extra_js_model_data = None


class DataGrid(DataGridJSMixin, DjbletsDataGrid):
    """Base class for a datagrid in Review Board.

    This contains additional information on JavaScript views/models
    to load for the page.
    """
    pass


class AlphanumericDataGrid(DataGridJSMixin, DjbletsAlphanumericDataGrid):
    """Base class for an alphanumeric datagrid in Review Board.

    This contains additional information on JavaScript views/models
    to load for the page.
    """
    pass


class ReviewRequestDataGrid(ShowClosedReviewRequestsMixin, DataGrid):
    """A datagrid that displays a list of review requests.

    This datagrid accepts the show_closed parameter in the URL, allowing
    submitted review requests to be filtered out or displayed.
    """
    new_updates = NewUpdatesColumn()
    my_comments = MyCommentsColumn()
    star = ReviewRequestStarColumn()
    ship_it = ShipItColumn()
    summary = SummaryColumn()
    submitter = UsernameColumn(label=_(b'Owner'), user_relation=[
     b'submitter'])
    branch = Column(label=_(b'Branch'), db_field=b'branch', shrink=True, sortable=True, link=False)
    bugs_closed = BugsColumn()
    repository = RepositoryColumn()
    time_added = DateTimeColumn(label=_(b'Posted'), detailed_label=_(b'Posted Time'), format=b'F jS, Y, P', shrink=True, css_class=lambda r: ageid(r.time_added))
    last_updated = DateTimeColumn(label=_(b'Last Updated'), format=b'F jS, Y, P', shrink=True, db_field=b'last_updated', field_name=b'last_updated', css_class=lambda r: ageid(r.last_updated))
    diff_updated = DiffUpdatedColumn(format=b'F jS, Y, P', shrink=True, css_class=lambda r: ageid(r.diffset_history.last_diff_updated))
    time_added_since = DateTimeSinceColumn(label=_(b'Posted'), detailed_label=_(b'Posted Time (Relative)'), field_name=b'time_added', shrink=True, css_class=lambda r: ageid(r.time_added))
    last_updated_since = DateTimeSinceColumn(label=_(b'Last Updated'), detailed_label=_(b'Last Updated (Relative)'), shrink=True, db_field=b'last_updated', field_name=b'last_updated', css_class=lambda r: ageid(r.last_updated))
    diff_updated_since = DiffUpdatedSinceColumn(detailed_label=_(b'Diff Updated (Relative)'), shrink=True, css_class=lambda r: ageid(r.diffset_history.last_diff_updated))
    diff_size = DiffSizeColumn()
    review_count = ReviewCountColumn()
    target_groups = GroupsColumn()
    target_people = PeopleColumn()
    to_me = ToMeColumn()
    review_id = ReviewRequestIDColumn()
    status_query_field = b'status'
    site_query_field = b'local_site'

    def __init__(self, *args, **kwargs):
        """Initialize the datagrid."""
        self.local_site = kwargs.pop(b'local_site', None)
        super(ReviewRequestDataGrid, self).__init__(*args, **kwargs)
        self.listview_template = b'datagrids/review_request_listview.html'
        self.profile_sort_field = b'sort_review_request_columns'
        self.profile_columns_field = b'review_request_columns'
        self.show_closed = True
        self.submitter_url_name = b'user'
        self.default_sort = [b'-last_updated']
        self.default_columns = [
         b'star', b'summary', b'submitter', b'time_added', b'last_updated_since']
        user = self.request.user
        if user.is_authenticated():
            profile = user.get_profile()
            self.timezone = pytz.timezone(profile.timezone)
            self.time_added.timezone = self.timezone
            self.last_updated.timezone = self.timezone
            self.diff_updated.timezone = self.timezone
        return

    def load_extra_state(self, profile, allow_hide_closed=True):
        """Load extra state for the datagrid."""
        return super(ReviewRequestDataGrid, self).load_extra_state(profile, allow_hide_closed)

    def post_process_queryset(self, queryset):
        """Add additional data to the queryset."""
        q = queryset.with_counts(self.request.user)
        return super(ReviewRequestDataGrid, self).post_process_queryset(q)

    def link_to_object(self, state, obj, value):
        """Return a link to the given object."""
        if value and isinstance(value, User):
            return local_site_reverse(b'user', request=self.request, args=[
             value])
        return obj.get_absolute_url()


class ReviewDataGrid(ShowClosedReviewRequestsMixin, DataGrid):
    """A datagrid that displays a list of reviews.

    This datagrid accepts the show_closed parameter in the URL, allowing
    submitted review requests to be filtered out or displayed.
    """
    timestamp = DateTimeColumn(label=_(b'Date Reviewed'), format=b'F jS, Y', shrink=True)
    submitter = UsernameColumn(label=_(b'Owner'), user_relation=[
     b'review_request', b'submitter'])
    review_summary = ReviewSummaryColumn()
    status_query_field = b'review_request__status'
    site_query_field = b'review_request__local_site'

    def __init__(self, *args, **kwargs):
        """Initialize the datagrid."""
        self.local_site = kwargs.pop(b'local_site', None)
        super(ReviewDataGrid, self).__init__(*args, **kwargs)
        self.listview_template = b'datagrids/review_request_listview.html'
        self.profile_columns_field = b'review_columns'
        self.show_closed = True
        self.default_sort = [b'-timestamp']
        self.default_columns = [
         b'submitter', b'review_summary', b'timestamp']
        user = self.request.user
        if user.is_authenticated():
            profile = user.get_profile()
            self.timezone = pytz.timezone(profile.timezone)
            self.timestamp.timezone = self.timezone
        return


class DashboardDataGrid(DataGridSidebarMixin, ReviewRequestDataGrid):
    """Displays the dashboard.

    The dashboard is the main place where users see what review requests
    are out there that may need their attention.
    """
    new_updates = NewUpdatesColumn()
    my_comments = MyCommentsColumn()
    selected = ReviewRequestCheckboxColumn()
    sidebar = Sidebar([
     OutgoingSection,
     IncomingSection], default_view_id=b'incoming')
    js_model_class = b'RB.Dashboard'
    js_view_class = b'RB.DashboardView'
    periodic_reload = True

    def __init__(self, *args, **kwargs):
        """Initialize the datagrid."""
        local_site = kwargs.get(b'local_site', None)
        super(DashboardDataGrid, self).__init__(*args, **kwargs)
        self.listview_template = b'datagrids/hideable_listview.html'
        self.profile_sort_field = b'sort_dashboard_columns'
        self.profile_columns_field = b'dashboard_columns'
        self.default_view = b'incoming'
        self.show_closed = False
        self.show_archived = False
        self.default_sort = [b'-last_updated']
        self.default_columns = [
         b'selected', b'new_updates', b'ship_it', b'my_comments', b'summary',
         b'submitter', b'last_updated_since']
        self.extra_js_model_data = {b'show_archived': self.show_archived}
        self.local_site = local_site
        self.user = self.request.user
        self.profile = self.user.get_profile()
        self.site_profile = self.user.get_site_profile(local_site)
        return

    def load_extra_state(self, profile):
        """Load extra state for the datagrid."""
        group_name = self.request.GET.get(b'group', b'')
        view = self.request.GET.get(b'view', self.default_view)
        user = self.request.user
        if view == b'outgoing':
            self.queryset = ReviewRequest.objects.from_user(user, user, local_site=self.local_site)
            self.title = _(b'All Outgoing Review Requests')
        else:
            if view == b'mine':
                self.queryset = ReviewRequest.objects.from_user(user, user, None, local_site=self.local_site)
                self.title = _(b'All My Review Requests')
            elif view == b'to-me':
                self.queryset = ReviewRequest.objects.to_user_directly(user, user, local_site=self.local_site)
                self.title = _(b'Incoming Review Requests to Me')
            elif view in ('to-group', 'to-watched-group'):
                if group_name:
                    try:
                        group = Group.objects.get(name=group_name, local_site=self.local_site)
                        if not group.is_accessible_by(user):
                            raise Http404
                    except Group.DoesNotExist:
                        raise Http404

                    self.queryset = ReviewRequest.objects.to_group(group_name, self.local_site, user)
                    self.title = _(b'Incoming Review Requests to %s') % group_name
                else:
                    self.queryset = ReviewRequest.objects.to_user_groups(user, user, local_site=self.local_site)
                    self.title = _(b'All Incoming Review Requests to My Groups')
            elif view == b'starred':
                self.queryset = self.profile.starred_review_requests.public(user=user, local_site=self.local_site, status=None)
                self.title = _(b'Starred Review Requests')
            elif view == b'incoming':
                self.queryset = ReviewRequest.objects.to_user(user, user, local_site=self.local_site)
                self.title = _(b'All Incoming Review Requests')
            else:
                raise Http404
            if profile and b'show_archived' in profile.extra_data:
                self.show_archived = profile.extra_data[b'show_archived']
            try:
                show = self.request.GET.get(b'show-archived', self.show_archived)
                self.show_archived = int(show) != 0
            except ValueError:
                pass

        if not self.show_archived:
            hidden_q = ReviewRequestVisit.objects.filter(user=user).exclude(visibility=ReviewRequestVisit.VISIBLE)
            hidden_q = hidden_q.values_list(b'review_request_id', flat=True)
            self.queryset = self.queryset.exclude(pk__in=hidden_q)
        if profile and self.show_archived != profile.extra_data.get(b'show_archived'):
            profile.extra_data[b'show_archived'] = self.show_archived
            profile_changed = True
        else:
            profile_changed = False
        self.extra_js_model_data[b'show_archived'] = self.show_archived
        parent_profile_changed = super(DashboardDataGrid, self).load_extra_state(profile, allow_hide_closed=False)
        return profile_changed or parent_profile_changed


class UsersDataGrid(AlphanumericDataGrid):
    """A datagrid showing a list of users registered on Review Board."""
    username = UsernameColumn(label=_(b'Username'))
    fullname = FullNameColumn(label=_(b'Full Name'), link=True, expand=True)
    pending_count = PendingCountColumn(_(b'Open Review Requests'), field_name=b'directed_review_requests', shrink=True)

    def __init__(self, request, queryset=User.objects.all(), title=_(b'All users'), local_site=None):
        """Initialize the datagrid."""
        if local_site:
            qs = queryset.filter(local_site=local_site)
        else:
            qs = queryset
        super(UsersDataGrid, self).__init__(request, qs, title=title, sortable_column=b'username', extra_regex=b'^[0-9_\\-\\.].*')
        self.listview_template = b'datagrids/user_listview.html'
        self.default_sort = [b'username']
        self.profile_sort_field = b'sort_submitter_columns'
        self.profile_columns_field = b'submitter_columns'
        self.default_columns = [
         b'username', b'fullname', b'pending_count']
        self.show_inactive = False

    def link_to_object(self, state, obj, value):
        """Return a link to the given object."""
        return local_site_reverse(b'user', request=self.request, args=[
         obj.username])

    def load_extra_state(self, profile):
        """Load extra state for the datagrid.

        This handles hiding or showing inactive users.

        Args:
            profile (reviewboard.accounts.models.Profile):
                The user profile which contains some basic
                configurable settings.

        Returns:
            bool:
            Always returns False.
        """
        show_inactive = self.request.GET.get(b'show-inactive', 0)
        try:
            self.show_inactive = int(show_inactive)
        except ValueError:
            pass

        if not self.show_inactive:
            self.queryset = self.queryset.filter(is_active=True)
        return False


class GroupDataGrid(DataGrid):
    """A datagrid showing a list of review groups accessible by the user."""
    star = ReviewGroupStarColumn()
    name = Column(_(b'Group ID'), link=True, sortable=True)
    displayname = Column(_(b'Group Name'), field_name=b'display_name', link=True, expand=True)
    pending_count = PendingCountColumn(_(b'Open Review Requests'), field_name=b'review_requests', link=True, shrink=True)
    member_count = GroupMemberCountColumn(_(b'Members'), field_name=b'members', shrink=True)

    def __init__(self, request, title=_(b'All groups'), *args, **kwargs):
        """Initialize the datagrid."""
        local_site = kwargs.pop(b'local_site', None)
        queryset = Group.objects.accessible(request.user, local_site=local_site)
        super(GroupDataGrid, self).__init__(request, queryset=queryset, title=title, *args, **kwargs)
        self.profile_sort_field = b'sort_group_columns'
        self.profile_columns_field = b'group_columns'
        self.default_sort = [b'name']
        self.default_columns = [
         b'star', b'name', b'displayname', b'pending_count']
        return

    @staticmethod
    def link_to_object(state, obj, value):
        """Return a link to the given object."""
        return obj.get_absolute_url()


class UserPageDataGridMixin(DataGridSidebarMixin):
    """An abstract class for data grids on the user page.

    This will display information about the user on the side.
    """
    sidebar = Sidebar([
     UserProfileItem,
     UserGroupsItem])


class UserPageReviewRequestDataGrid(UserPageDataGridMixin, ReviewRequestDataGrid):
    """A data grid for the user page.

    This will show the review requests the user has out for review.
    """
    tab_title = _(b'Review Requests')

    def __init__(self, request, user, *args, **kwargs):
        """Initialize the datagrid."""
        queryset = ReviewRequest.objects.from_user(user.username, user=request.user, status=None, with_counts=True, local_site=kwargs.get(b'local_site'), filter_private=True, show_inactive=True)
        super(UserPageReviewRequestDataGrid, self).__init__(request, queryset=queryset, title=(_(b"%s's Review Requests") % user.username), extra_context={b'pii_safe_title': _(b"User's Review Requests")}, *args, **kwargs)
        self.groups = user.review_groups.accessible(request.user)
        self.user = user
        return


class UserPageReviewsDataGrid(UserPageDataGridMixin, ReviewDataGrid):
    """A data grid for the user page.

    This will show reviews the user has made on other review requests.
    """
    tab_title = _(b'Reviews')

    def __init__(self, request, user, *args, **kwargs):
        """Initialize the datagrid."""
        queryset = Review.objects.from_user(user.username, user=request.user, public=True, filter_private=True, status=None, local_site=kwargs.get(b'local_site'))
        super(UserPageReviewsDataGrid, self).__init__(request, queryset=queryset, title=(_(b"%s's Reviews") % user.username), extra_context={b'pii_safe_title': _(b"User's Reviews")}, *args, **kwargs)
        self.groups = user.review_groups.accessible(request.user)
        self.user = user
        return