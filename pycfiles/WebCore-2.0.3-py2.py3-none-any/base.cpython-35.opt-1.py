# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web/ext/base.py
# Compiled at: 2016-09-25 02:30:01
# Size of source mod 2**32: 5961 bytes
"""The base extension providing request, response, and core views."""
from __future__ import unicode_literals
from io import IOBase
try:
    IOBase = (
     IOBase, file)
except:
    pass

try:
    from collections import Generator
except ImportError:

    def _tmp():
        yield


    Generator = type(_tmp())

from os.path import getmtime
from time import mktime, gmtime
from datetime import datetime
from mimetypes import init, add_type, guess_type
from collections import namedtuple
from webob import Request, Response
from web.core.compat import str, unicode, Path
from web.core.util import safe_name
log = __import__('logging').getLogger(__name__)
Crumb = namedtuple('Breadcrumb', ('handler', 'path'))

class Bread(list):

    @property
    def current(self):
        return self[(-1)].path


class BaseExtension(object):
    __doc__ = 'Base framework extension.\n\t\n\tThis extension is not meant to be manually constructed or manipulated; use is automatic.\n\t'
    first = True
    always = True
    provides = ['base', 'request', 'response']

    def start(self, context):
        init()
        add_type('text/x-yaml', 'yml')
        add_type('text/x-yaml', 'yaml')
        register = context.view.register
        register(type(None), self.render_none)
        register(Response, self.render_response)
        register(str, self.render_binary)
        register(unicode, self.render_text)
        register(IOBase, self.render_file)
        register(Generator, self.render_generator)

    def prepare(self, context):
        """Add the usual suspects to the context.
                
                This adds `request`, `response`, and `path` to the `RequestContext` instance.
                """
        context.request = Request(context.environ)
        context.response = Response(request=context.request)
        context.environ['web.base'] = context.request.script_name
        context.request.remainder = context.request.path_info.split('/')
        if context.request.remainder and not context.request.remainder[0]:
            del context.request.remainder[0]
        context.path = Bread()

    def dispatch(self, context, consumed, handler, is_endpoint):
        """Called as dispatch descends into a tier.
                
                The base extension uses this to maintain the "current url".
                """
        request = context.request
        if not consumed and context.request.path_info_peek() == '':
            consumed = [
             '']
        if consumed:
            if not isinstance(consumed, (list, tuple)):
                consumed = consumed.split('/')
            for element in consumed:
                if element == context.request.path_info_peek():
                    context.request.path_info_pop()

        context.path.append(Crumb(handler, Path(request.script_name)))
        if consumed:
            request.remainder = request.remainder[len(consumed):]

    def render_none(self, context, result):
        """Render empty responses."""
        context.response.body = b''
        del context.response.content_length
        return True

    def render_response(self, context, result):
        """Allow direct returning of WebOb `Response` instances."""
        context.response = result
        return True

    def render_binary(self, context, result):
        """Return binary responses unmodified."""
        context.response.app_iter = iter((result,))
        return True

    def render_text(self, context, result):
        """Return textual responses, encoding as needed."""
        context.response.text = result
        return True

    def render_file(self, context, result):
        """Perform appropriate metadata wrangling for returned open file handles."""
        response = context.response
        response.conditional_response = True
        modified = mktime(gmtime(getmtime(result.name)))
        response.last_modified = datetime.fromtimestamp(modified)
        ct, ce = guess_type(result.name)
        if not ct:
            ct = 'application/octet-stream'
        response.content_type, response.content_encoding = ct, ce
        response.etag = unicode(modified)
        result.seek(0, 2)
        response.content_length = result.tell()
        result.seek(0)
        response.body_file = result
        return True

    def render_generator(self, context, result):
        """Attempt to serve generator responses through stream encoding.
                
                This allows for direct use of cinje template functions, which are generators, as returned views.
                """
        context.response.encoding = 'utf8'
        context.response.app_iter = ((i.encode('utf8') if isinstance(i, unicode) else i) for i in result if i is not None)
        return True