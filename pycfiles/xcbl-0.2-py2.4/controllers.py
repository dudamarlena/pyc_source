# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/xcbl/controllers.py
# Compiled at: 2007-05-09 14:22:33
import logging, cherrypy, turbogears
from turbogears import controllers, expose, validate, redirect
from xcbl import json
log = logging.getLogger('xcbl.controllers')

class Root(controllers.RootController):
    __module__ = __name__

    @expose(template='xcbl.templates.welcome')
    def index(self):
        import time
        log.debug('Happy TurboGears Controller Responding For Duty')
        return dict(now=time.ctime())