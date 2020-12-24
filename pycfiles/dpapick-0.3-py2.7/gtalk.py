# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/DPAPI/Probes/gtalk.py
# Compiled at: 2014-09-22 08:18:29
import array, struct
from DPAPI import probe
from DPAPI.Core import blob

class GTalkAccount(probe.DPAPIProbe):
    r"""Probe to decrypt Google Talk saved credentials.

        They are stored in the user account registry, aka
        HKCU\Software\Google\Google Talk\Accounts

        Each subkey contains a "pw" value that is the obfuscated DPAPI blob
        that should be given to the constructor.

    """

    def parse(self, data):
        self.login = None
        self.raw = data.remain()
        return

    def preprocess(self, **k):
        self.login = k.get('login', None)
        entrop = [
         1777540771, 534340103, 2100685086, 1216205391]
        seed = 3121456925
        maxint = 4294967295
        arr = array.array('B')
        arr.fromstring(k['username'] + k['computername'])
        for i, v in enumerate(arr):
            entrop[(i & 3)] ^= seed * v & maxint
            seed = seed * 48271 & maxint

        self.entropy = ('').join(map(lambda y: struct.pack('<L', y & maxint), entrop))
        v = entrop[0] | 1
        arr = array.array('B')
        for i in range(4, len(self.raw), 2):
            a = ord(self.raw[i]) - 33 << 4 & 240 | ord(self.raw[(i + 1)]) - 33 & 15
            arr.append((a - (v & 255)) % 256)
            v = v * 4085 & maxint

        self.dpapiblob = blob.DPAPIBlob(arr.tostring())
        return

    def __getattr__(self, name):
        return getattr(self.dpapiblob, name)

    def __repr__(self):
        s = [
         'Google Talk account']
        if self.login is not None:
            s.append('        login    = %s' % self.login)
        if self.dpapiblob is not None and self.dpapiblob.decrypted:
            s.append('        password = %s' % self.cleartext)
        if self.entropy is not None:
            s.append('        entropy  = %s' % self.entropy.encode('hex'))
        s.append('    %r' % self.dpapiblob)
        return ('\n').join(s)