# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/webapi/resources/base_original_file.py
# Compiled at: 2020-02-11 04:03:57
from __future__ import unicode_literals
import logging
from django.http import HttpResponse
from django.utils.six.moves.urllib.parse import quote as urllib_quote
from djblets.util.http import set_last_modified
from djblets.webapi.errors import DOES_NOT_EXIST, WebAPIError
from reviewboard.diffviewer.models import FileDiff
from reviewboard.diffviewer.diffutils import get_original_file
from reviewboard.webapi.base import WebAPIResource
from reviewboard.webapi.decorators import webapi_check_local_site, webapi_check_login_required
from reviewboard.webapi.errors import FILE_RETRIEVAL_ERROR

class BaseOriginalFileResource(WebAPIResource):
    """Base class for the original file resources."""
    added_in = b'2.0.4'
    uri_name = b'original-file'
    link_name = b'original_file'
    singleton = True
    allowed_mimetypes = [{b'item': b'text/plain'}]

    def get_filediff(self, request, *args, **kwargs):
        """Returns the FileDiff, or an error, for the given parameters."""
        raise NotImplementedError

    @webapi_check_login_required
    @webapi_check_local_site
    def get(self, request, *args, **kwargs):
        """Returns the original file.

        The file is returned as :mimetype:`text/plain` and is the original
        file before applying a patch.
        """
        result = self.get_filediff(request, *args, **kwargs)
        if isinstance(result, FileDiff):
            filediff = result
        else:
            if isinstance(result, WebAPIError):
                return result
            raise ValueError(b'Unexpected result from get_filediff')
        if filediff.is_new:
            return DOES_NOT_EXIST
        try:
            orig_file = get_original_file(filediff, request, filediff.diffset.repository.get_encoding_list())
        except Exception as e:
            logging.error(b'%s: Error retrieving original file for FileDiff %s: %s', self.__class__.__name__, filediff.pk, e, exc_info=1, request=request)
            return FILE_RETRIEVAL_ERROR

        resp = HttpResponse(orig_file, content_type=b'text/plain')
        filename = urllib_quote(filediff.source_file)
        resp[b'Content-Disposition'] = b'inline; filename=%s' % filename
        set_last_modified(resp, filediff.diffset.timestamp)
        return resp