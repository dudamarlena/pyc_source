# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.5.0-Power_Macintosh/egg/workspace/plugins/gvim.py
# Compiled at: 2006-04-03 07:48:33
from zope.interface import implements
from workspace.plugins.items_interfaces import IWorkspaceItem
import re, commands, os

class GvimItem(object):
    __module__ = __name__
    implements(IWorkspaceItem)
    name = 'gvim'

    def __init__(self, files, cwd=None):
        self.files = files
        self.cwd = cwd

    @classmethod
    def fromSystem(cls):
        """ return an array of GvimItems """
        pids = commands.getoutput("ps awx | grep Vim | grep -v grep | awk '{print $1}'")
        pids = pids.split()
        return [ cls._fromPID(p) for p in pids ]

    def serialize(self):
        return '%s:%s:%s' % (self.name, self.cwd, (':').join(self.files))

    @classmethod
    def unserialize(cls, s):
        parts = s.split(':')
        return cls(parts[2:], cwd=parts[1])

    def load(self):
        last = os.getcwd()
        os.chdir(self.cwd)
        os.spawnlp(os.P_NOWAIT, 'gvim', 'gvim', *self.files)
        os.chdir(last)

    def __str__(self):
        return self.serialize()

    re_grep_swap = re.compile('\\.swp')
    re_swap = re.compile('.* (/.*/)\\.(.*)\\.swp$')
    re_grep_cwd = re.compile('\\scwd\\s')
    re_cwd = re.compile('.* (\\/.*)*')

    @classmethod
    def _fromPID(cls, pid):
        lsof = commands.getoutput('lsof -p %s' % pid)
        lsof = lsof.split('\n')
        swapFiles = [ cls.re_swap.sub('\\1\\2', x) for x in lsof if cls.re_grep_swap.search(x) ]
        cwd = [ cls.re_cwd.sub('\\1', x) for x in lsof if cls.re_grep_cwd.search(x) ]
        return cls(swapFiles, cwd=cwd[0])