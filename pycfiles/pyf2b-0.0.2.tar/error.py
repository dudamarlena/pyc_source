# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyf/services/controllers/error.py
# Compiled at: 2010-05-21 08:57:50
__doc__ = 'Error controller'
from tg import request, expose
__all__ = [
 'ErrorController']

class ErrorController(object):
    """
    Generates error documents as and when they are required.

    The ErrorDocuments middleware forwards to ErrorController when error
    related status codes are returned from the application.

    This behaviour can be altered by changing the parameters to the
    ErrorDocuments middleware in your config/middleware.py file.
    
    """

    @expose('pyf.services.templates.error')
    def document(self, *args, **kwargs):
        """Render the error document"""
        resp = request.environ.get('pylons.original_response')
        default_message = "<p>We're sorry but we weren't able to process  this request.</p>"
        values = dict(prefix=request.environ.get('SCRIPT_NAME', ''), code=request.params.get('code', resp.status_int), message=request.params.get('message', default_message))
        return values