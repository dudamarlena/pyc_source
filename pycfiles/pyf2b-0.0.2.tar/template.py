# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyf/services/controllers/template.py
# Compiled at: 2010-12-14 10:51:23
__doc__ = 'Fallback controller.'
from pyf.services.lib.base import BaseController
from pylons.controllers.util import abort
__all__ = [
 'TemplateController']

class TemplateController(BaseController):
    """
    The fallback controller for pyf.services.
    
    By default, the final controller tried to fulfill the request
    when no other routes match. It may be used to display a template
    when all else fails, e.g.::
    
        def view(self, url):
            return render('/%s' % url)
    
    Or if you're using Mako and want to explicitly send a 404 (Not
    Found) response code when the requested template doesn't exist::
    
        import mako.exceptions
        
        def view(self, url):
            try:
                return render('/%s' % url)
            except mako.exceptions.TopLevelLookupException:
                abort(404)
    
    """

    def view(self, url):
        """Abort the request with a 404 HTTP status code."""
        abort(404)