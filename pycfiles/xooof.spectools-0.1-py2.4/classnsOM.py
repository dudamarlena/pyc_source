# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/xooof/spectools/classnsOM.py
# Compiled at: 2008-10-01 10:40:59


class Classns:
    __module__ = __name__

    def __init__(self):
        self.ns = {}
        self.descr = []

    def __repr__(self):
        return 'Classns instance ns = %s' % self.ns

    def getValue(self, key):
        val = self.ns.get(key, None)
        if val is not None:
            return val.package
        return


class Ns:
    __module__ = __name__

    def __init__(self):
        self.type = {}
        self.package = None
        return

    def __repr__(self):
        return "Ns instance type='%s',package='%s',manifest='%s'" % (self.type, self.package, self.manifest)