# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gazest/controllers/tmpl.py
# Compiled at: 2007-09-26 14:43:59
from gazest.lib.base import *
import routes
from pprint import pprint

class TmplController(BaseController):
    __module__ = __name__

    def index(self):
        return Response('Hello World')

    def foo(self):
        c.title = 'The ultimate Foo'
        pprint(request.environ['pylons.routes_dict'])
        pprint(routes.request_config().mapper_dict)
        pprint(c.routes_dict)
        return render_response('/simple.mak')

    def bar(self):
        return h.redirect_to(controller='/tmpl', action='foo')