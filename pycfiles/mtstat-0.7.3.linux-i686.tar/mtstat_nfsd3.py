# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.5/site-packages/mtstat/plugins/mtstat_nfsd3.py
# Compiled at: 2006-12-12 18:59:17
import string

class mtstat_nfsd3(mtstat):

    def __init__(self):
        self.name = 'nfs3 server'
        self.format = ('d', 5, 1000)
        self.open('/proc/net/rpc/nfsd')
        self.vars = ('read', 'write', 'readdir', 'inode', 'filesystem', 'commit')
        self.nick = ('read', 'writ', 'rdir', 'inod', 'fs', 'cmmt')
        self.init(self.vars, 1)
        info(1, 'Module mtstat_nfsd3 is still experimental.')

    def extract(self):
        self.fd.seek(0)
        for line in self.fd.readlines():
            l = line.split()
            if not l or l[0] != 'proc3':
                continue
            self.cn2['read'] = long(l[8])
            self.cn2['write'] = long(l[9])
            self.cn2['readdir'] = long(l[18]) + long(l[19])
            self.cn2['inode'] = long(l[3]) + long(l[4]) + long(l[5]) + long(l[6]) + long(l[7]) + long(l[10]) + long(l[11]) + long(l[12]) + long(l[13]) + long(l[14]) + long(l[15]) + long(l[16]) + long(l[17])
            self.cn2['filesystem'] = long(l[20]) + long(l[21]) + long(l[22])
            self.cn2['commit'] = long(l[23])

        for name in self.vars:
            self.val[name] = (self.cn2[name] - self.cn1[name]) * 1.0 / tick

        if step == op.delay:
            self.cn1.update(self.cn2)


# global string ## Warning: Unused global