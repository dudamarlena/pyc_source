# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/datagrids/columns.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
from django.core.urlresolvers import NoReverseMatch
from django.template.defaultfilters import date
from django.utils import six
from django.utils.html import conditional_escape, escape, format_html, format_html_join
from django.utils.safestring import mark_safe
from django.utils.six.moves import reduce
from django.utils.translation import ugettext_lazy as _, ugettext
from djblets.datagrid.grids import CheckboxColumn, Column, DateTimeColumn
from djblets.siteconfig.models import SiteConfiguration
from reviewboard.accounts.models import Profile, ReviewRequestVisit
from reviewboard.avatars import avatar_services
from reviewboard.reviews.models import ReviewRequest
from reviewboard.reviews.templatetags.reviewtags import render_star
from reviewboard.site.urlresolvers import local_site_reverse

class BaseStarColumn(Column):
    """Indicates if an item is starred.

    This is the base class for all columns that deal with starring items.

    The star is interactive, allowing the user to star or unstar the item.
    """

    def __init__(self, *args, **kwargs):
        """Initialize the column."""
        super(BaseStarColumn, self).__init__(image_class=b'rb-icon rb-icon-star-on', image_alt=_(b'Starred'), detailed_label=_(b'Starred'), shrink=True, *args, **kwargs)

    def setup_state(self, state):
        """Set up the state for this column."""
        state.all_starred = set()

    def render_data(self, state, obj):
        """Return the rendered contents of the column."""
        obj.starred = obj.pk in state.all_starred
        return render_star(state.datagrid.request.user, obj)


class UsernameColumn(Column):
    """A column for showing a username and the user's avatar.

    The username and avatar will link to the user's profile page and will
    show basic profile information when hovering over the link.

    When constructing an instance of this column, the relation between the
    object being represented in the datagrid and the user can be specified
    as a tuple or list of field names forming a path to the user field.
    """
    AVATAR_SIZE = 24

    def __init__(self, label=_(b'Username'), user_relation=[], *args, **kwargs):
        """Initialize the column.

        Args:
            label (unicode, optional):
                The label for the column.

            user_relation (list of unicode, optional):
                A list of fields forming a relation path to the user. This can
                be left blank if representing the user.

            *args (tuple):
                Additional positional arguments to pass to the column.

            **kwargs (dict):
                Additional keyword arguments to pass to the column.
        """
        self._user_relation = user_relation
        super(UsernameColumn, self).__init__(label=label, db_field=(b'__').join(user_relation + [b'username']), css_class=b'submitter-column', shrink=True, sortable=True, link=True, link_func=self._link_user, link_css_class=b'user', *args, **kwargs)

    def get_user(self, obj):
        """Return the user associated with this object.

        Args:
            obj (object):
                The object provided to the column.

        Returns:
            django.contrib.auth.models.User:
            The resulting user.
        """
        user = obj
        for field_name in self._user_relation:
            user = getattr(user, field_name)

        return user

    def render_data(self, state, obj):
        """Render the user's name and avatar as HTML.

        Args:
            state (djblets.datagrid.grids.StatefulColumn):
                The column state.

            obj (django.db.models.Model):
                The object being rendered in the datagrid.

        Returns:
            django.utils.safestring.SafeText:
            The HTML for the column.
        """
        user = self.get_user(obj)
        siteconfig = SiteConfiguration.objects.get_current()
        request = state.datagrid.request
        avatar_html = b''
        if siteconfig.get(avatar_services.AVATARS_ENABLED_KEY):
            avatar_service = avatar_services.for_user(user)
            if avatar_service:
                avatar_html = avatar_service.render(request=request, user=user, size=self.AVATAR_SIZE)
        username = user.username
        return format_html(b'{0}{1}', avatar_html, username)

    def augment_queryset(self, state, queryset):
        """Add additional queries to the queryset.

        This will select fields for the user and the user's profile, to
        help with query performance.

        Args:
            state (djblets.datagrid.grids.StatefulColumn):
                The column state.

            queryset (django.db.models.query.QuerySet):
                The queryset to augment.

        Returns:
            django.db.models.query.QuerySet:
            The resulting queryset.
        """
        user_field = (b'__').join(self._user_relation)
        if user_field:
            fields = [
             user_field, b'%s__profile' % user_field]
        else:
            fields = [
             b'profile']
        return queryset.select_related(*fields)

    def _link_user(self, state, obj, *args):
        """Return the URL to link the user associated with this object.

        Args:
            state (djblets.datagrid.grids.StatefulColumn, unused):
                The column state.

            obj (object):
                The object provided to the column.

            *args (tuple):
                Additional keyword arguments provided to the method.

        Returns:
            unicode:
            The URL for the user.
        """
        return local_site_reverse(b'user', request=state.datagrid.request, kwargs={b'username': self.get_user(obj).username})


