# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/rbbz/extension.py
# Compiled at: 2015-01-29 15:15:33
import json, logging, re
from django.contrib.sites.models import Site
from django.db.models.signals import pre_delete
from djblets.siteconfig.models import SiteConfiguration
from djblets.util.decorators import simple_decorator
from reviewboard.extensions.base import Extension
from reviewboard.extensions.hooks import AuthBackendHook, SignalHook
from reviewboard.reviews.errors import PublishError
from reviewboard.reviews.models import ReviewRequest, ReviewRequestDraft
from reviewboard.reviews.signals import reply_publishing, review_publishing, review_request_closed, review_request_publishing, review_request_reopened
from reviewboard.site.urlresolvers import local_site_reverse
from rbbz.auth import BugzillaBackend
from rbbz.bugzilla import Bugzilla
from rbbz.diffs import build_plaintext_review
from rbbz.errors import BugzillaError, ConfidentialBugError, InvalidBugIdError
from rbbz.middleware import BugzillaCookieAuthMiddleware, CorsHeaderMiddleware
from rbbz.models import BugzillaUserMap, get_or_create_bugzilla_users
from rbbz.resources import bugzilla_cookie_login_resource
REVIEWID_RE = re.compile('bz://(\\d+)/[^/]+')
AUTO_CLOSE_DESCRIPTION = '\nDiscarded automatically because parent review request was discarded.\n'
AUTO_SUBMITTED_DESCRIPTION = '\nSubmitted because the parent review request was submitted.\n'
NEVER_USED_DESCRIPTION = '\nDiscarded because this review request ended up not being needed.\n'
OBSOLETE_DESCRIPTION = '\nDiscarded because this change is no longer required.\n'
DRAFTED_EXTRA_DATA_KEYS = [
 'p2rb.identifier',
 'p2rb.commit_id',
 'p2rb.commits']

class BugzillaExtension(Extension):
    middleware = [
     BugzillaCookieAuthMiddleware, CorsHeaderMiddleware]
    resources = [
     bugzilla_cookie_login_resource]

    def initialize(self):
        AuthBackendHook(self, BugzillaBackend)
        SignalHook(self, pre_delete, on_draft_pre_delete)
        SignalHook(self, review_request_publishing, on_review_request_publishing, sandbox_errors=False)
        SignalHook(self, review_publishing, on_review_publishing)
        SignalHook(self, reply_publishing, on_reply_publishing)
        SignalHook(self, review_request_closed, on_review_request_closed_discarded)
        SignalHook(self, review_request_closed, on_review_request_closed_submitted)
        SignalHook(self, review_request_reopened, on_review_request_reopened)


def review_or_request_url(review_or_request, site=None, siteconfig=None):
    if not site:
        site = Site.objects.get_current()
    if not siteconfig:
        siteconfig = SiteConfiguration.objects.get_current()
    return '%s://%s%s%s' % (
     siteconfig.get('site_domain_method'), site.domain,
     local_site_reverse('root').rstrip('/'),
     review_or_request.get_absolute_url())


def is_review_request_pushed(review_request):
    return str(review_request.extra_data.get('p2rb', False)) == 'True'


def is_review_request_squashed(review_request):
    squashed = str(review_request.extra_data.get('p2rb.is_squashed', False))
    return squashed == 'True'


def on_draft_pre_delete(sender, instance, using, **kwargs):
    """ Handle draft discards.

    There are no handy signals built into Review Board (yet) for us to detect
    when a squashed Review Request Draft is discarded. Instead, we monitor for
    deletions of models, and handle cases where the models being deleted are
    ReviewRequestDrafts. We then do some processing to ensure that the draft
    is indeed a draft of a squashed review request that we want to handle,
    and then propagate the discard down to the child review requests.
    """
    if not sender == ReviewRequestDraft:
        return
    else:
        if instance.changedesc is None or instance.changedesc.public:
            return
        review_request = instance.review_request
        if not review_request:
            return
        if not is_review_request_squashed(review_request):
            return
        if review_request.status == ReviewRequest.DISCARDED:
            return
        user = review_request.submitter
        for child in gen_child_rrs(review_request):
            draft = child.get_draft()
            if draft:
                draft.delete()

        for child in gen_rrs_by_extra_data_key(review_request, 'unpublished_rids'):
            child.close(ReviewRequest.DISCARDED, user=user, description=NEVER_USED_DESCRIPTION)

        review_request.extra_data['p2rb.discard_on_publish_rids'] = '[]'
        review_request.extra_data['p2rb.unpublished_rids'] = '[]'
        review_request.save()
        return


