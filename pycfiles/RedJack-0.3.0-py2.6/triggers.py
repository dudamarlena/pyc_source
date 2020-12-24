# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/redjack/triggers.py
# Compiled at: 2011-01-23 04:37:33
import os, pickle, logging, re, time
from mako.template import Template
from killableprocess import Popen, PIPE, STDOUT
try:
    import git
except ImportError:
    git = None

log = logging.getLogger('rj.triggers')
log = logging

class Trigger(object):

    def __init__(self, project, trigger_type, name, trigger):
        self.project = project
        self.trigger_type = trigger_type
        self.name = name
        self._load_state()

    def prepare(self, project):
        pass

    def get_changes(self):
        raise Exception('not implemented')

    def _load_state(self):
        self.state = self.project.load_trigger_state(self.name)

    def _save_state(self):
        self.project.save_trigger_state(self.name, self.state)


class GitRepo(Trigger):

    def __init__(self, project, trigger_type, name, repo_info):
        Trigger.__init__(self, project, trigger_type, name, repo_info)
        if git == None:
            raise Exception('missing git')
        self.url = repo_info['url']
        self.directory = repo_info['directory']
        return

    def prepare(self):
        log.info('Preparing Git repository for project %s' % self.project.name)
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        elif not os.path.isdir(self.directory):
            raise Exception('%s should be a directory' % self.directory)
        if not os.path.exists(os.path.join(self.directory, '.git')):
            log.info('Cloning Git repo')
            g = git.cmd.Git(self.directory)
            g.clone(self.url, self.directory)
        self.repo = git.Repo(self.directory)
        self._update_state()
        log.info('Preparation completed')

    def _update_state(self):
        tip = self.repo.heads[0].commit.id
        self.state['tip'] = tip
        self._save_state()

    def _parse_changes(self, changes):
        changesets = []
        for (rev, change) in changes:
            author = change.author.name
            email = change.author.email
            date = time.strftime('%Y.%m.%d<br/>%H:%M', change.authored_date)
            files = change.stats.files.keys()
            c = {'revision': rev, 'author': author, 'email': email, 'date': date, 'comment': change.message, 'files': files}
            changesets.append(c)

        return changesets

    def _get_changes(self):
        self.repo.git.pull()
        prev_tip = self.state['tip']
        tip = self.repo.heads[0].commit
        changes = []
        for r in self.repo.commits_between(prev_tip, tip):
            c = self.repo.commit(r)
            changes.append((r, c))

        log.info('%s: repo %s changes %d' % (self.project.name, self.url, len(changes)))
        if len(changes) > 0:
            self._update_state()
            return self._parse_changes(changes)
        return []

    def get_changes(self):
        changesets = []
        try:
            changesets = self._get_changes()
        except Exception, e:
            log.exception(e)

        return {'info': 'Git repository %s' % self.url, 'changesets': changesets}


class MercurialRepo(Trigger):

    def __init__(self, project, trigger_type, name, repo_info):
        Trigger.__init__(self, project, trigger_type, name, repo_info)
        self.url = repo_info['url']
        self.directory = repo_info['directory']

    def prepare(self):
        log.info('Preparing Mercurial repository for project %s' % self.project.name)
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        elif not os.path.isdir(self.directory):
            raise Exception('%s should be a directory' % self.directory)
        if not os.path.exists(os.path.join(self.directory, '.hg')):
            log.info('Cloning Mercurial repo')
            cmd = 'hg -y clone %s %s' % (self.url, self.directory)
            p = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT)
            p.wait()
        self._update_state()
        log.info('Preparation completed')

    def _get_tip(self):
        cmd = 'hg -y log -r tip --template "{rev}:{node}"'
        p = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT, cwd=self.directory)
        p.wait()
        tip_rev = p.stdout.read().strip()
        return tip_rev

    def _update_state(self):
        tip_rev = self._get_tip()
        self.state['tip'] = tip_rev
        self._save_state()

    def _get_changes(self):
        log.info('pulling repo')
        cmd = 'hg -y pull -u'
        p = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT, cwd=self.directory)
        (out, err) = p.communicate()
        log.info('hg pull: %s' % out)
        old_tip = self.state['tip']
        new_tip = self._get_tip()
        log.info('old tip: %s,  new tip %s' % (old_tip, new_tip))
        sep = '#@##@##@##@##@##@##@#'
        cmd = 'hg -y log '
        cmd += '--template "{rev}:{node}\\n{author|user}\\n{author|email}\\n{date|isodate}\\n{files}\\n{desc}\\n%s\\n" ' % sep
        cmd += '-r %s:%s' % (old_tip, new_tip)
        p = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT, cwd=self.directory)
        (text, err) = p.communicate()
        text = text.strip()
        entries = text.split(sep)[:-1]
        changes = []
        for e in entries:
            log.debug(e)
            e = e.split('\n')
            rev = e[0]
            author = e[1]
            email = e[2]
            date = e[3]
            files = e[4]
            comment = ('\n').join(e[5:])
            if rev == old_tip:
                continue
            log.info('%s, %s, %s, %s' % (rev, author, date, comment))
            c = {'revision': rev, 'author': author, 'email': email, 'date': date, 'comment': comment, 'branch': '[branch-TODO]', 
               'files': files}
            changes.append(c)

        log.info('%s: repo %s changes %d' % (self.project.name, self.url, len(changes)))
        if len(changes) > 0:
            self._update_state()
            return changes
        return []

    def get_changes(self):
        changesets = []
        try:
            changesets = self._get_changes()
        except Exception, e:
            log.exception(e)

        return {'info': 'Mercurial repository %s' % self.url, 'changesets': changesets}


trigger_classes = {'git': GitRepo, 'mercurial': MercurialRepo}