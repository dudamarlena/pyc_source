# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/dvdev/controllers/dashboard.py
# Compiled at: 2009-04-17 21:12:56
import logging
from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from dvdev.lib.base import BaseController
log = logging.getLogger(__name__)

class DashboardController(BaseController):

    def index(self):
        return 'Hello World'