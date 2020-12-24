# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/DPAPI/Probes/IE7.py
# Compiled at: 2014-09-22 08:17:12
import hashlib
from DPAPI import probe
from DPAPI.Core import blob
from DPAPI.Core import eater

class IE7Autocomplete(probe.DPAPIProbe):

    class IE7Secret(eater.DataStruct):

        def __init__(self, raw=None):
            self.secrets = []
            eater.DataStruct.__init__(self, raw)

        def parse(self, data):
            data.eat('L')
            data.eat('L')
            data.eat('L')
            data.eat('L')
            data.eat('L')
            n = data.eat('L')
            data.eat('L')
            data.eat('L')
            data.eat('L')
            l = []
            off = []
            for i in range(n):
                off.append(data.eat('L'))
                data.eat_string(8)
                l.append(2 * data.eat('L'))

            sec = data.remain()
            for i in range(n):
                self.secrets.append(sec[off[i]:off[i] + l[i]].decode('UTF-16LE'))

        def __repr__(self):
            s = ['IE7Secret']
            s.append('%s' % repr(self.secrets))
            return ('\n').join(s)

    class IE7Entry(probe.DPAPIProbe):

        def parse(self, data):
            self.dpapiblob = blob.DPAPIBlob(data.remain())
            self.cleartext = None
            self.login = None
            self.password = None
            self.other = []
            return

        def preprocess(self, **k):
            self.entropy = k.get('entropy', None)
            return

        def postprocess(self, **k):
            b = IE7Autocomplete.IE7Secret(self.dpapiblob.cleartext)
            self.login = b.secrets.pop(0)
            self.password = b.secrets.pop(0)
            if len(b.secrets) > 0:
                self.other = b.secrets

        def __repr__(self):
            s = ['Autocomplete Entry']
            s.append('url     : %s' % self.entropy)
            s.append('login   : %s' % self.login)
            s.append('password: %s' % self.password)
            for i in self.other:
                s.append('secret  : %s' % i)

            s.append('blob    : %r' % self.dpapiblob)
            return ('\n').join(s)

    def parse(self, data):
        pass

    def preprocess(self, **k):
        self._dicurls = {}
        self.entries = k.get('values', {})
        self.urls = k.get('urls', [])
        for i in self.urls:
            u = (i + '\x00').encode('UTF-16LE')
            self._dicurls[hashlib.sha1(u).hexdigest().lower()] = u

        arr = self.entries.keys()
        for i in arr:
            self.entries[i[:40].lower()] = IE7Autocomplete.IE7Entry(self.entries[i])
            self.entries.pop(i)

    def try_decrypt_with_hash(self, h, mkeypool, sid, **k):
        self.preprocess(**k)
        rv = True
        for e in self.entries.keys():
            if self._dicurls.get(e) is not None:
                if not self.entries[e].try_decrypt_with_hash(h, mkeypool, sid, entropy=self._dicurls[e]):
                    rv = False

        return rv

    def postprocess(self, **k):
        pass

    def __repr__(self):
        s = [
         'Internet Explorer 7+ autocomplete']
        for i in self.entries.keys():
            s.append('-' * 50)
            s.append('    %r' % self.entries[i])

        return ('\n').join(s)