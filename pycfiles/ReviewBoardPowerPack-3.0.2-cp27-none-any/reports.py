# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /rbpowerpack/reports/reports.py
# Compiled at: 2019-06-17 15:11:31
from __future__ import division, unicode_literals
import csv, itertools, json, logging
from collections import OrderedDict, defaultdict
from io import BytesIO
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render
from django.utils import six
from django.utils.html import format_html
from django.utils.translation import ugettext as _
from djblets.gravatars import get_gravatar_url_for_email
from djblets.siteconfig.models import SiteConfiguration
from reviewboard.admin.server import build_server_url
from reviewboard.changedescs.models import ChangeDescription
from reviewboard.reviews.models import BaseComment, Comment, FileAttachmentComment, ReviewRequest, Review, ScreenshotComment
from reviewboard.site.urlresolvers import local_site_reverse
from rbpowerpack.reports.forms import BasicReportForm
from rbpowerpack.reports.queries import UserQuery, get_reviewbot_user_id
_populated = False
_registered_report_classes = OrderedDict()

class Report(object):
    """An abstract report.

    This should be subclassed to introduce new reports.
    """
    id = b''
    summary = b''
    description = b''
    long_description_html = b''
    thumbnail_image = b''
    js_model_class = b''
    js_view_class = b''
    form = BasicReportForm
    template_name = b'powerpack/reports/basic_report.html'

    def __init__(self):
        """Initialize the report."""
        self.reviewbot_user_id = get_reviewbot_user_id()

    def get_data(self, extension, request, get_params, local_site):
        """Return data for the report.

        This should be implemented by subclasses to return specific data for
        the report.

        Args:
            extension (rbpowerpack.extension.PowerPackExtension):
                The Power pack extension.

            request (django.http.HttpRequest):
                The HTTP request.

            get_params (dict):
                The GET parameters. This may be the same as ``request.GET``,
                but may have been pre-processed.

            local_site (reviewboard.site.models.LocalSite):
                The local site, if appropriate.

        Returns:
            Any JSON-serializable type:
            Data for the report.

        Raises:
            ValueError:
                The parameters in the request could not be parsed.
        """
        raise NotImplementedError

    def render(self, extension, request, local_site, extra_context={}):
        """Render this report.

        By default, this uses :py:attr`template`, :py:attr`js_model_class`, and
        :py:attr`js_view_class` to handle most reports. Reports that need very
        custom behavior can override any of those or even this method.

        Returns:
            django.utils.safestring.SafeText:
            The rendered report HTML.
        """
        siteconfig = SiteConfiguration.objects.get_current()
        use_gravatars = siteconfig.get(b'integration_gravatars', True)
        context = {b'use_gravatars': use_gravatars, 
           b'report': self, 
           b'extension': extension, 
           b'js_model_class': self.js_model_class, 
           b'js_view_class': self.js_view_class}
        context.update(extra_context)
        return render(request, self.template_name, context)

    def _timedelta_span(self, earlier, later):
        """Return the difference between two datetimes in days.

        Returns:
            float:
                The number of days between the two datetimes.
        """
        td = later - earlier
        ms = td.microseconds + (td.seconds + td.days * 24 * 3600) * 1000000
        return ms / 1000000 / 86400

    def _serialize_user(self, request, user):
        """Return a serialized user object for inclusion in report data.

        Several reports include user data in the output. This method serializes
        the important data from a user object.

        Args:
            request (django.http.HttpRequest):
                The request object.

            user (django.contrib.auth.models.User):
                The user to serialize.

        Returns:
            dict:
            Data suitable for serializing to JSON.
        """

        def _pretty_user_name(user):
            return (b'%(first_name)s %(last_name)s' % user).strip() or user[b'username']

        return {b'name': _pretty_user_name(user), 
           b'avatar': format_html(b'<img src="{0}" width="{1}" height="{1}" class="gravatar">', get_gravatar_url_for_email(request, user[b'email'].strip().lower(), 24), 24), 
           b'username': user[b'username'], 
           b'email': user[b'email']}


