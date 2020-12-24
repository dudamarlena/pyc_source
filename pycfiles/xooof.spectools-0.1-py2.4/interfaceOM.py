# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/xooof/spectools/interfaceOM.py
# Compiled at: 2008-10-01 10:40:59


class Interface:
    __module__ = __name__

    def __init__(self, name):
        self.name = name
        self.specFile = None
        self.descr = []
        self.doc = []
        self.extends = []
        self.methods = []
        self.interfaceNs = None
        return

    def getAllEvents(self):
        r = self.methods
        for interface in self.extends:
            r = r + interface.getAllEvents()

        return r

    def getAllInterfaces(self):
        r = self.extends
        for interface in self.extends:
            r = r + interface.getAllInterfaces()

        return r

    def getInterfaceForEvent(self, event):
        if event in self.methods:
            return self
        for interface in self.extends:
            itf = interface.getInterfaceForEvent(event)
            if itf is not None:
                return itf

        return


class Event:
    __module__ = __name__
    VISIBILITY_PUBLIC = 'public'
    VISIBILITY_PRIVATE = 'private'
    SPECIAL_CONSTRUCTOR = 'constructor'
    SPECIAL_DESTRUCTOR = 'destructor'

    def __init__(self):
        self.name = None
        self.visibility = None
        self.special = None
        self.rqst = None
        self.rply = None
        self.descr = []
        self.doc = []
        self.isInstanceMethod = None
        return

    def __repr__(self):
        return "Event instance : name='%s',visibility='%s',special='%s'" % (self.name, self.visibility, self.special)


class Request:
    __module__ = __name__

    def __init__(self):
        self.className = None
        self.classPath = None
        self.isList = None
        self.isOptional = None
        self.isValidated = None
        self.doc = []
        return

    def __repr__(self):
        return "Request Instance : class='%s'" % (self.className,)


class Reply:
    __module__ = __name__

    def __init__(self):
        self.className = None
        self.classPath = None
        self.isList = None
        self.isOptional = None
        self.isValidated = None
        self.doc = []
        return

    def __repr__(self):
        return "Reply Instance : class='%s'" % (self.className,)