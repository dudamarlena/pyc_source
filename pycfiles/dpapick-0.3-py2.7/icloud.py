# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/DPAPI/Probes/icloud.py
# Compiled at: 2014-10-15 10:57:22
from DPAPI import probe
from DPAPI.Core import blob
from DPAPI.Core import eater
import CFPropertyList

class iCloud(probe.DPAPIProbe):
    """iCloud Apple token decryption"""
    APPLE_ENTROPY = b"\x1d\xac\xa8\xf8\xd3\xb8H>H}>\nb\x07\xdd&\xe6g\x81\x03\xe7\xb2\x13\xa5\xb0y\xeeO\x0fA\x15\xed{\x14\x8c\xe5KF\r\xc1\x8e\xfe\xd6\xe7'u\x06\x8bI\x00\xdc\x0f0\xa0\x9e\xfd\t\x85\xf1\xc8\xaau\xc1\x08\x05y\x01\xe2\x97\xd8\xaf\x808`\x0bq\x0ehSw/\x0fa\xf6\x1d\x8e\x8f\\\xb2=!t@K\xb5\x06n\xabz\xbd\x8b\xa9~2\x8fn\x06$\xd9)\xa4\xa5\xbe&#\xfd\xee\xf1L\x0ft^X\xfb\x91t\xef\x91"

    def preprocess(self, **k):
        self.entropy = self.APPLE_ENTROPY
        with open(k['aoskit'], 'rb') as (f):
            plist = CFPropertyList.CFPropertyList(f)
            plist.load()
            plist_values = CFPropertyList.native_types(plist.value)
            self.account = plist_values.keys()[0]
            plist_data_dict = plist_values[self.account]
            self.dpapiblob = blob.DPAPIBlob(plist_data_dict['data'])

    def parse(self, data):
        self.dpapiblob = None
        self.account = None
        self.decrypted = None
        return

    def postprocess(self, **k):
        if self.dpapiblob.decrypted:
            e = eater.Eater(self.dpapiblob.cleartext)
            self.decrypted = e.eat_length_and_string('L')

    def __repr__(self):
        s = ['\niCloud Apple token decryption']
        if self.dpapiblob is not None and self.dpapiblob.decrypted:
            s.append('Binary PLIST file for account %s decrypted!' % self.account)
        else:
            s.append('Unable to decrypt Apple Token for account %s!' % self.account)
        return ('\n').join(s)