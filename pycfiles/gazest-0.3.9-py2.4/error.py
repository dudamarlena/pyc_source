# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gazest/controllers/error.py
# Compiled at: 2007-10-20 15:16:47
import os.path, paste.fileapp
from pylons.middleware import error_document_template, media_path
from gazest.lib.base import *
from pprint import pprint

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
        c.code = request.params.get('code', '')
        c.title = '%s Error' % c.code
        c.message = request.params.get('message', '')
        return render('/error.mako')