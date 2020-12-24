# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/webapi/resources/diff_context.py
# Compiled at: 2020-02-11 04:03:57
from __future__ import unicode_literals
from django.http import Http404
from django.utils import six
from djblets.webapi.decorators import webapi_response_errors, webapi_request_fields
from djblets.webapi.errors import DOES_NOT_EXIST
from reviewboard.reviews.views import ReviewsDiffViewerView
from reviewboard.webapi.base import WebAPIResource
from reviewboard.webapi.decorators import webapi_check_local_site, webapi_check_login_required
from reviewboard.webapi.resources import resources

class DiffViewerContextView(ReviewsDiffViewerView):

    def render_to_response(self, context, **kwargs):
        return context


class DiffContextResource(WebAPIResource):
    """Provides context information for a specific diff view.

    The output of this is more or less internal to the Review Board web UI.
    This will return the various pieces of information required to render a
    diff view for a given diff revision/interdiff. This is used to re-render
    the diff viewer without a reload when navigating between revisions.
    """
    added_in = b'2.0'
    name = b'diff_context'
    singleton = True

    @webapi_check_login_required
    @webapi_check_local_site
    @webapi_request_fields(optional={b'revision': {b'type': int, 
                     b'description': b'Which revision of the diff to show.'}, 
       b'filenames': {b'type': six.text_type, 
                      b'description': b'A list of case-sensitive filenames or Unix shell patterns used to filter the resulting list of files.', 
                      b'added_in': b'3.0.4'}, 
       b'interdiff-revision': {b'type': int, 
                               b'description': b'A tip revision for showing interdiffs. If this is provided, the ``revision`` field will be the base diff.', 
                               b'added_in': b'2.0.7'}, 
       b'page': {b'type': int, 
                 b'description': b'The page number for paginated diffs.'}})
    @webapi_response_errors(DOES_NOT_EXIST)
    def get(self, request, review_request_id, local_site_name=None, *args, **kwargs):
        """Returns the context info for a particular revision or interdiff.

        The output of this is more or less internal to the Review Board web UI.
        The result will be an object with several fields for the files in the
        diff, pagination information, and other data which is used to render
        the diff viewer page.

        Note that in versions 2.0.0 through 2.0.6, the ``interdiff-revision``
        parameter was named ``interdiff_revision``. Because of the internal
        nature of this API, this was changed without adding backwards
        compatibility for 2.0.7.
        """
        revision = request.GET.get(b'revision')
        interdiff_revision = request.GET.get(b'interdiff-revision')
        review_request = resources.review_request.get_object(request, review_request_id=review_request_id, local_site_name=local_site_name, *args, **kwargs)
        if not review_request.is_accessible_by(request.user):
            return self.get_no_access_error(request, obj=review_request, *args, **kwargs)
        try:
            view = DiffViewerContextView.as_view()
            context = view(request=request, review_request_id=review_request_id, revision=revision, interdiff_revision=interdiff_revision, local_site_name=local_site_name)
        except Http404:
            return DOES_NOT_EXIST

        return (200,
         {self.item_result_key: context[b'diff_context']})


diff_context_resource = DiffContextResource()