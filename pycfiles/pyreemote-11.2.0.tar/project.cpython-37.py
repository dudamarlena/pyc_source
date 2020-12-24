# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/PyreeEngine/project.py
# Compiled at: 2018-04-26 13:08:36
# Size of source mod 2**32: 1277 bytes
from pathlib import Path
import json

class Project:
    """Project"""

    def __init__(self, path: Path):
        self.path = path
        self.data = None
        self.projectName = None
        self.authorName = None
        self.nodes = None
        self.signals = None
        self.entry = None
        self.readJSON(self.path)

    def readJSON(self, path: Path):
        with path.open('r') as (f):
            self.data = json.load(f)
        self.projectName = self.getFromData('projectName')
        self.author = self.getFromData('author')
        self.nodes = self.getFromData('nodes')
        self.signals = self.getSignals()
        self.signals += self.getExecs()
        self.entry = self.getFromData('entry')

    def getFromData(self, key):
        if key in self.data:
            return self.data[key]
        return

    def getSignals(self):
        sigs = self.getFromData('signals')
        for sig in sigs:
            sig['__PYREE__sigtype'] = 'signal'

        return sigs

    def getExecs(self):
        execs = self.getFromData('execSignals')
        for exec in execs:
            exec['__PYREE__sigtype'] = 'exec'

        return execs