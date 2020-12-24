# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/argonaut/controllers/admin.py
# Compiled at: 2011-02-18 19:15:09
import logging
from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from argonaut.lib.base import BaseController, render
from repoze.what.predicates import not_anonymous, has_permission
from repoze.what.plugins.pylonshq import ActionProtector
log = logging.getLogger(__name__)

class AdminController(BaseController):

    def index(self):
        return 'Index'