# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyf/services/controllers/error.py
# Compiled at: 2010-05-21 08:57:50
"""Error controller"""
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