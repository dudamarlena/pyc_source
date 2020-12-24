# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/twiddler/zope2/executor/traverse.py
# Compiled at: 2008-07-24 14:48:01
from Acquisition import Implicit
from Persistence import Persistent
from twiddler import Twiddler
from twiddler.interfaces import IExecutor
from twiddler.zope2.interfaces import IConfigurableComponent
from zope.interface import implements
form = Twiddler('<div>\nPath: <input name="path" value=""/>\n</div>')

class Traverse(Persistent, Implicit):
    implements(IExecutor, IConfigurableComponent)

    def __init__(self, path=''):
        self.path = path

    def __call__(self, *args, **kw):
        return self.unrestrictedTraverse(self.path)(*args, **kw)

    def configureForm(self):
        t = form.clone()
        t['path'].replace(value=self.path)
        return t.render()

    def configure(self, form):
        self.path = form['path']