# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/linkexchange/turbogears/controllers.py
# Compiled at: 2011-05-13 04:29:10
from cherrypy import request, response, NotFound
from turbogears import expose
from turbogears.controllers import Controller
from linkexchange.turbogears import support

class LinkExchangeHandler(Controller):

    @expose()
    def default(self, *args, **kw):
        if support.platform is None:
            raise NotFound()
        page_request = support.convert_request(request)
        page_response = support.platform.handle_request(page_request)
        response.status = page_response.status
        response.headerMap.update(response.headers)
        return page_response.body