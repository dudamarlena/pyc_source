# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/reviews/context.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
from django.utils import six
from django.utils.translation import ugettext as _
from django.template.defaultfilters import truncatechars
from djblets.siteconfig.models import SiteConfiguration
from reviewboard.accounts.models import ReviewRequestVisit
from reviewboard.admin.server import build_server_url
from reviewboard.diffviewer.models import DiffSet
from reviewboard.reviews.forms import UploadDiffForm
from reviewboard.reviews.markdown_utils import markdown_render_conditional, normalize_text_for_edit
from reviewboard.reviews.models import BaseComment
from reviewboard.site.urlresolvers import local_site_reverse

def comment_counts(user, all_comments, filediff, interfilediff=None):
    """
    Returns an array of current comments for a filediff, sorted by line number.

    Each entry in the array has a dictionary containing the following keys:

    =========== ==================================================
    Key                Description
    =========== ==================================================
    comment_id         The ID of the comment
    text               The plain or rich text of the comment
    rich_text          The rich text flag for the comment
    line               The first line number
    num_lines          The number of lines this comment spans
    user               A dictionary containing "username" and "name" keys
                       for the user
    url                The URL to the comment
    localdraft         True if this is the current user's draft comment
    review_id          The ID of the review this comment is associated with
    ==============================================================
    """
    comment_dict = {}
    if interfilediff:
        key = (
         filediff.pk, interfilediff.pk)
    else:
        key = (
         filediff.pk, None)
    comments = all_comments.get(key, [])
    for comment in comments:
        review = comment.get_review()
        if review and (review.public or review.user_id == user.pk):
            key = (
             comment.first_line, comment.num_lines)
            comment_dict.setdefault(key, []).append({b'comment_id': comment.id, 
               b'text': normalize_text_for_edit(user, comment.text, comment.rich_text), 
               b'html': markdown_render_conditional(comment.text, comment.rich_text), 
               b'rich_text': comment.rich_text, 
               b'line': comment.first_line, 
               b'num_lines': comment.num_lines, 
               b'user': {b'username': review.user.username, 
                         b'name': review.user.get_full_name() or review.user.username}, 
               b'url': comment.get_review_url(), 
               b'localdraft': review.user == user and not review.public, 
               b'review_id': review.id, 
               b'issue_opened': comment.issue_opened, 
               b'issue_status': BaseComment.issue_status_to_string(comment.issue_status), 
               b'reply_to_id': comment.reply_to_id})

    comments_array = []
    for key, value in six.iteritems(comment_dict):
        comments_array.append({b'linenum': key[0], 
           b'num_lines': key[1], 
           b'comments': value})

    comments_array.sort(cmp=lambda x, y: cmp(x[b'linenum'], y[b'linenum'] or cmp(x[b'num_lines'], y[b'num_lines'])))
    return comments_array


def make_review_request_context(request, review_request, extra_context={}, is_diff_view=False):
    """Returns a dictionary for template contexts used for review requests.

    The dictionary will contain the common data that is used for all
    review request-related pages (the review request detail page, the diff
    viewer, and the screenshot pages).

    For convenience, extra data can be passed to this dictionary.
    """
    if review_request.repository:
        upload_diff_form = UploadDiffForm(review_request, request=request)
        scmtool = review_request.repository.get_scmtool()
    else:
        upload_diff_form = None
        scmtool = None
    if b'blocks' not in extra_context:
        extra_context[b'blocks'] = list(review_request.blocks.all())
    tabs = [
     {b'text': _(b'Reviews'), 
        b'url': review_request.get_absolute_url()}]
    draft = review_request.get_draft(request.user)
    if draft and draft.diffset_id or hasattr(review_request, b'_diffsets') and len(review_request._diffsets) > 0:
        has_diffs = True
    else:
        has_diffs = DiffSet.objects.filter(history__pk=review_request.diffset_history_id).exists()
    if has_diffs:
        tabs.append({b'active': is_diff_view, 
           b'text': _(b'Diff'), 
           b'url': local_site_reverse(b'view-diff', args=[
                  review_request.display_id], local_site=review_request.local_site) + b'#index_header'})
    siteconfig = SiteConfiguration.objects.get_current()
    review_request_details = extra_context.get(b'review_request_details', review_request)
    social_page_description = truncatechars(review_request_details.description.replace(b'\n', b' '), 300)
    context = dict({b'mutable_by_user': review_request.is_mutable_by(request.user), 
       b'status_mutable_by_user': review_request.is_status_mutable_by(request.user), 
       b'review_request': review_request, 
       b'upload_diff_form': upload_diff_form, 
       b'scmtool': scmtool, 
       b'send_email': siteconfig.get(b'mail_send_review_mail'), 
       b'tabs': tabs, 
       b'social_page_description': social_page_description, 
       b'social_page_url': build_server_url(request.path, request=request)}, **extra_context)
    if b'review_request_visit' not in context and request.user.is_authenticated():
        context[b'review_request_visit'] = ReviewRequestVisit.objects.get_or_create(user=request.user, review_request=review_request)[0]
    return context


def has_comments_in_diffsets_excluding(review, diffset_pair):
    """Returns whether the specified review has "other comments".

    This is used to notify users that their review has comments on diff
    revisions other than the one that they happen to be looking at at any given
    moment.
    """
    if not review:
        return False
    current_diffset, interdiff = diffset_pair
    q = DiffSet.objects.filter(files__comments__review=review)
    q = q.filter(files__comments__interfilediff__isnull=True).distinct()
    if not interdiff:
        q = q.exclude(pk=current_diffset.id)
    if q.exists():
        return True
    q = DiffSet.objects.filter(files__comments__review=review)
    q = q.filter(files__comments__interfilediff__isnull=False)
    if interdiff:
        q = q.exclude(pk=current_diffset.id, files__comments__interfilediff__diffset=interdiff)
    return q.exists()


def diffsets_with_comments(review, current_pair):
    """Returns a list of diffsets in the review that contain draft comments."""
    if not review:
        return
    else:
        diffsets = DiffSet.objects.filter(files__comments__review=review)
        diffsets = diffsets.filter(files__comments__interfilediff__isnull=True)
        diffsets = diffsets.distinct()
        for diffset in diffsets:
            yield {b'diffset': diffset, 
               b'is_current': current_pair[0] == diffset and current_pair[1] is None}

        return


def interdiffs_with_comments(review, current_pair):
    """Get a list of interdiffs in the review that contain draft comments."""
    if not review:
        return
    diffsets = DiffSet.objects.filter(files__comments__review=review)
    diffsets = diffsets.filter(files__comments__interfilediff__isnull=False)
    diffsets = diffsets.distinct()
    for diffset in diffsets:
        interdiffs = DiffSet.objects.filter(files__interdiff_comments__filediff__diffset=diffset).distinct()
        for interdiff in interdiffs:
            yield {b'diffset': diffset, 
               b'interdiff': interdiff, 
               b'is_current': current_pair[0] == diffset and current_pair[1] == interdiff}