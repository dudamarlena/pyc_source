# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysvnmanager/controllers/template.py
# Compiled at: 2010-08-08 03:18:44
from pysvnmanager.lib.base import *
from pylons.i18n import _, ungettext, N_

class TemplateController(BaseController):

    def __init__(self):
        if hasattr(g, 'catch_e') and g.catch_e:
            self.catch_e = g.catch_e[:]
            g.catch_e = None
        else:
            self.catch_e = None
        return

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

    def show_e(self):
        if self.catch_e:
            c.catch_e = self.catch_e
        else:
            c.catch_e = [
             '', '']
        return render('/catch_e.mako')