# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/git/lib/python2.5/site-packages/hive/controllers/repos.py
# Compiled at: 2011-07-26 04:32:59
import logging
try:
    import json
except ImportError:
    import simplejson as json

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from hive.lib.base import BaseController, render
from hive.lib.glam.api import Repo
from hive.lib.glam.api import HTTPBadRequest
from hive.lib.glam.api import HTTPNotFound
from hive.lib.glam.api import HTTPConflict
from hive.lib.glam.api import HTTPNotImplemented
from hive.lib.glam.api import HTTPInternalServerError
log = logging.getLogger(__name__)

class ReposController(BaseController):
    """REST Controller styled on the Atom Publishing Protocol"""

    def index(self, format='html'):
        """GET /repos: All items in the collection"""
        try:
            repo_list = Repo.index()
        except HTTPInternalServerError:
            return abort(500)

        repo_list = [ url('repo', id=repo) for repo in repo_list ]
        return json.dumps(repo_list)

    def create(self):
        """POST /repos: Create a new item"""
        params = json.loads(request.body)
        try:
            repo = Repo.create(params['name'])
        except (IndexError, HTTPBadRequest):
            abort(400)
        except HTTPConflict:
            abort(409)
        except HTTPInternalServerError:
            abort(500)

        response.headers['Location'] = url('repo', id=repo)
        response.status_int = 201

    def new(self, format='html'):
        """GET /repos/new: Form to create a new item"""
        abort(501)

    def update(self, id):
        """PUT /repos/id: Update an existing item"""
        abort(501)

    def delete(self, id):
        """DELETE /repos/id: Delete an existing item"""
        try:
            Repo.delete(id)
        except HTTPBadRequest:
            abort(400)
        except HTTPConflict:
            abort(409)

        response.status_int = 200

    def show(self, id, format='html'):
        """GET /repos/id: Show a specific item"""
        abort(501)

    def edit(self, id, format='html'):
        """GET /repos/id/edit: Form to edit an existing item"""
        abort(501)