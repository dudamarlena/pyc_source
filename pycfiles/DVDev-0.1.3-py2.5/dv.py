# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/dvdev/controllers/dv.py
# Compiled at: 2009-04-17 21:13:04
import logging
from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect
from dvdev.lib.base import BaseController, render
from pygments import highlight
from pygments.lexers import DiffLexer
from pygments.formatters import HtmlFormatter
from mercurial import commands, ui, hg, patch, cmdutil
from re import compile
from os import path, unlink
from filesafe import Chroot
from pylons.decorators import rest
import yamltrak
DIFF_FILE = compile('diff -r [0-91-f]+ (.*)$')
log = logging.getLogger(__name__)

class DvController(BaseController):

    def index(self):
        """Go through all of the repositories and list any uncommitted changes"""
        c.css = '<style type="text/css">%s</style>' % HtmlFormatter().get_style_defs('.highlight')
        c.diffs = self._get_diffs()
        return render('dv/commit.html')

    def _get_diffs(self, repository=None, filepath=None):
        diffs = []
        for (repo, root) in self.repositories:
            if repository and root != repository:
                continue
            (node1, node2) = cmdutil.revpair(repo, None)
            match = cmdutil.match(repo, (), {})
            repodiffs = []
            for diff in patch.diff(repo, node1, node2, match=match, opts=patch.diffopts(self.ui)):
                diffheader = diff.split('\n')[0]
                filename = DIFF_FILE.match(diffheader).groups()[0]
                if filepath and filepath == filename:
                    return {'repository': root, 'filename': filename, 'diff': highlight(diff, DiffLexer(), HtmlFormatter())}
                repodiffs.append({'repository': root, 'filename': filename, 
                   'diff': highlight(diff, DiffLexer(), HtmlFormatter())})

            try:
                issues = yamltrak.issues([repo.root])[root]
            except KeyError:
                issues = {}

            for diff in repodiffs:
                relatedissues = yamltrak.relatedissues(repo.root, filename=diff['filename'], ids=issues.keys())
                related = {}
                for issue in relatedissues:
                    related[issue] = {'repo': root, 'title': issues[issue]['title']}

                diff['relatedissues'] = related

            diffs += repodiffs

        if filepath:
            raise LookupError
        return diffs

    @rest.dispatch_on(GET='index')
    def commit(self):
        """Use the list of files given by the user to commit to the repository"""
        url = request.environ['routes.url']
        message = request.params['message']
        if not message:
            redirect(url.current(action='index'))
        for (repo, root) in self.repositories:
            if root not in request.params:
                continue
            repochroot = Chroot(repo.root)
            try:
                files = (repochroot(path.join(repo.root, file)) for file in request.params.getall(root))
            except IOError:
                error = 'Bad Filename'
                redirect(url(controller='dv', action='index', error=error))

            self.ui.pushbuffer()
            commands.commit(self.ui, repo, message=message, logfile=None, *files)
            output = self.ui.popbuffer()

        redirect(url.current(action='index'))
        return

    @rest.dispatch_on(POST='_revert_confirmed')
    def revert(self, repository, filepath):
        url = request.environ['routes.url']
        if not repository or not filepath:
            redirect(url.current(action='index'))
        found = False
        for (repoobj, root) in self.repositories:
            if root == repository:
                found = True
                repo = repoobj
                break

        if not found:
            redirect(url.current(action='index'))
        repochroot = Chroot(repo.root)
        try:
            fullfilepath = repochroot(path.join(repo.root, filepath))
        except IOError:
            error = 'Bad Filename'
            redirect(url.current(action='index', error=error))

        statusmapper = dict(enumerate(['modified', 'added', 'removed', 'deleted', 'unknown', 'ignored', 'clean']))
        c.added = False
        statuses = repo.status()
        for (index, status) in statusmapper.iteritems():
            if filepath in statuses[index]:
                c.status = status
                if status == 'added':
                    c.added = True
                break

        c.filepath = filepath
        try:
            c.diff = self._get_diffs(repository=repository, filepath=filepath)
        except LookupError:
            redirect(url.current(action='index', error='File not in repository'))

        c.css = '<style type="text/css">%s</style>' % HtmlFormatter().get_style_defs('.highlight')
        return render('dv/revert.html')

    def _revert_confirmed(self, repository, filepath):
        """Revert the given file to its pristine state."""
        url = request.environ['routes.url']
        if not repository or not filepath:
            redirect(url.current(action='index'))
        found = False
        for (repoobj, root) in self.repositories:
            if root == repository:
                found = True
                repo = repoobj
                break

        if not found:
            redirect(url.current(action='index'))
        repochroot = Chroot(repo.root)
        try:
            fullfilepath = repochroot(path.join(repo.root, filepath))
        except IOError:
            error = 'Bad Filename'
            redirect(url.current(action='index', error=error))

        statusmapper = dict(enumerate(['modified', 'added', 'removed', 'deleted', 'unknown', 'ignored', 'clean']))
        statuses = repo.status()
        for (index, status) in statusmapper.iteritems():
            if status not in ('modified', 'added', 'removed', 'deleted'):
                if filepath in statuses[index]:
                    c.status = status
                    c.error = "Can't revert this file"
                    return render('dv/revert.html')
                continue
            if filepath in statuses[index]:
                commands.revert(self.ui, repo, fullfilepath, rev='tip', date=None)
                if status == 'added' and request.params.get('remove'):
                    unlink(fullfilepath)
                redirect(url(repository=repository, controller='dv', action='index'))

        c.error = 'Not found'
        return render('dv/revert.html')