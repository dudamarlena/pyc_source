# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: e:\nmdev\src\branches\loyalty\evasion-web\evasion\web\controllers\root.py
# Compiled at: 2010-05-18 09:51:54
import logging
from routes import url_for
from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from evasion.web.lib.base import BaseController, render

class RootController(BaseController):

    def __init__(self, *args, **kw):
        BaseController.__init__(self, *args, **kw)
        self.log = logging.getLogger('evasion.web.controllers.root.RootController')

    def index(self):
        return render('root.mako')