class FullNameColumn(Column):
    """Shows the full name of the user when appropriate."""

    def augment_queryset(self, state, queryset):
        """Add additional queries to the queryset.

        This will select fields for the user and the user's profile, to
        help with query performance.

        Args:
            state (djblets.datagrid.grids.StatefulColumn):
                The column state.

            queryset (django.db.models.query.QuerySet):
                The queryset to augment.

        Returns:
            django.db.models.query.QuerySet:
            The resulting queryset.
        """
        return queryset.select_related(b'profile')

    def render_data(self, state, user):
        """Render the full name, or blank if not visible to the user.

        Args:
            state (djblets.datagrid.grids.StatefulColumn):
                The column state.

            user (django.contrib.auth.models.User):
                The user whose full name is to be rendered.

        Returns:
            unicode:
            Either the full name (if visible to the user) or an empty string.
        """
        profile = user.get_profile()
        if user.is_profile_visible(state.datagrid.request.user):
            display_name = profile.get_display_name(state.datagrid.request.user)
        else:
            display_name = b''
        return escape(display_name)


class BugsColumn(Column):
    """Shows the list of bugs specified on a review request.

    The list of bugs will be linked to the bug tracker, if a bug tracker
    was configured for the repository the review request's change is on.
    """

    def __init__(self, *args, **kwargs):
        """Initialize the column."""
        super(BugsColumn, self).__init__(label=_(b'Bugs'), css_class=b'bugs', link=False, shrink=True, sortable=False, *args, **kwargs)

    def augment_queryset(self, state, queryset):
        """Add additional queries to the queryset."""
        return queryset.select_related(b'repository')

    def render_data(self, state, review_request):
        """Return the rendered contents of the column."""
        bugs = review_request.get_bug_list()
        repository = review_request.repository
        local_site_name = None
        if review_request.local_site:
            local_site_name = review_request.local_site.name
        if repository and repository.bug_tracker:
            links = []
            for bug in bugs:
                try:
                    url = local_site_reverse(b'bug_url', local_site_name=local_site_name, args=[
                     review_request.display_id, bug])
                    links.append(format_html(b'<a class="bug" href="{0}">{1}</a>', url, bug))
                except NoReverseMatch:
                    links.append(escape(bug))

            return (b', ').join(links)
        else:
            return format_html_join(b', ', b'<span class="bug">{0}</span>', ((bug,) for bug in bugs))


class ReviewRequestCheckboxColumn(CheckboxColumn):
    """A column containing a check-box."""

    def render_data(self, state, obj):
        """Return the rendered contents of the column."""
        if self.is_selectable(state, obj):
            checked = b''
            if self.is_selected(state, obj):
                checked = b'checked="true"'
            return b'<input type="checkbox" data-object-id="%s" data-checkbox-name="%s" %s />' % (
             obj.display_id, escape(self.checkbox_name), checked)
        else:
            return b''


