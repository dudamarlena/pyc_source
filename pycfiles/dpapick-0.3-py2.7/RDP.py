# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/DPAPI/Probes/RDP.py
# Compiled at: 2014-09-22 09:04:02
from DPAPI.probe import DPAPIProbe
from DPAPI.Core import blob
from collections import defaultdict

class RDPFile(DPAPIProbe):

    def parse(self, data):
        self.cleartext = None
        self.dpapiblob = None
        self.entropy = None
        self.values = defaultdict(lambda : None)
        return

    def preprocess(self, **k):
        s = []
        if k.get('file') != None:
            f = open(k['file'], 'r')
            s = f.read().split('\n')
            f.close()
        else:
            if k.get('content') != None:
                s = k['content'].split('\n')
            for l in s:
                n, t, v = l.split(':', 3)
                v = v.rstrip()
                if t == 'i':
                    v = int(v)
                elif t == 'b':
                    if len(v) & 1 == 1:
                        v = v[:-1]
                    v = v.decode('hex')
                self.values[n] = v
                if self.values['password 51'] != None:
                    self.dpapiblob = blob.DPAPIBlob(self.values['password 51'])

        return

    def __repr__(self):
        s = [
         'RDP Connection file']
        for p in self.__dict__:
            if self.__dict__[p] != None:
                s.append('        %s = %r' % (p, self.__dict__[p]))

        return ('\n').join(s)