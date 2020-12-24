# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.5/site-packages/mtstat/plugins/mtstat_rpcd.py
# Compiled at: 2006-12-12 18:59:18
import string

class mtstat_rpcd(mtstat):

    def __init__(self):
        self.name = 'rpc server'
        self.format = ('d', 5, 1000)
        self.open('/proc/net/rpc/nfsd')
        self.vars = ('calls', 'badcalls', 'badauth', 'badclnt', 'xdrcall')
        self.nick = ('call', 'erca', 'erau', 'ercl', 'xdrc')
        self.init(self.vars, 1)

    def extract(self):
        self.fd.seek(0)
        for line in self.fd.readlines():
            l = line.split()
            if not l or l[0] != 'rpc':
                continue
            for (i, name) in enumerate(self.vars):
                self.cn2[name] = long(l[(i + 1)])

        for name in self.vars:
            self.val[name] = (self.cn2[name] - self.cn1[name]) * 1.0 / tick

        if step == op.delay:
            self.cn1.update(self.cn2)


# global string ## Warning: Unused global