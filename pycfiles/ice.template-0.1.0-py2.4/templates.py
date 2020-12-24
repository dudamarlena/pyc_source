# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ice/template/templates.py
# Compiled at: 2009-05-04 14:30:04
from Cheetah.Template import Template
from BTrees.OOBTree import OOBTree
from persistent import Persistent
from zope.component import getAdapter, getAdapters, getUtilitiesFor
from zope.interface import implements
from zope.location import ILocation
from interfaces import ITemplates, ITemplate

def getUtilityName(context):
    for (name, utility) in getUtilitiesFor(ITemplates, context):
        if utility == context:
            return name


class Templates(Persistent):
    __module__ = __name__
    implements(ITemplates, ILocation)
    __parent__ = __name__ = None

    def __init__(self):
        self._templates = OOBTree()
        super(Templates, self).__init__()

    def getTemplate(self, name):
        return self._templates.get(name) or self.resetTemplate(name)

    def setTemplate(self, name, text):
        self._templates[name] = text

    def compileTemplate(self, name, data={}):
        return str(Template(self.getTemplate(name), searchList=[data]))

    def getVariables(self, name):
        return getAdapter(self, ITemplate, name=name).variables

    def resetTemplate(self, name):
        result = self._templates[name] = self.getSource(name)
        return result

    def getSource(self, name):
        tmpl = getAdapter(self, ITemplate, name=name)
        if tmpl.storage == getUtilityName(self):
            return tmpl.source
        raise KeyError

    def getAllTemplates(self):
        uname = getUtilityName(self)
        for (name, adapter) in getAdapters([self], ITemplate):
            if adapter.storage == uname:
                yield (
                 name, adapter)