# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/dvdev/controllers/mercurialgateway.py
# Compiled at: 2009-04-17 23:30:13
import logging
from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from dvdev.lib.base import BaseController, render
from mercurial.hgweb.hgwebdir_mod import hgwebdir
from mercurial import ui, extensions
from pylons import config
from os import path
repositories = [ (path.basename(repo), repo) for repo in config.get('repo').split() ]
parentui = ui.ui()
extensions.load(parentui, 'hgext.highlight', '')
log = logging.getLogger(__name__)

class MercurialgatewayController(BaseController):

    def __call__(self, environ, start_response):
        application = hgwebdir(repositories, parentui)
        output = application(environ, start_response)
        return ('').join([ x for x in output ])