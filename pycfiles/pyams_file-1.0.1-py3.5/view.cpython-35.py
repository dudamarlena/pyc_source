# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_file/skin/view.py
# Compiled at: 2019-12-20 08:10:37
# Size of source mod 2**32: 2926 bytes
"""PyAMS_file.skin.view module

This module provides a Pyramid view used to download any file.
"""
from http.client import NOT_MODIFIED, PARTIAL_CONTENT
from pyramid.response import Response
from pyramid.view import view_config
from zope.dublincore.interfaces import IZopeDublinCore
from pyams_file.interfaces import IFile
from pyams_utils.unicode import translate_string
__docformat__ = 'restructuredtext'
MAX_RANGE_LENGTH = 2097152

@view_config(context=IFile)
def FileView(request):
    """Default file view"""
    context = request.context
    content_type = context.content_type
    if isinstance(content_type, bytes):
        content_type = content_type.decode('utf-8')
    response = Response(content_type=content_type)
    zdc = IZopeDublinCore(context, None)
    if zdc is not None:
        modified = zdc.modified
        if_modified_since = request.if_modified_since
        if if_modified_since and int(modified.timestamp()) <= int(if_modified_since.timestamp()):
            return Response(content_type=content_type, status=NOT_MODIFIED)
        response.last_modified = modified
    body_file = context.get_blob(mode='c')
    if request.params.get('download') is not None:
        filename = context.filename or 'noname.txt'
        response.content_disposition = 'attachment; filename="{0}"'.format(translate_string(filename, force_lower=False))
    if request.range is not None:
        try:
            body = body_file.read()
            body_length = len(body)
            range_start = request.range.start or 0
            if 'Firefox' in request.user_agent:
                range_end = body_length
            else:
                range_end = request.range.end or min(body_length, range_start + MAX_RANGE_LENGTH)
            ranged_body = body[range_start:range_end]
            response.status = PARTIAL_CONTENT
            response.headers['Content-Range'] = 'bytes {first}-{last}/{len}'.format(first=range_start, last=range_start + len(ranged_body) - 1, len=body_length)
            response.body = ranged_body
        finally:
            body_file.close()

    else:
        response.body_file = body_file
    return response