# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/argonaut/controllers/error.py
# Compiled at: 2011-02-18 19:15:09
import cgi
from paste.urlparser import PkgResourcesParser
from pylons.middleware import error_document_template
from webhelpers.html.builder import literal
from argonaut.lib.base import BaseController

class ErrorController(BaseController):
    """Generates error documents as and when they are required.

    The ErrorDocuments middleware forwards to ErrorController when error
    related status codes are returned from the application.

    This behaviour can be altered by changing the parameters to the
    ErrorDocuments middleware in your config/middleware.py file.

    """

    def document(self):
        """Render the error document"""
        request = self._py_object.request
        resp = request.environ.get('pylons.original_response')
        content = literal(resp.body) or cgi.escape(request.GET.get('message', ''))
        page = error_document_template % dict(prefix=request.environ.get('SCRIPT_NAME', ''), code=cgi.escape(request.GET.get('code', str(resp.status_int))), message=content)
        return page

    def img(self, id):
        """Serve Pylons' stock images"""
        return self._serve_file(('/').join(['media/img', id]))

    def style(self, id):
        """Serve Pylons' stock stylesheets"""
        return self._serve_file(('/').join(['media/style', id]))

    def _serve_file(self, path):
        """Call Paste's FileApp (a WSGI application) to serve the file
        at the specified path
        """
        request = self._py_object.request
        request.environ['PATH_INFO'] = '/%s' % path
        return PkgResourcesParser('pylons', 'pylons')(request.environ, self.start_response)