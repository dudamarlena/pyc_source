# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tomchristie/GitHub/api-star/api_star/core.py
# Compiled at: 2016-04-14 12:24:07
# Size of source mod 2**32: 1019 bytes
from api_star.compat import string_types, text_type
from api_star.exceptions import Forbidden

def check_permissions(request, permissions):
    for permission in permissions:
        if not permission(request):
            raise Forbidden()
            continue


def render(request, data):
    """
    Given the incoming request, and the outgoing data,
    determine the content type and content of the response.
    """
    renderer = request.renderer or request.renderers[0]
    if data is None:
        content = b''
    else:
        if not isinstance(data, string_types):
            context = {'request': request}
            content = renderer(data, **context)
        else:
            content = data
        if isinstance(content, text_type):
            if renderer.charset:
                content = content.encode(renderer.charset)
        if renderer.media_type:
            content_type = '%s' % renderer.media_type
            if renderer.charset:
                content_type += '; charset=%s' % renderer.charset
        else:
            content_type = None
    return (
     content, content_type)