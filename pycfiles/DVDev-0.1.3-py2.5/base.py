# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/dvdev/lib/base.py
# Compiled at: 2009-04-17 21:12:17
"""The base Controller API

Provides the BaseController class for subclassing.
"""
from pylons.controllers import WSGIController
from pylons.templating import render_genshi as render
from pylons import request, response, session, tmpl_context as c
from pylons import config
from mercurial import commands, ui, hg
from filesafe import get_sanitized_path
from os import makedirs, path
repositories = config.get('repo').split()

class BaseController(WSGIController):

    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        self.ui = ui.ui()
        identity = request.environ.get('repoze.who.identity')
        if identity:
            self.user = identity.get('repoze.who.userid')
            workspace = self.__ensure_repositories()
            self.repositories = [ (hg.repository(self.ui, path.join(workspace, path.basename(repo))), path.basename(repo)) for repo in repositories ]
        else:
            self.repositories = [ (hg.repository(self.ui, repo), path.basename(repo)) for repo in repositories ]
        c.uncommitted = ''
        for (repo, name) in self.repositories:
            self.ui.pushbuffer()
            commands.diff(self.ui, repo)
            test = self.ui.popbuffer()
            if test:
                c.uncommitted = 'uncommitted'
                break

        c.project = environ['pylons.routes_dict'].get('repository')
        return WSGIController.__call__(self, environ, start_response)

    def __ensure_repositories(self):
        workspace = get_sanitized_path(config.get('workspace').split('/') + [self.user])
        try:
            makedirs(workspace)
        except OSError:
            pass

        for repo in repositories:
            if not path.exists(path.join(workspace, path.basename(repo))):
                commands.clone(self.ui, repo, path.join(workspace, path.basename(repo)))

        self.workspace = workspace
        return workspace