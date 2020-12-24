# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.5/site-packages/mtstat/plugins/mtstat_freespace.py
# Compiled at: 2006-12-12 18:59:17
import string, os
from mtstat.mtstat import mtstat

class mtstat_freespace(mtstat):

    def __init__(self):
        self.format = ('f', 5, 1024)
        self.open('/etc/mtab')
        self.vars = self.vars()
        self.name = []
        for name in self.vars:
            self.name.append('/' + os.path.basename(name))

        self.nick = ('used', 'free')
        self.init(self.vars + ['total'], 2)

    def vars(self):
        global string
        ret = []
        if self.fd:
            self.fd.seek(0)
            for line in self.fd.readlines():
                l = string.split(line)
                if len(l) < 6:
                    continue
                if l[2] in ('binfmt_misc', 'devpts', 'iso9660', 'none', 'proc', 'sysfs',
                            'usbfs'):
                    continue
                if l[0] in ('devpts', 'none', 'proc', 'sunrpc', 'usbfs'):
                    continue
                name = l[1]
                res = os.statvfs(name)
                if res[0] == 0:
                    continue
                ret.append(name)

        return ret

    def extract(self):
        self.val['total'] = (0, 0)
        for name in self.vars:
            res = os.statvfs(name)
            self.val[name] = ((float(res.f_blocks) - float(res.f_bavail)) * long(res.f_frsize), float(res.f_bavail) * float(res.f_frsize))
            self.val['total'] = (self.val['total'][0] + self.val[name][0], self.val['total'][1] + self.val[name][1])