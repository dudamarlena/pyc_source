# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/oebakery/cmd_pull.py
# Compiled at: 2010-01-27 07:14:08
import os, subprocess, socket, sys, string, optparse, oebakery

class PullCommand:

    def __init__(self, config, argv=[]):
        parser = optparse.OptionParser('Usage: oe pull [options] [submodules]*\n\n  Fetch from remote repositories.\n\n  When called without submodules, fetch and merge head of main repository,\n  and checkout the submodule versions stored in main repository.\n\n  When called with a list of submodules, fetch and merge branch heads of\n  specified submodules, overriding the versions stored in main repository.\n  Main repository is not pulled.')
        parser.add_option('-m', '--main', action='store_true', dest='main', default=False, help='pull branch head of main repository')
        parser.add_option('-u', '--update-submodules', action='store_true', dest='update_sub', default=False, help='checkout submodule versions specified in main repository')
        parser.add_option('-r', '--remotes', action='store_true', dest='remotes', default=False, help='fetch updates for remote tracking branches')
        parser.add_option('-s', '--all-submodules', action='store_true', dest='all_sub', default=False, help='pull all submodule branch heads (and main repository)')
        (self.options, self.args) = parser.parse_args(argv)
        if len(argv) == 0:
            self.options.main = True
            self.options.update_sub = True
        if self.options.update_sub and self.options.all_sub:
            print 'Invalid arguments: --update-submodules and --all-submodules'
            return
        if self.options.all_sub and len(self.args) > 0:
            print 'Invalid arguments: --all-submodules and submodule(s)'
            return
        self.config = config

    def run(self):
        if not os.path.exists('.git'):
            print 'Aiee!  This is not a git repository!!'
            return
        else:
            if self.options.remotes:
                self.git_remote_update()
            if self.options.main:
                if not oebakery.call('git pull'):
                    print 'Failed to pull updates to main repository'
            if self.options.update_sub and os.path.exists('.gitmodules'):
                cmd = 'git submodule update --init'
                if '--recursive' in oebakery.call('git help submodule', quiet=True):
                    cmd += ' --recursive'
                if not oebakery.call(cmd):
                    print 'Failed to update git submodules'
                    return
            self.submodules = {}
            for line in oebakery.call('git submodule status', quiet=True).split('\n'):
                if len(line) == 0:
                    continue
                path = line[1:].split()[1]
                prefix = line[0]
                commitid = line[1:].split()[0]
                fetch_url = None
                push_url = None
                branch = None
                remotes = None
                if self.config.has_option('submodules', path):
                    url = self.config.get('submodules', path)
                    url_split = url.split()
                    if len(url_split) < 1 or len(url_split) > 3:
                        print 'Invalid submodule url (%s): %s' % (path, url)
                        return
                    fetch_url = url_split[0]
                    if len(url_split) > 1:
                        branch = url_split[1]
                    if len(url_split) > 2:
                        push_url = url_split[2]
                    section_name = 'remotes "%s"' % path
                    if self.config.has_section(section_name):
                        remotes = self.config.items(section_name)
                self.submodules[path] = {'prefix': prefix, 'commitid': commitid, 
                   'fetch_url': fetch_url, 
                   'push_url': push_url, 
                   'branch': branch, 
                   'remotes': remotes}

            for path in self.submodules.keys():
                if self.options.remotes:
                    self.git_remote_update(path)

            for path in self.submodules.keys():
                if self.options.all_sub or path in self.args:
                    self.git_pull_submodule(path, self.submodules[path]['branch'])

            return

    def git_pull_submodule(self, path=None, branch=None):
        if branch == None:
            branch = ''
        if not oebakery.call('git checkout %s' % branch, dir=path):
            print 'Failed to checkout submodule %s branch %s' % (path, branch)
            return
        else:
            if not oebakery.call('git pull', dir=path):
                print 'Failed to pull submodule %s' % path
                return
            return

    def git_remote_update(self, path=None):
        oebakery.call('git remote update', dir=path)
        remotes = oebakery.call('git remote', dir=path, quiet=True)
        if remotes:
            for remote in remotes.split('\n'):
                if not remote or len(remote) == 0:
                    continue
                if not oebakery.call('git remote prune %s' % remote, dir=path):
                    if path == None:
                        path = 'main repository'
                    print 'Failed to prune remote %s in ' % (remote, path)

        return