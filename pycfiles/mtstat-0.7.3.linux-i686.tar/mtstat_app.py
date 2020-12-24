# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.5/site-packages/mtstat/plugins/mtstat_app.py
# Compiled at: 2006-12-12 18:59:17
import string, os
from mtstat.mtstat import mtstat

class mtstat_app(mtstat):

    def __init__(self):
        self.name = 'most expensive'
        self.format = ('s', 18, 0)
        self.nick = ('process', )
        self.vars = self.nick
        self.pid = str(os.getpid())
        self.cn1 = {}
        self.cn2 = {}
        self.val = {}

    def extract(self):
        global string
        max = 0.0
        for pid in os.listdir('/proc/'):
            try:
                int(pid)
            except:
                continue

            if os.path.exists('/proc/%s/stat' % pid):
                if pid == self.pid:
                    continue
                if not self.cn1.has_key(pid):
                    self.cn1[pid] = 0
                l = string.split(open('/proc/%s/stat' % pid).read())
                if len(l) < 15:
                    continue
                self.cn2[pid] = int(l[13]) + int(l[14])
                usage = (self.cn2[pid] - self.cn1[pid]) * 1.0 / self.tick
                if usage > max:
                    max = usage
                    self.val['name'] = l[1][1:-1]
                    self.val['pid'] = pid

        if max == 0.0:
            self.val['process'] = ''
        else:
            if self.val['name'] in ('bash', 'csh', 'ksh', 'perl', 'python', 'sh'):
                l = string.split(open('/proc/%s/cmdline' % self.val['pid']).read(), '\x00')
                if len(l) > 2:
                    self.val['name'] = os.path.basename(l[1])
            self.val['process'] = '%-*s%s%3d' % (self.format[1] - 3, self.val['name'], self.ansi['yellow'], round(max))
        if self.step == self.op.delay:
            self.cn1.update(self.cn2)