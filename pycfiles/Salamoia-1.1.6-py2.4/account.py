# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/salamoia/frontends/account.py
# Compiled at: 2007-12-02 16:26:54
import connection

class User:
    __module__ = __name__
    _group = None

    def __init__(self, dict):
        self.uid = dict['uid'][0]
        self.uidNumber = dict['uidNumber'][0]
        self.gidNumber = dict['gidNumber'][0]
        self.home = dict['homeDirectory'][0]

    def __repr__(self):
        return '<user: %s:%s %s>' % (self.uid, self.group().name, self.home)

    def group(self):
        if not self._group:
            self._group = connection.DefaultConnection().groupByGid(self.gidNumber)
        return self._group


class Group:
    __module__ = __name__

    def __init__(self, dict):
        self.name = dict['cn'][0]

    def __repr__(self):
        return '<group: %s>' % self.name