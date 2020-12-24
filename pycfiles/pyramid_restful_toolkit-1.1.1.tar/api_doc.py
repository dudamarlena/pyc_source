# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /sources/github/pyramid_restful_toolkit/pyramid_restful_toolkit/api_doc.py
# Compiled at: 2014-08-28 06:07:04
"""This module add a view for API's documentation.

Every API with '__doc__' appended to path_info will trigger this view.

This view simply returns the view (that will serve the API without __doc__)'s
__doc__ attribute.
"""
from pyramid.response import Response
from pyramid.httpexceptions import HTTPNotFound
from pyramid.scripts import pviews
from pyramid.config.views import view_description
from pyramid.scripting import _make_request
import six, sys
if six.PY2:
    _MAX_INT = sys.maxint
else:
    _MAX_INT = sys.maxsize
try:
    from docutils.core import publish_parts
    reST2html = lambda txt: publish_parts(txt, writer_name='html')['html_body']
    __HTML__ = '<html>\n<head>\n    <link rel="stylesheet"\n          type="text/css"\n          href="//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css" />\n    <style>\n        body {\n            font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;\n        }\n    </style>\n</head>\n<body>\n    <div class="container">\n        <div class="page-header">\n            <h1>%(api_name)s</h1>\n        </div>\n        %(body)s\n    </div>\n</body>\n</html>\n'

    def _render(api_name, body):
        html = __HTML__ % {'api_name': api_name, 
           'body': body}
        return Response(body=html)


except ImportError:
    reST2html = lambda txt: txt

    def _render(api_name, body):
        html = api_name.upper() + '\n\n' + body
        return Response(body=html, content_type='text/plain')


def trim_docstring(docstring):
    if not docstring:
        return ''
    lines = docstring.expandtabs().splitlines()
    indent = _MAX_INT
    for line in lines[1:]:
        stripped = line.lstrip()
        if stripped:
            indent = min(indent, len(line) - len(stripped))

    trimmed = [
     lines[0].strip()]
    if indent < _MAX_INT:
        for line in lines[1:]:
            trimmed.append(line[indent:].rstrip())

    while trimmed and not trimmed[(-1)]:
        trimmed.pop()

    while trimmed and not trimmed[0]:
        trimmed.pop(0)

    return ('\n').join(trimmed)


def api_doc_view(context, request):
    """
    :type request: pyramid.request.Request
    """
    sim_request = _make_request('/' + request.matchdict['api_path_info'], request.registry)
    cmd = pviews.PViewsCommand([])
    found_view = cmd._find_view(sim_request)
    if found_view is None:
        raise HTTPNotFound('API not found')
    original_view = found_view.__original_view__
    try:
        view = getattr(original_view, found_view.__view_attr__)
    except AttributeError:
        view = original_view

    doc = trim_docstring(view.__doc__)
    html = reST2html(doc)
    return _render(view_description(found_view), html)