class TimeToFeedback(Report):
    id = b'time-to-feedback'
    summary = _(b'Time To First Feedback')
    description = _(b'Time elapsed between posting a review request and initial feedback.')
    long_description_html = _(b'<p> This report shows a cumulative graph of the amount of time elapsed between when a review request is first published and when the first code review for that change is published. This can be used to determine about how long users have to wait before they get feedback on a code change.</p><p> The two dashed boxes show two different metrics of particular interest: the percentage of review requests which get an initial code review in less than one day, and the median time users have to wait (meaning that 50% of review requests get a code review within that time or less).</p>')
    thumbnail_image = b'images/report-thumbnails/time-to-first-feedback.png'
    js_model_class = b'PowerPack.Reports.TimeTo'
    js_view_class = b'PowerPack.Reports.TimeToView'

    def get_data(self, extension, request, get_params, local_site):
        """Return data for the report.

        This report uses a list of "durations" which represent the time span
        (in days) between when a review request is first posted and when the
        first non-automated (non-ReviewBot) review is posted.

        Args:
            extension (rbpowerpack.extension.PowerPackExtension):
                The Power pack extension.

            request (django.http.HttpRequest):
                The HTTP request.

            get_params (dict):
                The GET parameters. This may be the same as ``request.GET``,
                but may have been pre-processed.

            local_site (reviewboard.site.models.LocalSite):
                The local site, if appropriate.

        Returns:
            list of float:
            Data for the report.

        Raises:
            ValueError:
                The parameters in the request could not be parsed.
        """
        data = self._get_data_int(request, get_params, local_site)
        return [ item[b'time_span'] for item in data if b'time_span' in item
               ]

    def get_csv(self, extension, request, get_params, local_site):
        """Return the data for the report in CSV.

        Args:
            extension (rbpowerpack.extension.PowerPackExtension):
                The Power Pack extension.

            request (django.http.HttpRequest):
                The HTTP request.

            get_params (dict):
                The GET parameters. This may be the same as ``request.GET``,
                but may have been pre-processed.

            local_site (reviewboard.site.models.LocalSite):
                The local site, if appropriate.

        Returns:
            bytes:
            The data encoded as a UTF-8 CSV file.
        """
        output = BytesIO()
        writer = csv.DictWriter(output, fieldnames=[
         b'id',
         b'url',
         b'time_added',
         b'time_commented',
         b'time_span'])
        writer.writeheader()
        data = self._get_data_int(request, get_params, local_site)
        for item in data:
            review_request_id = item[b'local_id'] or item[b'pk']
            row = {b'id': review_request_id, 
               b'url': build_server_url(local_site_reverse(b'review-request-detail', local_site=local_site, kwargs={b'review_request_id': review_request_id})), 
               b'time_added': item[b'time_added'].isoformat()}
            if b'time_commented' in item:
                row[b'time_commented'] = item[b'time_commented'].isoformat()
                row[b'time_span'] = item[b'time_span']
            writer.writerow(row)

        return output.getvalue()

    def _get_data_int(self, request, get_params, local_site):
        """Do queries and return data.

        This is an internal helper that is shared between :py:meth:`get_data`
        and :py:meth:`get_csv`.

        Args:
            request (django.http.HttpRequest):
                The HTTP request.

            get_params (dict):
                The GET parameters. This may be the same as ``request.GET``,
                but may have been pre-processed.

            local_site (reviewboard.site.models.LocalSite):
                The local site, if appropriate.

        Returns:
            list of dict:
            The queried data.
        """
        form = self.form(get_params)
        if not form.is_valid():
            raise ValueError(b'Invalid report parameters.')
        review_requests = ReviewRequest.objects.public(status=None, user=request.user, local_site=local_site).filter(time_added__gte=form.cleaned_data[b'start'], time_added__lte=form.cleaned_data[b'end'])
        if not form.cleaned_data[b'everyone']:
            users = list(UserQuery(local_site=local_site, usernames=form.cleaned_data[b'users'], group_names=form.cleaned_data[b'groups']).get_objects().values_list(b'pk', flat=True))
            review_requests = review_requests.filter(submitter__in=users)
        review_requests = list(review_requests.values(b'pk', b'local_id', b'time_added'))
        review_requests_by_pk = dict((review_request[b'pk'], review_request) for review_request in review_requests)
        reviews = Review.objects.filter(review_request__in=six.iterkeys(review_requests_by_pk), public=True).order_by(b'timestamp').values(b'pk', b'user_id', b'timestamp', b'review_request_id')
        for review in reviews:
            review_request_pk = review[b'review_request_id']
            review_request = review_requests_by_pk[review_request_pk]
            if review[b'user_id'] != self.reviewbot_user_id and b'time_commented' not in review_request:
                review_request[b'time_commented'] = review[b'timestamp']

        for review_request in review_requests:
            if b'time_commented' in review_request:
                review_request[b'time_span'] = self._timedelta_span(review_request[b'time_added'], review_request[b'time_commented'])

        return review_requests


