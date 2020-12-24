# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/DPAPI/Probes/credstore.py
# Compiled at: 2014-09-22 08:18:20
import struct, datetime
from DPAPI import probe
from DPAPI.Core import blob

class CredentialStore(probe.DPAPIProbe):
    """This class represents a Credential Store file.
        It parses the file to extract the header, then builds a CredArray
        object that will contain Credential objects that are the actual blob

    """

    class Credential(probe.DPAPIProbe):
        """Represents an entry in the credential store."""
        _entropy = {1: 'abe2869f-9b47-4cd9-a358-c22904dba7f7\x00', 
           4: '82BD0E67-9FEA-4748-8672-D5EFE5B779B0\x00'}
        _type = {1: 'Generic', 
           2: 'Domain password', 
           3: 'Domain certificate', 
           4: 'Domain Visible password', 
           5: 'Generic certificate', 
           6: 'Domain extended'}
        _persist = [
         'No', 'Session', 'Local machine', 'Entreprise']

        def parse(self, data):
            tmp = data.read('L')
            d = data
            if tmp == 0:
                data.read('L')
                self.credtype = data.eat('L')
                data.eat('L')
            else:
                d = data.eat_sub(tmp)
                d.eat('2L')
                self.credtype = d.eat('L')
            self.timestamp = d.eat('Q')
            if self.timestamp > 0:
                self.timestamp /= 10000000
                self.timestamp -= 11644473600
            d.eat('L')
            self.persist = d.eat('L')
            d.eat('3L')
            self.name = d.eat_length_and_string('L').decode('UTF-16LE')
            self.comment = d.eat_length_and_string('L').decode('UTF-16LE')
            self.alias = d.eat_length_and_string('L').decode('UTF-16LE')
            if tmp == 0:
                d.eat_length_and_string('L')
            self.username = d.eat_length_and_string('L').decode('UTF-16LE')
            self.password = None
            if self.credtype == 1 or self.credtype == 4:
                self.dpapiblob = blob.DPAPIBlob(d.eat_length_and_string('L'))
            elif self.credtype == 2:
                self.password = d.eat_length_and_string('L')
                self.password = self.password.decode('UTF-16LE')
                self.dpapiblob = None
            elif self.credtype == 3:
                self.password = d.eat_length_and_string('L')
                self.dpapiblob = None
            self.entropy = self._entropy.get(self.credtype)
            if self.entropy is not None:
                s = ''
                for c in self.entropy:
                    s += struct.pack('<h', ord(c) << 2)

                self.entropy = s
            return

        def try_decrypt_with_hash(self, h, mkp, sid, **k):
            if self.dpapiblob is not None:
                return super(CredentialStore.Credential, self).try_decrypt_with_hash(h, mkp, sid, **k)
            else:
                return True

        def postprocess(self, **k):
            if self.credtype == 1:
                v = self.dpapiblob.cleartext.split(':', 2)
                self.username = v[0]
                self.password = v[1]
            if self.credtype == 4:
                self.password = self.dpapiblob.cleartext.decode('UTF-16LE')

        def __repr__(self):
            s = ['Credential']
            s.append('    Type    : %s' % self._type.get(self.credtype, 'Unknown'))
            s.append('    Persist : %s' % self._persist[self.persist])
            s.append('    Name    : %s' % self.name)
            s.append('    Username: %s' % self.username)
            s.append('    Comment : %s' % self.comment)
            s.append('    Alias   : %s' % self.alias)
            if self.password is not None:
                s.append('    Password: %s' % self.password)
            tmp = datetime.datetime.utcfromtimestamp(self.timestamp).ctime()
            s.append('    When    : %s' % tmp)
            if self.entropy is not None:
                s.append('    Entropy : %s' % self.entropy.encode('hex'))
            s.append('    Blob    : %s' % repr(self.dpapiblob))
            return ('\n').join(s)

    class CredArray(probe.DPAPIProbe):
        """Represents all the credential entries that are contained in the
            credential store file.

        """

        def parse(self, data):
            self.revision = data.eat('L')
            self.totallen = data.eat('L')
            self.creds = []
            while data:
                c = CredentialStore.Credential()
                c.parse(data)
                self.creds.append(c)

        def postprocess(self, **k):
            for c in self.creds:
                c.postprocess(**k)

        def try_decrypt_with_hash(self, h, mkp, sid, **k):
            """Returns True if all the entries has been successfully
                decrypted.

                This may change in future versions as in forensics usage
                we just want to retreive as many credentials as we can.

            """
            r = True
            for c in self.creds:
                r &= c.try_decrypt_with_hash(h, mkp, sid, **k)

            return r

        def __repr__(self):
            return ('\n' + '-' * 50 + '\n').join(map(lambda x: repr(x), self.creds))

    def parse(self, data):
        self.dpapiblob = blob.DPAPIBlob(data.remain())
        self.store = None
        return

    def try_decrypt_with_hash(self, h, mkp, sid, **k):
        if super(CredentialStore, self).try_decrypt_with_hash(h, mkp, sid, **k):
            self.store = CredentialStore.CredArray(self.dpapiblob.cleartext)
            return self.store.try_decrypt_with_hash(h, mkp, sid, **k)
        return False

    def __repr__(self):
        s = [
         'Credential Store']
        if self.store is not None:
            s.append('    %s' % repr(self.store))
        return ('\n').join(s)