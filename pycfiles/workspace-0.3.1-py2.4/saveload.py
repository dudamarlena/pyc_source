# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.5.0-Power_Macintosh/egg/workspace/plugins/saveload.py
# Compiled at: 2006-04-03 07:45:41
from zope.interface import implements
from workspace.interfaces import IWorkspaceCommand
from workspace.core import Workspace

class LoadCommand(object):
    __module__ = __name__
    implements(IWorkspaceCommand)

    @classmethod
    def canHandle(cls, cmd):
        return cmd == 'load'

    def handle(self, args):
        ws = Workspace.fromFile('.workspace')
        for (k, v) in ws.data.iteritems():
            for d in v.data:
                d.load()


class SaveCommand(object):
    __module__ = __name__
    implements(IWorkspaceCommand)

    @classmethod
    def canHandle(cls, cmd):
        return cmd == 'save'

    def handle(self, args):
        ws = Workspace.fromSystem()
        f = open('.workspace', 'w')
        f.write(str(ws))
        f.close()