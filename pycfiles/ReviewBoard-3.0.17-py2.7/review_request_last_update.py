# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/webapi/resources/review_request_last_update.py
# Compiled at: 2020-02-11 04:03:57
from __future__ import unicode_literals
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotModified
from django.utils import six
from django.utils.translation import ugettext as _
from djblets.util.http import encode_etag, etag_if_none_match
from djblets.webapi.errors import DOES_NOT_EXIST
from reviewboard.diffviewer.models import DiffSet
from reviewboard.reviews.models import Review, ReviewRequest
from reviewboard.webapi.base import WebAPIResource
from reviewboard.webapi.decorators import webapi_check_local_site, webapi_check_login_required
from reviewboard.webapi.resources import resources

class ReviewRequestLastUpdateResource(WebAPIResource):
    """Provides information on the last update made to a review request.

    Clients can periodically poll this to see if any new updates have been
    made.
    """
    name = b'last_update'
    policy_id = b'review_request_last_update'
    singleton = True
    allowed_methods = ('GET', )
    fields = {b'summary': {b'type': six.text_type, 
                    b'description': b'A short summary of the update. This should be one of "Review request updated", "Diff updated", "New reply" or "New review".'}, 
       b'timestamp': {b'type': six.text_type, 
                      b'description': b'The timestamp of this most recent update (``YYYY-MM-DD HH:MM:SS`` format).'}, 
       b'type': {b'type': ('review-request', 'diff', 'reply', 'review'), 
                 b'description': b"The type of the last update. ``review-request`` means the last update was an update of the review request's information. ``diff`` means a new diff was uploaded. ``reply`` means a reply was made to an existing review. ``review`` means a new review was posted."}, 
       b'user': {b'type': six.text_type, 
                 b'description': b'The username for the user who made the last update.'}}

    @webapi_check_login_required
    @webapi_check_local_site
    def get(self, request, *args, **kwargs):
        """Returns the last update made to the review request.

        This shows the type of update that was made, the user who made the
        update, and when the update was made. Clients can use this to inform
        the user that the review request was updated, or automatically update
        it in the background.

        This does not take into account changes to a draft review request, as
        that's generally not update information that the owner of the draft is
        interested in. Only public updates are represented.
        """
        try:
            review_request = resources.review_request.get_object(request, *args, **kwargs)
        except ObjectDoesNotExist:
            return DOES_NOT_EXIST

        if not resources.review_request.has_access_permissions(request, review_request):
            return self.get_no_access_error(request)
        else:
            info = review_request.get_last_activity_info()
            timestamp = info[b'timestamp']
            updated_object = info[b'updated_object']
            changedesc = info[b'changedesc']
            etag = encode_etag(b'%s:%s' % (timestamp, updated_object.pk))
            if etag_if_none_match(request, etag):
                return HttpResponseNotModified()
            summary = None
            update_type = None
            user = None
            if isinstance(updated_object, ReviewRequest):
                if updated_object.status == ReviewRequest.SUBMITTED:
                    summary = _(b'Review request submitted')
                elif updated_object.status == ReviewRequest.DISCARDED:
                    summary = _(b'Review request discarded')
                else:
                    summary = _(b'Review request updated')
                update_type = b'review-request'
            elif isinstance(updated_object, DiffSet):
                summary = _(b'Diff updated')
                update_type = b'diff'
            elif isinstance(updated_object, Review):
                if updated_object.is_reply():
                    summary = _(b'New reply')
                    update_type = b'reply'
                else:
                    summary = _(b'New review')
                    update_type = b'review'
                user = updated_object.user
            else:
                assert False
            if changedesc:
                user = changedesc.get_user(review_request)
            elif user is None:
                user = review_request.submitter
            return (200,
             {self.item_result_key: {b'timestamp': timestamp, 
                                       b'user': user, 
                                       b'summary': summary, 
                                       b'type': update_type}},
             {b'ETag': etag})


review_request_last_update_resource = ReviewRequestLastUpdateResource()