class TimeToClose(Report):
    id = b'time-to-close'
    summary = _(b'Time To Close')
    description = _(b'Time elapsed between posting a review request and code review process completion.')
    long_description_html = _(b'<p> This report shows a cumulative graph of the amount of time elapsed between when a review request is first published and when it is marked as closed. This can be used to determine about how long the entire code review process takes in order to approve a code change.</p><p> The two dashed boxes show two different metrics of particular interest: the percentage of review requests which are closed in less than one day, and the median time it takes for a code change to go through the code review process (meaning that 50% of review requests are closed within that time or less).</p>')
    thumbnail_image = b'images/report-thumbnails/time-to-close.png'
    js_model_class = b'PowerPack.Reports.TimeTo'
    js_view_class = b'PowerPack.Reports.TimeToView'

    def get_data(self, extension, request, get_params, local_site):
        """Return data for the report.

        This report uses a list of "durations" which represent the time span
        (in days) between when a review request is first posted and when it is
        closed.

        Args:
            extension (rbpowerpack.extension.PowerPackExtension):
                The Power pack extension.

            request (django.http.HttpRequest):
                The HTTP request.

            get_params (dict):
                The GET parameters. This may be the same as ``request.GET``,
                but may have been pre-processed.

            local_site (reviewboard.site.models.LocalSite):
                The local site, if appropriate.

        Returns:
            list of float:
            Data for the report.

        Raises:
            ValueError:
                The parameters in the request could not be parsed.
        """
        data = self._get_data_int(request, get_params, local_site)
        return [ item[b'time_span'] for item in data if b'time_span' in item
               ]

    def get_csv(self, extension, request, get_params, local_site):
        """Return the data for the report in CSV.

        Args:
            extension (rbpowerpack.extension.PowerPackExtension):
                The Power Pack extension.

            request (django.http.HttpRequest):
                The HTTP request.

            get_params (dict):
                The GET parameters. This may be the same as ``request.GET``,
                but may have been pre-processed.

            local_site (reviewboard.site.models.LocalSite):
                The local site, if appropriate.

        Returns:
            bytes:
            The data encoded as a UTF-8 CSV file.
        """
        output = BytesIO()
        writer = csv.DictWriter(output, fieldnames=[
         b'id',
         b'url',
         b'time_added',
         b'time_closed',
         b'time_span'])
        writer.writeheader()
        data = self._get_data_int(request, get_params, local_site)
        for item in data:
            review_request_id = item[b'local_id'] or item[b'pk']
            row = {b'id': review_request_id, 
               b'url': build_server_url(local_site_reverse(b'review-request-detail', local_site=local_site, kwargs={b'review_request_id': review_request_id})), 
               b'time_added': item[b'time_added'].isoformat()}
            if b'time_closed' in item:
                row[b'time_closed'] = item[b'time_closed'].isoformat()
                row[b'time_span'] = item[b'time_span']
            writer.writerow(row)

        return output.getvalue()

    def _get_data_int(self, request, get_params, local_site):
        """Do queries and return data.

        This is an internal helper that is shared between :py:meth:`get_data`
        and :py:meth:`get_csv`.

        Args:
            request (django.http.HttpRequest):
                The HTTP request.

            get_params (dict):
                The GET parameters. This may be the same as ``request.GET``,
                but may have been pre-processed.

            local_site (reviewboard.site.models.LocalSite):
                The local site, if appropriate.

        Returns:
            list of dict:
            The queried data.
        """
        form = self.form(get_params)
        if not form.is_valid():
            raise ValueError(b'Invalid report parameters.')
        review_requests = ReviewRequest.objects.public(status=None, user=request.user, local_site=local_site).filter(status__in=[
         ReviewRequest.SUBMITTED,
         ReviewRequest.DISCARDED], time_added__gte=form.cleaned_data[b'start'], time_added__lte=form.cleaned_data[b'end'])
        if not form.cleaned_data[b'everyone']:
            users = list(UserQuery(local_site=local_site, usernames=form.cleaned_data[b'users'], group_names=form.cleaned_data[b'groups']).get_objects().values_list(b'pk', flat=True))
            review_requests = review_requests.filter(submitter__in=users)
        review_requests = list(review_requests.values(b'pk', b'local_id', b'time_added'))
        review_requests_by_pk = dict((review_request[b'pk'], review_request) for review_request in review_requests)
        changedescs = ChangeDescription.objects.filter(public=True, review_request__in=six.iterkeys(review_requests_by_pk)).values(b'pk', b'review_request__id', b'fields_changed', b'timestamp')
        for changedesc in changedescs:
            fields_changed = json.loads(changedesc[b'fields_changed'])
            review_request = review_requests_by_pk[changedesc[b'review_request__id']]
            if b'status' in fields_changed:
                old_status = fields_changed[b'status'][b'old'][0]
                new_status = fields_changed[b'status'][b'new'][0]
                time_closed = review_request.get(b'time_closed', review_request[b'time_added'])
                if old_status == ReviewRequest.PENDING_REVIEW and new_status in (ReviewRequest.SUBMITTED,
                 ReviewRequest.DISCARDED) and changedesc[b'timestamp'] > time_closed:
                    review_request[b'time_closed'] = changedesc[b'timestamp']

        for review_request in review_requests:
            if b'time_closed' in review_request:
                review_request[b'time_span'] = self._timedelta_span(review_request[b'time_added'], review_request[b'time_closed'])

        return review_requests


