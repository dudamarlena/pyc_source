# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pycrud/controllers/template.py
# Compiled at: 2008-06-20 03:40:59
from pycrud.lib.base import *

class TemplateController(BaseController):

    def index(self):
        return render('/intro.mako')

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
        return render('/blank.mako')
        abort(404)