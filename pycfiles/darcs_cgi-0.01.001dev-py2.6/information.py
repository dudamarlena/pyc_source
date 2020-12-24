# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/darcscgi/controllers/information.py
# Compiled at: 2009-09-11 13:58:44
import logging
from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from darcscgi.lib.base import BaseController, render
from pylons import app_globals
from darcscgi.lib.helpers import filelisting
log = logging.getLogger(__name__)

class InformationController(BaseController):

    def redirect(self):
        redirect_to(controller='information', action='front')

    def front(self):
        return render('/information/front.mako')

    def repositories(self):
        return render('/information/repositories.mako')

    def quarantine(self):
        c.quarantinedFiles = filelisting(app_globals.globalSettings['quarantine-location'], 0)
        return render('/information/quarantine.mako')