# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.5/site-packages/mtstat/plugins/mtstat_gpfsop.py
# Compiled at: 2006-12-12 18:59:17
import string, select

class mtstat_gpfsop(mtstat):

    def __init__(self):
        self.name = 'gpfs file operations'
        self.format = ('d', 5, 1000)
        self.vars = ('_oc_', '_cc_', '_rdc_', '_wc_', '_dir_', '_iu_')
        self.nick = ('open', 'clos', 'read', 'writ', 'rdir', 'inod')
        self.init(self.vars, 1)

    def check(self):
        if os.access('/usr/lpp/mmfs/bin/mmpmon', os.X_OK):
            try:
                (self.stdin, self.stdout, self.stderr) = dpopen('/usr/lpp/mmfs/bin/mmpmon -p -s')
                self.stdin.write('reset\n')
                readpipe(self.stdout)
            except IOError:
                raise Exception, 'Module can not interface with gpfs mmpmon binary'
            else:
                return True
        raise Exception, 'Module needs gpfs mmpmon binary'

    def extract(self):
        try:
            self.stdin.write('io_s\n')
            for line in readpipe(self.stdout):
                if not line:
                    continue
                l = line.split()
                for name in self.vars:
                    self.cn2[name] = long(l[(l.index(name) + 1)])

            for name in self.vars:
                self.val[name] = (self.cn2[name] - self.cn1[name]) * 1.0 / tick

        except IOError, e:
            for name in self.vars:
                self.val[name] = -1

        except Exception, e:
            for name in self.vars:
                self.val[name] = -1

        if step == op.delay:
            self.cn1.update(self.cn2)


# global select ## Warning: Unused global
# global string ## Warning: Unused global