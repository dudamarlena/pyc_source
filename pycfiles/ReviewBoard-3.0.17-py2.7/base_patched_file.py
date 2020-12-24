# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/webapi/resources/base_patched_file.py
# Compiled at: 2020-02-11 04:03:57
from __future__ import unicode_literals
import logging
from django.http import HttpResponse
from django.utils.six.moves.urllib.parse import quote as urllib_quote
from djblets.util.http import set_last_modified
from djblets.webapi.errors import DOES_NOT_EXIST, WebAPIError
from reviewboard.diffviewer.models import FileDiff
from reviewboard.diffviewer.diffutils import get_original_file, get_patched_file
from reviewboard.webapi.base import WebAPIResource
from reviewboard.webapi.decorators import webapi_check_local_site, webapi_check_login_required
from reviewboard.webapi.errors import FILE_RETRIEVAL_ERROR

class BasePatchedFileResource(WebAPIResource):
    """Base class for the patched file resources."""
    added_in = b'2.0.4'
    uri_name = b'patched-file'
    link_name = b'patched_file'
    singleton = True
    allowed_mimetypes = [{b'item': b'text/plain'}]

    def get_filediff(self, request, *args, **kwargs):
        """Returns the FileDiff, or an error, for the given parameters."""
        raise NotImplementedError

    @webapi_check_login_required
    @webapi_check_local_site
    def get(self, request, *args, **kwargs):
        """Returns the patched file.

        The file is returned as :mimetype:`text/plain` and is the result
        of applying the patch to the original file.
        """
        result = self.get_filediff(request, *args, **kwargs)
        if isinstance(result, FileDiff):
            filediff = result
        else:
            if isinstance(result, WebAPIError):
                return result
            raise ValueError(b'Unexpected result from get_filediff')
        if filediff.deleted:
            return DOES_NOT_EXIST
        try:
            orig_file = get_original_file(filediff, request, filediff.diffset.repository.get_encoding_list())
        except Exception as e:
            logging.error(b'%s: Error retrieving original file for FileDiff %s: %s', self.__class__.__name__, filediff.pk, e, exc_info=1, request=request)
            return FILE_RETRIEVAL_ERROR

        try:
            patched_file = get_patched_file(orig_file, filediff, request)
        except Exception as e:
            logging.error(b'%s: Error retrieving patched file for FileDiff %s: %s', self.__class__.__name__, filediff.pk, e, exc_info=1, request=request)
            return FILE_RETRIEVAL_ERROR

        resp = HttpResponse(patched_file, content_type=b'text/plain')
        filename = urllib_quote(filediff.dest_file)
        resp[b'Content-Disposition'] = b'inline; filename=%s' % filename
        set_last_modified(resp, filediff.diffset.timestamp)
        return resp