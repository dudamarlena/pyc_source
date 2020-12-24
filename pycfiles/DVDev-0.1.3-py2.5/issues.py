# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/dvdev/controllers/issues.py
# Compiled at: 2009-04-19 13:53:21
import logging
from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to, redirect
from pylons.decorators import rest
from pylons.decorators import jsonify
from dvdev.lib.base import BaseController, render
import yamltrak
from pylons import config
from os import path
repositories = dict(((repo.split(path.sep)[(-1)], repo) for repo in config.get('repo').split()))
log = logging.getLogger(__name__)

class IssuesController(BaseController):
    """REST Controller styled on the Atom Publishing Protocol"""

    def index(self, repository, format='html'):
        """GET /issues: All items in the collection"""
        allissues = yamltrak.issues(repositories.values(), 'issues')
        c.issues = {}
        for repo in repositories:
            c.issues[repo] = {}
            issuedb = allissues.get(repo, {})
            for (issueid, issue) in issuedb.iteritems():
                group = issue.get('group', 'unfiled')
                c.issues[repo][group] = c.issues[repo].get(group, {})
                c.issues[repo][group][issueid] = issue

            if repo not in allissues:
                c.issues[repo] = None

        return render('issues/index.html')

    def create(self, repository):
        """POST /issues: Create a new item"""
        pass

    @rest.dispatch_on(POST='_add_new')
    def new(self, repository, format='html'):
        """GET /issues/new: Form to create a new item"""
        skeleton = yamltrak.issue(repositories[repository], 'issues', 'newticket', detail=False)
        if not skeleton:
            skeleton = yamltrak.issue(repositories[repository], 'issues', 'skeleton', detail=False)
        c.skeleton = skeleton[0]['data']
        keys = c.skeleton.keys()
        orderedkeys = []
        if 'title' in keys:
            keys.remove('title')
            orderedkeys.append('title')
        if 'description' in keys:
            keys.remove('description')
            orderedkeys.append('description')
        orderedkeys += keys
        c.orderedkeys = orderedkeys
        return render('issues/add.html')

    def _add_new(self, repository, format='html'):
        issue = {}
        issue['title'] = request.params.get('title')
        issue['description'] = request.params.get('description')
        issue['estimate'] = request.params.get('estimate')
        if not issue['title'] or not issue['description'] or 'estimate' not in request.params:
            c.issue = issue
            return render('issues/add.html')
        issueid = yamltrak.new(repositories[repository], issue)
        url = request.environ['routes.url']
        redirect(url.current(repository=repository, id=issueid, action='show'))

    def update(self, repository, id):
        """PUT /issues/id: Update an existing item"""
        pass

    def delete(self, repository, id):
        """DELETE /issues/id: Delete an existing item"""
        pass

    def close(self, repository, id):
        """POST /issues/id: Show a specific item"""
        if yamltrak.close(repositories[repository], id):
            redirect_to('/issues')
        redirect_to(action='show', id=id)

    def show(self, repository, id, format='html'):
        """GET /repository/issues/id: Show a specific item"""
        c.id = id
        issue = yamltrak.issue(repositories[repository], 'issues', id)
        skeleton = yamltrak.issue(repositories[repository], 'issues', 'skeleton', detail=False)
        c.issue = issue[0]['data']
        c.skeleton = skeleton[0]['data']
        c.uncommitted_diff = issue[0].get('diff')
        c.versions = issue[1:]
        return render('issues/issue.html')

    def initialize(self, repository, format='html'):
        """GET /issues/id/edit: Form to edit an existing item"""
        url = request.environ['routes.url']
        yamltrak.dbinit(repository)
        return redirect(url(controller='issues', repository=repository, action='index'))

    @rest.dispatch_on(GET='show')
    def edit(self, repository, id, format='html'):
        """GET /issues/id/edit: Form to edit an existing item"""
        oldissue = yamltrak.issue(repositories[repository], 'issues', id, detail=False)
        skeleton = yamltrak.issue(repositories[repository], 'issues', 'skeleton', detail=False)
        newissue = {}
        for key in skeleton[0]['data']:
            if key in oldissue[0]['data']:
                newissue[key] = oldissue[0]['data'][key]
            else:
                newissue[key] = skeleton[0]['data'][key]
            if key in request.params:
                newissue[key] = request.params[key]

        yamltrak.edit_issue(repositories[repository], 'issues', newissue, id)
        redirect_to(action='show', id=id)

    def burndown(self, repository, id):
        c.group = id
        c.groupdata = yamltrak.burndown(repository, id)
        maxtime = None
        maxwork = 0
        worstslope = 0
        for (timestamp, workleft) in c.groupdata:
            if workleft >= maxwork:
                maxtime, maxwork = timestamp, workleft

        for (timestamp, workleft) in c.groupdata:
            try:
                if (timestamp - maxtime) / (workleft - maxwork) < worstslope:
                    worstslope = (timestamp - maxtime) / (workleft - maxwork)
            except ZeroDivisionError:
                pass

        c.maxtime = maxtime
        c.maxwork = maxwork
        c.worsttime = -worstslope * maxwork + maxtime
        return render('issues/burndown.html')