class DateTimeSinceColumn(DateTimeColumn):
    """Displays how long it has been since a given date/time.

    These columns will dynamically update as the page is shown, so that the
    number of minutes, hours, days, etc. ago is correct.
    """

    def render_data(self, state, obj):
        """Return the rendered contents of the column."""
        return b'<time class="timesince" datetime="%s">%s</time>' % (
         date(getattr(obj, self.field_name), b'c'),
         super(DateTimeSinceColumn, self).render_data(state, obj))


class DiffUpdatedColumn(DateTimeColumn):
    """Shows the date/time that the diff was last updated."""

    def __init__(self, *args, **kwargs):
        """Initialize the column."""
        super(DiffUpdatedColumn, self).__init__(label=_(b'Diff Updated'), db_field=b'diffset_history__last_diff_updated', field_name=b'last_diff_updated', sortable=True, link=False, *args, **kwargs)

    def augment_queryset(self, state, queryset):
        """Add additional queries to the queryset."""
        return queryset.select_related(b'diffset_history')

    def render_data(self, state, obj):
        """Return the rendered contents of the column."""
        if obj.diffset_history.last_diff_updated:
            return super(DiffUpdatedColumn, self).render_data(state, obj.diffset_history)
        else:
            return b''


class DiffUpdatedSinceColumn(DateTimeSinceColumn):
    """Shows the elapsed time since the diff was last updated."""

    def __init__(self, *args, **kwargs):
        """Initialize the column."""
        super(DiffUpdatedSinceColumn, self).__init__(label=_(b'Diff Updated'), db_field=b'diffset_history__last_diff_updated', field_name=b'last_diff_updated', sortable=True, link=False, *args, **kwargs)

    def augment_queryset(self, state, queryset):
        """Add additional queries to the queryset."""
        return queryset.select_related(b'diffset_history')

    def render_data(self, state, obj):
        """Return the rendered contents of the column."""
        if obj.diffset_history.last_diff_updated:
            return super(DiffUpdatedSinceColumn, self).render_data(state, obj.diffset_history)
        else:
            return b''


class GroupMemberCountColumn(Column):
    """Shows the number of users that are part of a review group."""

    def __init__(self, *args, **kwargs):
        """Initialize the column."""
        super(GroupMemberCountColumn, self).__init__(link=True, link_func=self.link_to_object, *args, **kwargs)

    def render_data(self, state, group):
        """Return the rendered contents of the column."""
        return six.text_type(group.users.count())

    def link_to_object(self, state, group, value):
        """Return the link to the object in the column."""
        return local_site_reverse(b'group-members', request=state.datagrid.request, args=[
         group.name])


class GroupsColumn(Column):
    """Shows the list of groups requested to review the review request."""

    def __init__(self, *args, **kwargs):
        """Initialize the column."""
        super(GroupsColumn, self).__init__(label=_(b'Groups'), detailed_label=_(b'Target Groups'), sortable=False, shrink=False, *args, **kwargs)

    def augment_queryset(self, state, queryset):
        """Add additional queries to the queryset."""
        return queryset.prefetch_related(b'target_groups')

    def render_data(self, state, review_request):
        """Return the rendered contents of the column."""
        groups = review_request.target_groups.all()
        return reduce(lambda a, d: a + d.name + b' ', groups, b'')


