# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/webapi/resources/draft_patched_file.py
# Compiled at: 2020-02-11 04:03:57
from __future__ import unicode_literals
from django.core.exceptions import ObjectDoesNotExist
from djblets.webapi.errors import DOES_NOT_EXIST
from reviewboard.webapi.resources import resources
from reviewboard.webapi.resources.base_patched_file import BasePatchedFileResource

class DraftPatchedFileResource(BasePatchedFileResource):
    """Provides the patched file corresponding to a draft file diff."""
    added_in = b'2.0.4'
    name = b'draft_patched_file'

    def get_filediff(self, request, *args, **kwargs):
        """Returns the FileDiff, or an error, for the given parameters."""
        draft_resource = resources.review_request_draft
        try:
            draft = draft_resource.get_object(request, *args, **kwargs)
        except ObjectDoesNotExist:
            return DOES_NOT_EXIST

        if not draft_resource.has_access_permissions(request, draft):
            return self.get_no_access_error(request)
        try:
            return resources.draft_filediff.get_object(request, *args, **kwargs)
        except ObjectDoesNotExist:
            return DOES_NOT_EXIST


draft_patched_file_resource = DraftPatchedFileResource()