class ReviewRequestStats(Report):
    id = b'review-request-stats'
    summary = _(b'Review Request Statistics')
    description = _(b'Counts and information about review requests by user.')
    long_description_html = _(b'<p> This report shows a table of users along with some aggregate metrics on the review requests that they\'ve posted. The different columns are:</p><dl> <dt>Review Requests</dt> <dd>  The number of review requests posted by the user in the given  time-frame. </dd> <dt>Issues/Review Request</dt> <dd>  The average number of issues reported against each review  request posted by the user. </dd> <dt>% of Issues Dropped</dt> <dd>  The percentage of issues opened against review requests posted  by the user which are closed as "Dropped" instead of "Fixed". </dd></dl>')
    thumbnail_image = b'images/report-thumbnails/review-request-statistics.png'
    js_model_class = b'PowerPack.Reports.ReviewRequestStats'
    js_view_class = b'PowerPack.Reports.TableView'

    def get_data(self, extension, request, get_params, local_site):
        """Return data for the report.

        This report uses a list of entries corresponding to the rows of the
        table. Each entry includes user data (as returned by
        :py:meth:`_serialize_user`), as well as these fields:
        ``num_review_requests``, ``num_issues``, and ``num_dropped_issues``.

        Args:
            extension (rbpowerpack.extension.PowerPackExtension):
                The Power pack extension.

            request (django.http.HttpRequest):
                The HTTP request.

            get_params (dict):
                The GET parameters. This may be the same as ``request.GET``,
                but may have been pre-processed.

            local_site (reviewboard.site.models.LocalSite):
                The local site, if appropriate.

        Returns:
            list of dict:
            Data for the report.

        Raises:
            ValueError:
                The parameters in the request could not be parsed.
        """
        data = self._get_data_int(request, get_params, local_site)
        return list(six.itervalues(data))

    def get_csv(self, extension, request, get_params, local_site):
        """Return the data for the report in CSV.

        Args:
            extension (rbpowerpack.extension.PowerPackExtension):
                The Power Pack extension.

            request (django.http.HttpRequest):
                The HTTP request.

            get_params (dict):
                The GET parameters. This may be the same as ``request.GET``,
                but may have been pre-processed.

            local_site (reviewboard.site.models.LocalSite):
                The local site, if appropriate.

        Returns:
            bytes:
            The data encoded as a UTF-8 CSV file.
        """
        output = BytesIO()
        writer = csv.DictWriter(output, fieldnames=[
         b'username',
         b'realname',
         b'email',
         b'num_review_requests',
         b'num_issues',
         b'num_dropped_issues'])
        writer.writeheader()
        data = self._get_data_int(request, get_params, local_site)
        for item in six.itervalues(data):
            writer.writerow({b'username': item[b'username'].encode(b'utf-8'), 
               b'realname': item[b'name'].encode(b'utf-8'), 
               b'email': item[b'email'].encode(b'utf-8'), 
               b'num_review_requests': item[b'num_review_requests'], 
               b'num_issues': item[b'num_issues'], 
               b'num_dropped_issues': item[b'num_dropped_issues']})

        return output.getvalue()

    def _get_data_int(self, request, get_params, local_site):
        """Do queries and return data.

        This is an internal helper that is shared between :py:meth:`get_data`
        and :py:meth:`get_csv`.

        Args:
            request (django.http.HttpRequest):
                The HTTP request.

            get_params (dict):
                The GET parameters. This may be the same as ``request.GET``,
                but may have been pre-processed.

            local_site (reviewboard.site.models.LocalSite):
                The local site, if appropriate.

        Returns:
            dict:
            The queried data.
        """
        form = self.form(get_params)
        if not form.is_valid():
            raise ValueError(b'Invalid report parameters.')
        review_requests = ReviewRequest.objects.public(status=None, user=request.user, local_site=local_site).filter(time_added__gte=form.cleaned_data[b'start'], time_added__lte=form.cleaned_data[b'end'])
        everyone = form.cleaned_data[b'everyone']
        users_to_query = set()
        if everyone:
            users_by_pk = {}
            users_already_queried = set()
        else:
            users = list(UserQuery(local_site=local_site, usernames=form.cleaned_data[b'users'], group_names=form.cleaned_data[b'groups']).get_objects().values(b'pk', b'username', b'first_name', b'last_name', b'email'))
            users_by_pk = dict((user[b'pk'], user) for user in users)
            users_already_queried = set(six.iterkeys(users_by_pk))
            review_requests = review_requests.filter(submitter__in=users_already_queried)
        review_requests = list(review_requests.values(b'pk', b'submitter_id', b'time_added'))
        review_requests_by_pk = dict((review_request[b'pk'], review_request) for review_request in review_requests)
        reviews = list(Review.objects.filter(review_request__in=six.iterkeys(review_requests_by_pk), public=True).values(b'pk', b'review_request_id'))
        reviews_by_review_request = defaultdict(list)
        reviews_by_pk = {}
        for review in reviews:
            review_request_pk = review[b'review_request_id']
            reviews_by_review_request[review_request_pk].append(review)
            reviews_by_pk[review[b'pk']] = review

        comment_fields = [b'pk', b'review__id', b'issue_opened',
         b'issue_status']
        comments = list(itertools.chain(Comment.objects.filter(review__in=six.iterkeys(reviews_by_pk)).values(*comment_fields), FileAttachmentComment.objects.filter(review__in=six.iterkeys(reviews_by_pk)).values(*comment_fields), ScreenshotComment.objects.filter(review__in=six.iterkeys(reviews_by_pk)).values(*comment_fields)))
        comments_by_review_request = defaultdict(list)
        for comment in comments:
            review = reviews_by_pk[comment[b'review__id']]
            review_request_pk = review[b'review_request_id']
            review_request = review_requests_by_pk[review_request_pk]
            comments_by_review_request[review_request_pk].append(comment)

        data = {}
        for review_request in review_requests:
            user_id = review_request[b'submitter_id']
            if user_id == self.reviewbot_user_id:
                continue
            if user_id not in data:
                if user_id in users_by_pk:
                    user = users_by_pk[user_id]
                    data[user_id] = self._serialize_user(request, user)
                else:
                    assert everyone
                    data[user_id] = {}
                    users_to_query.add(user_id)
                data[user_id].update({b'num_review_requests': 1, 
                   b'num_issues': 0, 
                   b'num_dropped_issues': 0})
            else:
                data[user_id][b'num_review_requests'] += 1
            comments = comments_by_review_request[review_request[b'pk']]
            for comment in comments:
                if comment[b'issue_opened']:
                    data[user_id][b'num_issues'] += 1
                if comment[b'issue_status'] == BaseComment.DROPPED:
                    data[user_id][b'num_dropped_issues'] += 1

        users = list(User.objects.filter(pk__in=users_to_query - users_already_queried).values(b'pk', b'username', b'first_name', b'last_name', b'email'))
        for user in users:
            data[user[b'pk']].update(self._serialize_user(request, user))

        return data