class MyCommentsColumn(Column):
    """Shows if the current user has reviewed the review request."""

    def __init__(self, *args, **kwargs):
        """Initialize the column."""
        super(MyCommentsColumn, self).__init__(image_class=b'rb-icon rb-icon-datagrid-comment-draft', image_alt=_(b'My Comments'), detailed_label=_(b'My Comments'), shrink=True, *args, **kwargs)

    def augment_queryset(self, state, queryset):
        """Add additional queries to the queryset."""
        user = state.datagrid.request.user
        if user.is_anonymous():
            return queryset
        query_dict = {b'user_id': six.text_type(user.id)}
        return queryset.extra(select={b'mycomments_my_reviews': b'\n                SELECT COUNT(1)\n                  FROM reviews_review\n                  WHERE reviews_review.user_id = %(user_id)s\n                    AND reviews_review.review_request_id =\n                        reviews_reviewrequest.id\n            ' % query_dict, 
           b'mycomments_private_reviews': b'\n                SELECT COUNT(1)\n                  FROM reviews_review\n                  WHERE reviews_review.user_id = %(user_id)s\n                    AND reviews_review.review_request_id =\n                        reviews_reviewrequest.id\n                    AND NOT reviews_review.public\n            ' % query_dict, 
           b'mycomments_shipit_reviews': b'\n                SELECT COUNT(1)\n                  FROM reviews_review\n                  WHERE reviews_review.user_id = %(user_id)s\n                    AND reviews_review.review_request_id =\n                        reviews_reviewrequest.id\n                    AND reviews_review.ship_it\n            ' % query_dict})

    def render_data(self, state, review_request):
        """Return the rendered contents of the column."""
        user = state.datagrid.request.user
        if user.is_anonymous() or review_request.mycomments_my_reviews == 0:
            return b''
        if review_request.mycomments_private_reviews > 0:
            icon_class = b'rb-icon-datagrid-comment-draft'
            image_alt = _(b'Comments drafted')
        elif review_request.mycomments_shipit_reviews > 0:
            icon_class = b'rb-icon-datagrid-comment-shipit'
            image_alt = _(b'Comments published. Ship it!')
        else:
            icon_class = b'rb-icon-datagrid-comment'
            image_alt = _(b'Comments published')
        return b'<div class="rb-icon %s" title="%s"></div>' % (
         icon_class, image_alt)


class NewUpdatesColumn(Column):
    """Indicates if there are new updates on a review request.

    This will show an icon if the review request has had any new updates
    or reviews since the user last saw it.
    """

    def __init__(self, *args, **kwargs):
        """Initialize the column."""
        super(NewUpdatesColumn, self).__init__(image_class=b'rb-icon rb-icon-new-updates', image_alt=_(b'New Updates'), detailed_label=_(b'New Updates'), shrink=True, *args, **kwargs)

    def render_data(self, state, review_request):
        """Return the rendered contents of the column."""
        if hasattr(review_request, b'new_review_count') and review_request.new_review_count > 0:
            return b'<div class="%s" title="%s" />' % (
             self.image_class, self.image_alt)
        return b''


class PendingCountColumn(Column):
    """Shows the pending number of review requests for a user or group.

    This will show the pending number of review requests for the given
    review group or user. It only applies to group or user lists.
    """

    def render_data(self, state, obj):
        """Return the rendered contents of the column."""
        return six.text_type(getattr(obj, self.field_name).filter(public=True, status=b'P').count())


class PeopleColumn(Column):
    """Shows the list of people requested to review the review request."""

    def __init__(self, *args, **kwargs):
        """Initialize the column."""
        super(PeopleColumn, self).__init__(label=_(b'People'), detailed_label=_(b'Target People'), sortable=False, shrink=False, *args, **kwargs)

    def augment_queryset(self, state, queryset):
        """Add additional queries to the queryset."""
        return queryset.prefetch_related(b'target_people')

    def render_data(self, state, review_request):
        """Return the rendered contents of the column."""
        people = review_request.target_people.all()
        return reduce(lambda a, d: a + d.username + b' ', people, b'')


class RepositoryColumn(Column):
    """Shows the name of the repository the review request's change is on."""

    def __init__(self, *args, **kwargs):
        """Initialize the column."""
        super(RepositoryColumn, self).__init__(label=_(b'Repository'), db_field=b'repository__name', shrink=True, sortable=True, link=False, css_class=b'repository-column', *args, **kwargs)

    def augment_queryset(self, state, queryset):
        """Add additional queries to the queryset."""
        return queryset.select_related(b'repository')

    def render_data(self, state, obj):
        """Return the rendered contents of the column."""
        return super(RepositoryColumn, self).render_data(state, obj) or b''


