# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/frla/controllers/error.py
# Compiled at: 2008-09-22 06:43:32
import cgi, os.path
from paste.urlparser import StaticURLParser
from pylons.middleware import error_document_template, media_path
from frla.lib.base import *

class ErrorController(BaseController):
    """Generates error documents as and when they are required.

    The ErrorDocuments middleware forwards to ErrorController when error
    related status codes are returned from the application.

    This behaviour can be altered by changing the parameters to the
    ErrorDocuments middleware in your config/middleware.py file.
    
    """
    __module__ = __name__

    def document(self):
        """Render the error document"""
        page = error_document_template % dict(prefix=request.environ.get('SCRIPT_NAME', ''), code=cgi.escape(request.params.get('code', '')), message=cgi.escape(request.params.get('message', '')))
        return page

    def img(self, id):
        """Serve Pylons' stock images"""
        return self._serve_file(os.path.join(media_path, 'img'), id)

    def style(self, id):
        """Serve Pylons' stock stylesheets"""
        return self._serve_file(os.path.join(media_path, 'style'), id)

    def _serve_file(self, root, path):
        """Call Paste's FileApp (a WSGI application) to serve the file
        at the specified path
        """
        static = StaticURLParser(root)
        request.environ['PATH_INFO'] = '/%s' % path
        return static(request.environ, self.start_response)