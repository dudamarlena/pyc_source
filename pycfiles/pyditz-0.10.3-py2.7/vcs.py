# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ditz/vcs.py
# Compiled at: 2014-12-05 09:06:10
"""
VCS support.
"""
import os
from subprocess import check_call, CalledProcessError
from .config import config
from .logger import log

class VCS(object):

    def __init__(self, rootdir):
        self.cmd = None
        self.addcmd = None
        self.removecmd = None
        for name in config.get('vcs', 'systems').split():
            reponame = config.get(name, 'repo')
            repodir = os.path.join(rootdir, reponame)
            if os.path.isdir(repodir):
                log.info("detected '%s' version control system" % name)
                self.cmd = config.get(name, 'cmd')
                if config.has_option(name, 'add'):
                    self.addcmd = config.get(name, 'add')
                else:
                    self.addcmd = 'add'
                if config.has_option(name, 'remove'):
                    self.removecmd = config.get(name, 'remove')
                else:
                    self.removecmd = 'remove'
                break

        return

    def add(self, path):
        self.runcmd(self.addcmd, path)

    def remove(self, path):
        self.runcmd(self.removecmd, path)

    def runcmd(self, subcmd, path):
        if self.cmd and subcmd:
            cmdline = (' ').join([self.cmd, subcmd])
            args = cmdline.split() + [path]
            log.info("running '%s'" % (' ').join(args))
            try:
                check_call(args)
            except (OSError, CalledProcessError) as err:
                log.info("failed to run '%s': %s" % (args[0], str(err)))