class ReviewStats(Report):
    id = b'review-stats'
    summary = _(b'Code Review Statistics')
    description = _(b'Counts and information about code reviews by user.')
    long_description_html = _(b'<p> This report shows a table of users along with some aggregate metrics on the code reviews that they\'ve done for other users. The different columns are:</p><dl> <dt>Code Reviews</dt> <dd>  The number of code reviews done by the user in the given  time-frame. </dd> <dt>Ship It!</dt> <dd>  The percentage of code reviews done by the user which give a  Ship It! </dd> <dt>Issues/Code Review</dt> <dd>  The average number of issues reported in each code review  done by the user. </dd> <dt>% of Issues Dropped</dt> <dd>  The percentage of issues opened by the user which are closed  as "Dropped" instead of "Fixed". </dd></dl>')
    thumbnail_image = b'images/report-thumbnails/code-review-statistics.png'
    js_model_class = b'PowerPack.Reports.ReviewStats'
    js_view_class = b'PowerPack.Reports.TableView'

    def get_data(self, extension, request, get_params, local_site):
        """Return data for the report.

        This report uses a list of entries corresponding to the rows of the
        table. Each entry includes user data (as returned by
        :py:meth:`_serialize_user`), as well as these fields: ``num_reviews``,
        ``num_ship_it``, ``num_issues``, and ``num_dropped_issues``.

        Args:
            extension (rbpowerpack.extension.PowerPackExtension):
                The Power pack extension.

            request (django.http.HttpRequest):
                The HTTP request.

            get_params (dict):
                The GET parameters. This may be the same as ``request.GET``,
                but may have been pre-processed.

            local_site (reviewboard.site.models.LocalSite):
                The local site, if appropriate.

        Returns:
            list of dict:
            Data for the report.

        Raises:
            ValueError:
                The parameters in the request could not be parsed.
        """
        data = self._get_data_int(request, get_params, local_site)
        return list(six.itervalues(data))

    def get_csv(self, extension, request, get_params, local_site):
        """Return the data for the report in CSV.

        Args:
            extension (rbpowerpack.extension.PowerPackExtension):
                The Power Pack extension.

            request (django.http.HttpRequest):
                The HTTP request.

            get_params (dict):
                The GET parameters. This may be the same as ``request.GET``,
                but may have been pre-processed.

            local_site (reviewboard.site.models.LocalSite):
                The local site, if appropriate.

        Returns:
            bytes:
            The data encoded as a UTF-8 CSV file.
        """
        output = BytesIO()
        writer = csv.DictWriter(output, fieldnames=[
         b'username',
         b'realname',
         b'email',
         b'num_reviews',
         b'num_ship_it',
         b'num_issues',
         b'num_dropped_issues'])
        writer.writeheader()
        data = self._get_data_int(request, get_params, local_site)
        for item in six.itervalues(data):
            writer.writerow({b'username': item[b'username'].encode(b'utf-8'), 
               b'realname': item[b'name'].encode(b'utf-8'), 
               b'email': item[b'email'].encode(b'utf-8'), 
               b'num_ship_it': item[b'num_ship_it'], 
               b'num_reviews': item[b'num_reviews'], 
               b'num_issues': item[b'num_issues'], 
               b'num_dropped_issues': item[b'num_dropped_issues']})

        return output.getvalue()

    def _get_data_int(self, request, get_params, local_site):
        """Do queries and return data.

        This is an internal helper that is shared between :py:meth:`get_data`
        and :py:meth:`get_csv`.

        Args:
            request (django.http.HttpRequest):
                The HTTP request.

            get_params (dict):
                The GET parameters. This may be the same as ``request.GET``,
                but may have been pre-processed.

            local_site (reviewboard.site.models.LocalSite):
                The local site, if appropriate.

        Returns:
            dict:
            The queried data.
        """
        form = self.form(get_params)
        if not form.is_valid():
            raise ValueError(b'Invalid report parameters.')
        reviews = Review.objects._query(user=request.user, local_site=local_site, status=None, extra_query=Q(timestamp__gte=form.cleaned_data[b'start'], timestamp__lte=form.cleaned_data[b'end']), filter_private=True)
        everyone = form.cleaned_data[b'everyone']
        users_to_query = set()
        if everyone:
            users_by_pk = {}
            users_already_queried = set()
        else:
            users = list(UserQuery(local_site=local_site, usernames=form.cleaned_data[b'users'], group_names=form.cleaned_data[b'groups']).get_objects().values(b'pk', b'username', b'first_name', b'last_name', b'email'))
            users_by_pk = dict((user[b'pk'], user) for user in users)
            users_already_queried = set(six.iterkeys(users_by_pk))
            reviews = reviews.filter(user__in=users_already_queried)
        reviews = list(reviews.values(b'pk', b'ship_it', b'user_id'))
        ship_it = 0
        for review in reviews:
            if review[b'ship_it']:
                ship_it += 1

        reviews_by_pk = dict((review[b'pk'], review) for review in reviews)
        comment_fields = [
         b'pk', b'review__id', b'issue_opened',
         b'issue_status']
        comments = list(itertools.chain(Comment.objects.filter(review__in=six.iterkeys(reviews_by_pk)).values(*comment_fields), FileAttachmentComment.objects.filter(review__in=six.iterkeys(reviews_by_pk)).values(*comment_fields), ScreenshotComment.objects.filter(review__in=six.iterkeys(reviews_by_pk)).values(*comment_fields)))
        comments_by_review = defaultdict(list)
        for comment in comments:
            comments_by_review[comment[b'review__id']].append(comment)

        data = {}
        for review in reviews:
            user_id = review[b'user_id']
            if user_id == self.reviewbot_user_id:
                continue
            if user_id not in data:
                if user_id in users_by_pk:
                    user = users_by_pk[user_id]
                    data[user_id] = self._serialize_user(request, user)
                else:
                    assert everyone
                    data[user_id] = {}
                    users_to_query.add(user_id)
                data[user_id].update({b'num_reviews': 1, 
                   b'num_ship_it': 0, 
                   b'num_issues': 0, 
                   b'num_dropped_issues': 0})
            else:
                data[user_id][b'num_reviews'] += 1
            if review[b'ship_it']:
                data[user_id][b'num_ship_it'] += 1
            comments = comments_by_review[review[b'pk']]
            for comment in comments:
                if comment[b'issue_opened']:
                    data[user_id][b'num_issues'] += 1
                if comment[b'issue_status'] == BaseComment.DROPPED:
                    data[user_id][b'num_dropped_issues'] += 1

        users = list(User.objects.filter(pk__in=users_to_query - users_already_queried).values(b'pk', b'username', b'first_name', b'last_name', b'email'))
        for user in users:
            data[user[b'pk']].update(self._serialize_user(request, user))

        return data