@simple_decorator
def bugzilla_to_publish_errors(func):

    def _transform_errors(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except BugzillaError, e:
            raise PublishError('Bugzilla error: %s' % e.msg)

    return _transform_errors


@bugzilla_to_publish_errors
def on_review_request_publishing(user, review_request_draft, **kwargs):
    if not review_request_draft:
        logging.error('Strangely, there was no review request draft on the review request we were attempting to publish.')
        return
    else:
        review_request = review_request_draft.get_review_request()
        if not is_review_request_pushed(review_request):
            return
        reviewid = review_request_draft.extra_data.get('p2rb.identifier', None)
        m = REVIEWID_RE.match(reviewid)
        if not m:
            raise InvalidBugIdError('<unknown>')
        bug_id = m.group(1)
        using_bugzilla = we_are_using_bugzilla()
        try:
            bug_id = int(bug_id)
        except (TypeError, ValueError):
            raise InvalidBugIdError(bug_id)

        if using_bugzilla:
            b = Bugzilla(user.bzlogin, user.bzcookie)
            try:
                if b.is_bug_confidential(bug_id):
                    raise ConfidentialBugError
            except BugzillaError, e:
                if e.fault_code and (e.fault_code == 100 or e.fault_code == 101):
                    raise InvalidBugIdError(bug_id)
                raise

        review_request_draft.bugs_closed = str(bug_id)
        reviewers = set()
        for u in review_request_draft.target_people.all():
            if not using_bugzilla:
                reviewers.append(u.get_username())
            bum = BugzillaUserMap.objects.get(user=u)
            user_data = b.get_user_from_userid(bum.bugzilla_user_id)
            users = get_or_create_bugzilla_users(user_data)
            reviewers.add(users[0].email)

        if is_review_request_squashed(review_request):
            comment = review_request_draft.description
            if review_request_draft.changedesc and review_request_draft.changedesc.text:
                if not comment.endswith('\n'):
                    comment += '\n'
                comment += '\n%s' % review_request_draft.changedesc.text
            if using_bugzilla:
                b.post_rb_url(bug_id, review_request.id, review_request_draft.summary, comment, review_or_request_url(review_request), reviewers)
            unpublished_rids = json.loads(review_request.extra_data['p2rb.unpublished_rids'])
            discard_on_publish_rids = json.loads(review_request.extra_data['p2rb.discard_on_publish_rids'])
            for child in gen_child_rrs(review_request_draft):
                if child.get_draft(user=user) or not child.public:
                    child.publish(user=user)
                    id_str = str(child.id)
                    if id_str in unpublished_rids:
                        unpublished_rids.remove(id_str)

            for child in gen_rrs_by_rids(unpublished_rids):
                child.close(ReviewRequest.DISCARDED, user=user, description=NEVER_USED_DESCRIPTION)

            for child in gen_rrs_by_rids(discard_on_publish_rids):
                child.close(ReviewRequest.DISCARDED, user=user, description=OBSOLETE_DESCRIPTION)

            review_request.extra_data['p2rb.unpublished_rids'] = '[]'
            review_request.extra_data['p2rb.discard_on_publish_rids'] = '[]'
        draft_extra_data = review_request_draft.extra_data
        for key in DRAFTED_EXTRA_DATA_KEYS:
            if key in draft_extra_data:
                review_request.extra_data[key] = draft_extra_data[key]

        review_request.save()
        return


@bugzilla_to_publish_errors
def on_review_publishing(user, review, **kwargs):
    review_request = review.review_request
    if not is_review_request_pushed(review_request):
        return
    bug_id = int(review_request.get_bug_list()[0])
    site = Site.objects.get_current()
    siteconfig = SiteConfiguration.objects.get_current()
    comment = build_plaintext_review(review, review_or_request_url(review, site, siteconfig), {'user': user})
    b = Bugzilla(user.bzlogin, user.bzcookie)
    rr_url = review_or_request_url(review_request, site, siteconfig)
    if review.ship_it and is_review_request_squashed(review_request):
        b.r_plus_attachment(bug_id, review.user.email, comment, rr_url)
    else:
        cancelled = b.cancel_review_request(bug_id, review.user.email, rr_url, comment)
        if not cancelled and comment:
            b.post_comment(bug_id, comment)


@bugzilla_to_publish_errors
def on_reply_publishing(user, reply, **kwargs):
    review_request = reply.review_request
    if not is_review_request_pushed(review_request):
        return
    bug_id = int(review_request.get_bug_list()[0])
    b = Bugzilla(user.bzlogin, user.bzcookie)
    url = review_or_request_url(reply)
    comment = build_plaintext_review(reply, url, {'user': user})
    b.post_comment(bug_id, comment)


def on_review_request_closed_discarded(user, review_request, type, **kwargs):
    if not is_review_request_squashed(review_request) or type != ReviewRequest.DISCARDED:
        return
    else:
        review_request.commit = None
        close_child_review_requests(user, review_request, ReviewRequest.DISCARDED, AUTO_CLOSE_DESCRIPTION)
        b = Bugzilla(user.bzlogin, user.bzcookie)
        bug = int(review_request.get_bug_list()[0])
        url = review_or_request_url(review_request)
        b.obsolete_review_attachments(bug, url)
        return


def on_review_request_closed_submitted(user, review_request, type, **kwargs):
    if not is_review_request_squashed(review_request) or type != ReviewRequest.SUBMITTED:
        return
    close_child_review_requests(user, review_request, ReviewRequest.SUBMITTED, AUTO_SUBMITTED_DESCRIPTION)


def close_child_review_requests(user, review_request, status, child_close_description):
    """Closes all child review requests for a squashed review request."""
    for child in gen_child_rrs(review_request):
        child.close(status, user=user, description=child_close_description)

    for child in gen_rrs_by_extra_data_key(review_request, 'unpublished_rids'):
        child.close(ReviewRequest.DISCARDED, user=user, description=NEVER_USED_DESCRIPTION)

    review_request.extra_data['p2rb.unpublished_rids'] = '[]'
    review_request.extra_data['p2rb.discard_on_publish_rids'] = '[]'
    review_request.save()


def on_review_request_reopened(user, review_request, **kwargs):
    if not is_review_request_squashed(review_request):
        return
    identifier = review_request.extra_data['p2rb.identifier']
    try:
        preexisting_review_request = ReviewRequest.objects.get(commit_id=identifier)
        if preexisting_review_request != review_request:
            logging.error('Could not revive review request with ID %s because its commit id (%s) is already being used by a review request with ID %s.' % (
             review_request.id, identifier,
             preexisting_review_request.id))
            raise Exception('Revive failed because a review request with commit ID %s already exists.' % identifier)
    except ReviewRequest.DoesNotExist:
        pass

    for child in gen_child_rrs(review_request):
        child.reopen(user=user)

    review_request.commit = identifier
    review_request.save()
    draft = review_request.get_draft(user)
    if draft:
        draft.commit = identifier
        draft.save()


def gen_child_rrs(review_request):
    """ Generate child review requests.

    For some review request (draft or normal), that has a p2rb.commits
    extra_data field, we yield the child review requests belonging to
    the rids in that field.

    If a review request is not found for the listed ID, get_rr_for_id will
    log this, and we'll skip that ID.
    """
    key = 'p2rb.commits'
    if key not in review_request.extra_data:
        return
    commit_tuples = json.loads(review_request.extra_data[key])
    for commit_tuple in commit_tuples:
        child = get_rr_for_id(commit_tuple[1])
        if child:
            yield child


def gen_rrs_by_extra_data_key(review_request, key):
    key = 'p2rb.' + key
    if key not in review_request.extra_data:
        return
    return gen_rrs_by_rids(json.loads(review_request.extra_data[key]))


def gen_rrs_by_rids(rids):
    for rid in rids:
        review_request = get_rr_for_id(rid)
        if review_request:
            yield review_request


def get_rr_for_id(rid):
    try:
        return ReviewRequest.objects.get(pk=rid)
    except ReviewRequest.DoesNotExist:
        logging.error('Could not retrieve child review request with rid %s because it does not appear to exist.' % rid)


def we_are_using_bugzilla():
    siteconfig = SiteConfiguration.objects.get_current()
    return siteconfig.settings.get('auth_backend', 'builtin') == 'bugzilla'