class ReviewCountColumn(Column):
    """Shows the number of published reviews for a review request."""

    def __init__(self, *args, **kwargs):
        """Initialize the column."""
        super(ReviewCountColumn, self).__init__(label=_(b'Reviews'), detailed_label=_(b'Number of Reviews'), shrink=True, link=True, link_func=self.link_to_object, *kwargs, **kwargs)

    def render_data(self, state, review_request):
        """Return the rendered contents of the column."""
        return six.text_type(review_request.publicreviewcount_count)

    def augment_queryset(self, state, queryset):
        """Add additional queries to the queryset."""
        return queryset.extra(select={b'publicreviewcount_count': b'\n                SELECT COUNT(*)\n                  FROM reviews_review\n                  WHERE reviews_review.public\n                    AND reviews_review.base_reply_to_id is NULL\n                    AND reviews_review.review_request_id =\n                        reviews_reviewrequest.id\n            '})

    def link_to_object(self, state, review_request, value):
        """Return the link to the object in the column."""
        return b'%s#last-review' % review_request.get_absolute_url()


class ReviewGroupStarColumn(BaseStarColumn):
    """Indicates if a review group is starred.

    The star is interactive, allowing the user to star or unstar the group.
    """

    def augment_queryset(self, state, queryset):
        """Add additional queries to the queryset."""
        user = state.datagrid.request.user
        if user.is_authenticated():
            state.all_starred = set(user.get_profile().starred_groups.filter(pk__in=state.datagrid.id_list).values_list(b'pk', flat=True))
        return queryset


class ReviewRequestIDColumn(Column):
    """Displays the ID of the review request."""

    def __init__(self, *args, **kwargs):
        """Initialize the column."""
        super(ReviewRequestIDColumn, self).__init__(label=_(b'ID'), detailed_label=_(b'Review Request ID'), shrink=True, link=True, sortable=True, *args, **kwargs)

    def get_sort_field(self, state):
        """Return the model field for sorting this column."""
        if state.datagrid.local_site:
            return b'local_id'
        else:
            return b'id'

    def render_data(self, state, review_request):
        """Return the rendered contents of the column."""
        return review_request.display_id


class ReviewRequestStarColumn(BaseStarColumn):
    """Indicates if a review request is starred.

    The star is interactive, allowing the user to star or unstar the
    review request.
    """

    def augment_queryset(self, state, queryset):
        """Add additional queries to the queryset."""
        user = state.datagrid.request.user
        if user.is_authenticated():
            state.all_starred = set(user.get_profile().starred_review_requests.filter(pk__in=state.datagrid.id_list).values_list(b'pk', flat=True))
        return queryset


