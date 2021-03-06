# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.5.0-Power_Macintosh/egg/workspace/core.py
# Compiled at: 2006-04-03 07:45:55
import re, os, sprinkles
from workspace.interfaces import IWorkspaceSection, IWorkspaceCommand

class Workspace:
    __module__ = __name__
    data = {}
    re_sectionheader = re.compile('^\\[(\\w+)\\]$')
    sections = []

    def __init__(self):
        self.sections = sprinkles.fromPackage('workspace.plugins', IWorkspaceSection.implementedBy)

    @classmethod
    def fromFile(cls, f):
        if type(f) is type(''):
            f = open(f)
        self = cls()
        currentSection = None
        for l in f:
            l = l.strip()
            if currentSection is None:
                sec = cls.re_sectionheader.match(l)
                if not sec:
                    continue
                sec = sec.group(1)
                currentSection = self.getSection(sec)
                if currentSection.name not in self.data:
                    self.data[currentSection.name] = currentSection
                continue
            if len(l) < 1:
                currentSection = None
                continue
            currentSection.append(currentSection.getItem(l))

        return self

    @classmethod
    def fromSystem(cls):
        self = cls()
        for s in self.sections:
            d = s.fromSystem()
            self.data[d.name] = d

        return self

    def serialize(self):
        o = [
         'Saved workspace', '']
        for (s, v) in self.data.iteritems():
            o.append('[%s]' % s)
            for d in v.data:
                o.append(str(d))

        return ('\n').join(o)

    def __str__(self):
        return self.serialize()

    def getSection(self, sec):
        for s in self.sections:
            if s.canHandle(sec):
                return s()

        return


class CLI:
    __module__ = __name__
    commands = []

    def __init__(self):
        self.commands = sprinkles.fromPackage('workspace.plugins', IWorkspaceCommand.implementedBy)

    def handle(self, args):
        if len(args) < 2:
            raise Exception('come on, try harder than that')
        cmd = args[1]
        for h in self.commands:
            if h.canHandle(cmd):
                c = h()
                return c.handle(args[2:])

        raise Exception("couldn't find anything like that")