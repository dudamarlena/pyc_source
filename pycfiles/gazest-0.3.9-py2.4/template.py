# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gazest/controllers/template.py
# Compiled at: 2007-09-26 14:43:59
from gazest.lib.base import *

class TemplateController(BaseController):
    __module__ = __name__

    def view(self, url):
        """By default, the final controller tried to fulfill the request
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

        By default this controller aborts the request with a 404 (Not
        Found)
        """
        abort(404)