class ShipItColumn(Column):
    """Shows the "Ship It" count for a review request."""

    def __init__(self, *args, **kwargs):
        """Initialize the column."""
        super(ShipItColumn, self).__init__(image_class=b'rb-icon rb-icon-datagrid-column-shipits-issues', image_alt=_(b'Ship It!/Issue Counts'), detailed_label=_(b'Ship It!/Issue Counts'), db_field=b'shipit_count', sortable=True, shrink=True, *args, **kwargs)

    def render_data(self, state, review_request):
        """Return the rendered contents of the column.

        Args:
            state (djblets.datagrid.grids.StatefulColumn):
                The state for the datagrid.

            review_request (reviewboard.reviews.models.review_request.
                            ReviewRequest):
                The review request.

        Returns:
            django.utils.safestring.SafeText:
            The rendered HTML for the column.
        """
        open_issues = review_request.issue_open_count
        verifying_issues = review_request.issue_verifying_count
        if open_issues > 0 and verifying_issues > 0:
            return self._render_counts([
             {b'count': open_issues, 
                b'title': _(b'Open issue count')},
             {b'count': verifying_issues, 
                b'css_class': b'issue-verifying-count', 
                b'icon_name': b'issue-verifying', 
                b'title': _(b'Verifying issue count')}])
        else:
            if open_issues > 0:
                return self._render_counts([
                 {b'count': open_issues, 
                    b'title': _(b'Open issue count')}])
            if verifying_issues > 0:
                return self._render_counts([
                 {b'count': verifying_issues, 
                    b'icon_name': b'issue-verifying', 
                    b'title': _(b'Verifying issue count')}])
            if review_request.shipit_count:
                return self._render_counts([
                 {b'count': review_request.shipit_count, 
                    b'css_class': b'shipit-count', 
                    b'icon_name': b'shipit', 
                    b'title': _(b'Ship It! count')}], container_css_class=b'shipit-count-container')
            return b''

    def _render_counts(self, count_details, container_css_class=b'issue-count-container'):
        """Render the counts for the column.

        This will render a container bubble in the column and render each
        provided count and icon in the bubble. This can be used for issues,
        Ship Its, or anything else we need down the road.

        Args:
            count_details (list of dict):
                The list of details for the count. This must have ``count``
                and ``title`` keys, and may optionally have ``css_class`` and
                ``icon_name`` keys.

            container_css_class (unicode, optional):
                The optional CSS class name for the outer container.

        Returns:
            django.utils.safestring.SafeText:
            The resulting HTML for the counts bubble.
        """
        return format_html(b'<div class="{container_css_class}">{count_html}</div>', container_css_class=container_css_class, count_html=mark_safe((b'').join(format_html(b'<span class="{css_class}"><span class="rb-icon rb-icon-datagrid-{icon_name}"      title="{title}"></span>{count}</span>', **dict({b'css_class': b'issue-count', b'icon_name': b'open-issues'}, **count_detail)) for count_detail in count_details)))


class SummaryColumn(Column):
    """Shows the summary of a review request.

    This will also prepend the draft/submitted/discarded state, if any,
    to the summary.
    """

    def __init__(self, *args, **kwargs):
        """Initialize the column."""
        super(SummaryColumn, self).__init__(label=_(b'Summary'), expand=True, link=True, link_css_class=b'review-request-link', css_class=b'summary', sortable=True, *args, **kwargs)

    def augment_queryset(self, state, queryset):
        """Add additional queries to the queryset."""
        user = state.datagrid.request.user
        if user.is_anonymous():
            return queryset
        return queryset.extra(select={b'draft_summary': b'\n                SELECT reviews_reviewrequestdraft.summary\n                  FROM reviews_reviewrequestdraft\n                  WHERE reviews_reviewrequestdraft.review_request_id =\n                        reviews_reviewrequest.id\n            ', 
           b'visibility': b'\n                SELECT accounts_reviewrequestvisit.visibility\n                  FROM accounts_reviewrequestvisit\n                 WHERE accounts_reviewrequestvisit.review_request_id =\n                       reviews_reviewrequest.id\n                   AND accounts_reviewrequestvisit.user_id = %(user_id)s\n            ' % {b'user_id': six.text_type(user.id)}})

    def render_data(self, state, review_request):
        """Return the rendered contents of the column.

        Args:
            state (djblets.datagrids.grids.StatefulColumn):
                The state for the datagrid.

            review_request (reviewboard.reviews.models.review_request.ReviewRequest):
                The review request.

        Returns:
            django.utils.safestring.SafeText:
            The rendered column.
        """
        summary = review_request.summary
        labels = []
        if review_request.submitter_id == state.datagrid.request.user.id:
            if review_request.draft_summary is not None:
                summary = review_request.draft_summary
                labels.append((b'label-draft', _(b'Draft')))
            elif not review_request.public and review_request.status == ReviewRequest.PENDING_REVIEW:
                labels.append((b'label-draft', _(b'Draft')))
        if state.datagrid.request.user.is_authenticated():
            if review_request.visibility == ReviewRequestVisit.ARCHIVED:
                labels.append((b'label-archived', _(b'Archived')))
            elif review_request.visibility == ReviewRequestVisit.MUTED:
                labels.append((b'label-muted', _(b'Muted')))
        if review_request.status == ReviewRequest.SUBMITTED:
            labels.append((b'label-submitted', _(b'Submitted')))
        elif review_request.status == ReviewRequest.DISCARDED:
            labels.append((b'label-discarded', _(b'Discarded')))
        result = [
         format_html_join(b'', b'<label class="{0}">{1}</label>', labels)]
        if summary:
            result.append(format_html(b'<span>{0}</span>', summary))
        else:
            result.append(format_html(b'<span class="no-summary">{0}</span>', _(b'No Summary')))
        return mark_safe((b'').join(result))


