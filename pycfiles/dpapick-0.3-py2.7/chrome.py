# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/DPAPI/Probes/chrome.py
# Compiled at: 2014-09-22 08:34:07
from DPAPI import probe
from DPAPI.Core import blob

class ChromePassword(probe.DPAPIProbe):
    """This class represents a Google Chrome password entry that can
        be found in the SQLite databases of this browser.

    """

    def parse(self, data):
        self.dpapiblob = blob.DPAPIBlob(data.remain())

    def __getattr__(self, name):
        return getattr(self.dpapiblob, name)

    def __repr__(self):
        s = [
         'Google Chrome Password']
        if self.dpapiblob is not None and self.dpapiblob.decrypted:
            s.append('        password = %s' % self.cleartext)
        s.append('    %r' % self.dpapiblob)
        return ('\n').join(s)