class ReviewRelationships(Report):
    id = b'review-relationships'
    summary = _(b'Code Review Relationships')
    description = _(b'A visualization of who reviews code for whom')
    long_description_html = _(b"<p> This report shows a visualization of who performs code reviews for whom as a <em>chord graph</em>. Every user is listed along the outside of the circle, and chords are drawn between pairs of users who have done code reviews for each other. The width of the chord at each end represents how many code reviews were done by that user, and the color of the chord is the color of whichever user has done more code reviews for the other.</p><p> To get users' real names, you can hover your mouse over the  username blocks at the edge of the circle. For specific counts of  code reviews in each direction, hover your mouse over a chord.</p>")
    thumbnail_image = b'images/report-thumbnails/code-review-relationships.png'
    js_model_class = b'PowerPack.Reports.ReviewRelationships'
    js_view_class = b'PowerPack.Reports.ReviewRelationshipsView'

    def get_data(self, extension, request, get_params, local_site):
        """Return data for the report.

        This should be implemented by subclasses to return specific data for
        the report.

        Args:
            extension (rbpowerpack.extension.PowerPackExtension):
                The Power pack extension.

            request (django.http.HttpRequest):
                The HTTP request.

            get_params (dict):
                The GET parameters. This may be the same as ``request.GET``,
                but may have been pre-processed.

            local_site (reviewboard.site.models.LocalSite):
                The local site, if appropriate.

        Returns:
            JSON-serializable type:
            Data for the report.
        """
        counts, users_by_pk = self._get_data_int(request, get_params, local_site)
        user_pks = list(six.iterkeys(users_by_pk))
        return {b'matrix': [ [ counts[(i, j)] for j in user_pks ] for i in user_pks
                    ], 
           b'users': [ self._serialize_user(request, users_by_pk[pk]) for pk in user_pks
                   ]}

    def get_csv(self, extension, request, get_params, local_site):
        """Return the data for the report in CSV.

        Args:
            extension (rbpowerpack.extension.PowerPackExtension):
                The Power Pack extension.

            request (django.http.HttpRequest):
                The HTTP request.

            get_params (dict):
                The GET parameters. This may be the same as ``request.GET``,
                but may have been pre-processed.

            local_site (reviewboard.site.models.LocalSite):
                The local site, if appropriate.

        Returns:
            bytes:
            The data encoded as a UTF-8 CSV file.
        """
        output = BytesIO()
        writer = csv.DictWriter(output, fieldnames=[
         b'reviewer_username',
         b'reviewer_realname',
         b'reviewer_email',
         b'reviewee_username',
         b'reviewee_realname',
         b'reviewee_email',
         b'num_reviews'])
        writer.writeheader()
        counts, users_by_pk = self._get_data_int(request, get_params, local_site)
        for users, count in six.iteritems(counts):
            reviewer = self._serialize_user(request, users_by_pk[users[0]])
            reviewee = self._serialize_user(request, users_by_pk[users[1]])
            writer.writerow({b'reviewer_username': reviewer[b'username'].encode(b'utf-8'), 
               b'reviewer_realname': reviewer[b'name'].encode(b'utf-8'), 
               b'reviewer_email': reviewer[b'email'].encode(b'utf-8'), 
               b'reviewee_username': reviewee[b'username'].encode(b'utf-8'), 
               b'reviewee_realname': reviewee[b'name'].encode(b'utf-8'), 
               b'reviewee_email': reviewee[b'email'].encode(b'utf-8'), 
               b'num_reviews': count})

        return output.getvalue()

    def _get_data_int(self, request, get_params, local_site):
        """Do queries and return data.

        This is an internal helper that is shared between :py:meth:`get_data`
        and :py:meth:`get_csv`.

        Args:
            request (django.http.HttpRequest):
                The HTTP request.

            get_params (dict):
                The GET parameters. This may be the same as ``request.GET``,
                but may have been pre-processed.

            local_site (reviewboard.site.models.LocalSite):
                The local site, if appropriate.

        Returns:
            tuple:
            The queried data. The first element is a dictionary mapping
            2-tuples of user pks to a count of reviews. The second element is a
            map from user pk to data about that user.
        """
        form = self.form(get_params)
        if not form.is_valid():
            raise ValueError(b'Invalid report parameters.')
        reviews = Review.objects._query(user=request.user, local_site=local_site, status=None, extra_query=Q(timestamp__gte=form.cleaned_data[b'start'], timestamp__lte=form.cleaned_data[b'end']), filter_private=True)
        if not form.cleaned_data[b'everyone']:
            user_pks = set(UserQuery(local_site=local_site, usernames=form.cleaned_data[b'users'], group_names=form.cleaned_data[b'groups']).get_objects().values_list(b'pk', flat=True))
            reviews = reviews.filter(user__in=user_pks, review_request__submitter__in=user_pks)
        else:
            user_pks = set()
        reviews = list(reviews.values(b'pk', b'user_id', b'review_request_id'))
        review_request_pks = set([ review[b'review_request_id'] for review in reviews
                                 ])
        review_requests = list(ReviewRequest.objects.filter(pk__in=review_request_pks).values(b'pk', b'submitter_id'))
        submitters = {}
        for review_request in review_requests:
            user = review_request[b'submitter_id']
            submitters[review_request[b'pk']] = user
            user_pks.add(user)

        users = User.objects.filter(pk__in=user_pks).values(b'pk', b'username', b'first_name', b'last_name', b'email')
        users_by_pk = dict((user[b'pk'], user) for user in users)
        counts = defaultdict(lambda : 0)
        for review in reviews:
            reviewer = review[b'user_id']
            reviewee = submitters[review[b'review_request_id']]
            counts[(reviewer, reviewee)] += 1

        return (counts, users_by_pk)


def _populate_defaults():
    """Populates the default list of reports."""
    global _populated
    if not _populated:
        _populated = True
        for report_cls in (TimeToFeedback, TimeToClose, ReviewRequestStats,
         ReviewStats, ReviewRelationships):
            _register_report_class(report_cls)


def _register_report_class(report_cls):
    """Registers a report class.

    This will check if the report has already been registered before adding it.
    """
    _populate_defaults()
    report_id = report_cls.id
    if report_id in _registered_report_classes:
        raise KeyError(b'"%s" is already a registered report' % report_id)
    _registered_report_classes[report_id] = report_cls


def _unregister_report_class(report_cls):
    """Unregisters a previously registered report class."""
    _populate_defaults()
    report_id = report_cls.id
    if report_id not in _registered_report_classes:
        logging.error(b'Failed to unregister unknown report "%s"', report_id)
        raise KeyError(b'"%s" is not a registered report' % report_id)
    del _registered_report_classes[report_id]


def get_report_classes():
    """Returns all registered reports."""
    _populate_defaults()
    return _registered_report_classes.values()


def get_report(report_id):
    """Get an instance of a report by its ID."""
    _populate_defaults()
    return _registered_report_classes[report_id]()