class ReviewSummaryColumn(SummaryColumn):
    """Shows the summary of the review request of a review.

    This does not (yet) prepend the draft/submitted/discarded state, if any,
    to the summary.
    """

    def __init__(self, *args, **kwargs):
        """Initialize the column."""
        super(SummaryColumn, self).__init__(label=_(b'Review Request Summary'), expand=True, link=True, css_class=b'summary', *args, **kwargs)

    def render_data(self, state, review):
        """Return the rendered contents of the column."""
        return conditional_escape(review.review_request.summary)

    def augment_queryset(self, state, queryset):
        """Add additional queries to the queryset."""
        return queryset.select_related(b'review_request')


class ToMeColumn(Column):
    """Indicates if the user is requested to review the change.

    This will show an indicator if the user is on the Target People reviewers
    list.
    """

    def __init__(self, *args, **kwargs):
        """Initialize the column."""
        raquo = b'»'
        super(ToMeColumn, self).__init__(label=raquo, detailed_label=_(b'To Me'), detailed_label_html=(ugettext(b'%s To Me') % raquo), shrink=True, *args, **kwargs)

    def augment_queryset(self, state, queryset):
        """Add additional queries to the queryset."""
        user = state.datagrid.request.user
        if user.is_authenticated():
            state.all_to_me = set(user.directed_review_requests.filter(pk__in=state.datagrid.id_list).values_list(b'pk', flat=True))
        else:
            state.all_to_me = set()
        return queryset

    def render_data(self, state, review_request):
        """Return the rendered contents of the column."""
        if review_request.pk in state.all_to_me:
            return b'<div title="%s"><b>&raquo;</b></div>' % self.detailed_label
        return b''


class DiffSizeColumn(Column):
    """Indicates line add/delete counts for the latest diffset."""

    def __init__(self, *args, **kwargs):
        """Initialize the column."""
        super(DiffSizeColumn, self).__init__(label=_(b'Diff Size'), sortable=False, shrink=True, *args, **kwargs)

    def render_data(self, state, review_request):
        """Return the rendered contents of the column."""
        if review_request.repository_id is None:
            return b''
        else:
            diffsets = list(review_request.diffset_history.diffsets.all())
            if not diffsets:
                return b''
            diffset = diffsets[(-1)]
            counts = diffset.get_total_line_counts()
            insert_count = counts.get(b'raw_insert_count')
            delete_count = counts.get(b'raw_delete_count')
            result = []
            if insert_count:
                result.append(b'<span class="diff-size-column insert">+%d</span>' % insert_count)
            if delete_count:
                result.append(b'<span class="diff-size-column delete">-%d</span>' % delete_count)
            if result:
                return (b'&nbsp;').join(result)
            return b''

    def augment_queryset(self, state, queryset):
        """Add additional queries to the queryset.

        This will prefetch the diffsets and filediffs needed to perform the
        line calculations.

        Args:
            state (djblets.datagrid.grids.StatefulColumn):
                The column state.

            queryset (django.db.models.query.QuerySet):
                The queryset to augment.

        Returns:
            django.db.models.query.QuerySet:
            The resulting queryset.
        """
        return queryset.prefetch_related(b'diffset_history__diffsets', b'diffset_history__diffsets__files')