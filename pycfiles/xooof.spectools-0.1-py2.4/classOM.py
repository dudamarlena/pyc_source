# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/xooof/spectools/classOM.py
# Compiled at: 2008-10-01 10:40:59
from commonOM import Descr
from interfaceOM import Event
from interfaceOM import Reply

class Klass:
    __module__ = __name__

    def __init__(self):
        self.specFile = None
        self.name = None
        self.descr = []
        self.defaultinterface = None
        self.classmethods = []
        self.fsm = None
        self.classNs = None
        self.doc = []
        e = Event()
        e.name = 'getClassInfo'
        e.visibility = 'public'
        e.descr = [Descr()]
        e.descr[0].language = 'en'
        e.descr[0].description = 'Obtain information about the class'
        e.rply = Reply()
        e.rply.className = ('http://xmlcatalog/catalog/spectools/class/classinfo',
                            'MClass')
        e.rply.list = 1
        e.rply.optional = 0
        e.rply.validated = 1
        self.classmethods.append(e)
        return

    def __repr__(self):
        return "Klass instance name='%s'" % self.name[1]

    def validate(self):
        """TODO
           - validate name of class [A-Za-z][A-Za-z0-9]*
           - in methods : rqst and rply exists and are valid
           - fsm => consitency of fsm
        """
        raise RuntimeError('not implemented')

    def getAllEvents(self):
        r = self.classmethods
        if self.defaultinterface:
            r = r + self.defaultinterface.getAllEvents()
        return r