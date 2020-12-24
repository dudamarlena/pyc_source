# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.5/site-packages/mysql/mtstat/mysqlbase.py
# Compiled at: 2007-08-01 13:56:37
from mtstat.mtstat import mtstat, cprint, char, cprintlist
import types, MySQLdb

class mysqlbase(mtstat):
    db = MySQLdb.Connect(port=0, read_default_group='mtstat')
    server_info = db.get_server_info()
    if server_info[0] == '4':
        q = 'show status'
    else:
        q = 'show global status'
    data = {}
    data_last = {}
    val = {}
    mysqlvars = [
     (
      'Questions', ('diff', ('d', 7, 1000), 'quest'))]

    def __init__(self):
        self.formats = {}
        for (k, v) in self.mysqlvars:
            self.formats[k] = v[1]

        self.format = ('d', 7, 1000)
        self.vars = [ f[0] for f in self.mysqlvars ]
        self.name = 'mysql'
        self.nick = [ f[1][2].lower() for f in self.mysqlvars ]
        self.init(self.vars, 1)

    def get_diff(self, key):
        val_now = int(self.data[key])
        try:
            val_then = int(self.data_last[key])
        except KeyError:
            return 0

        if val_then == 0:
            return 0
        return val_now - val_then

    def extract(self):
        c = self.db.cursor()
        c.execute(self.q)
        for (key, val) in c.fetchall():
            self.data[key] = val

        foo = "\n        queries_now=int(data['Questions'])\n        if (self.queries_last==0):\n            self.queries=0\n        else:\n            self.queries=queries_now-self.queries_last\n        self.queries_last=queries_now\n        #c.execute(self.u)\n        uptime_now=int(data['Uptime'])\n        if (self.uptime_last==0):\n            self.uptime=1\n        else:\n            self.uptime=uptime_now-self.uptime_last "
        for f in self.vars:
            tup = []
            for x in self.mysqlvars:
                if x[0] == f:
                    tup = x[1]

            if tup[0] == 'diff':
                self.val[f] = self.get_diff(f)
            else:
                self.val[f] = int(self.data[f])

        self.data_last = self.data.copy()

    def show(self):
        """Display stat results"""
        line = ''
        for (i, name) in enumerate(self.vars):
            if isinstance(self.val[name], types.TupleType) or isinstance(self.val[name], types.ListType):
                line = line + cprintlist(self.val[name], self.formats[name])
                sep = ansi['default'] + char['colon']
            else:
                line = line + cprint(self.val[name], self.formats[name])
                sep = char['space']
            if i + 1 != len(self.vars):
                line = line + sep

        return line