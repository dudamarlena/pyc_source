# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/DPAPI/probe.py
# Compiled at: 2014-10-14 03:55:31
import hashlib
from DPAPI.Core import eater

class DPAPIProbe(eater.DataStruct):
    """This is the generic class for building DPAPIck probes.
        All probes must inherit this class.

    """

    def __init__(self, raw=None):
        """Constructs a DPAPIProbe object.
            If raw is set, automatically builds a DataStruct with that
            and calls parse() method with this.

        """
        self.dpapiblob = None
        self.cleartext = None
        self.entropy = None
        eater.DataStruct.__init__(self, raw)
        return

    def parse(self, data):
        """Parses raw data into structured data.
            Automatically called by __init__. You should not call it manually.

            data is a DataStruct object.

        """
        pass

    def preprocess(self, **k):
        """Optional. Apply tranformations to data before the decryption loop."""
        self.entropy = k.get('entropy')

    def postprocess(self, **k):
        """Optional. Apply transformations after a successful decryption."""
        if self.dpapiblob.decrypted:
            self.cleartext = self.dpapiblob.cleartext

    def try_decrypt_system(self, mkeypool, **k):
        """Decryption loop for SYSTEM account protected blob. eg. wifi blobs.
            Basic probes should not overload this function.

            Returns True/False upon decryption success/failure.

        """
        self.preprocess(**k)
        mkeypool.try_credential(None, None)
        for kguid in self.dpapiblob.guids:
            mks = mkeypool.getMasterKeys(kguid)
            for mk in mks:
                if mk.decrypted:
                    self.dpapiblob.decrypt(mk.get_key(), self.entropy, k.get('strong', None))
                    if self.dpapiblob.decrypted:
                        self.postprocess(**k)
                        return True

        return False

    def try_decrypt_with_hash(self, h, mkeypool, sid, **k):
        """Decryption loop for general blobs with given user's password hash.
            This function will call preprocess() first, then tries to decrypt.

            k may contain optional values such as:
                entropy: the optional entropy to use with that blob.
                strong: strong password given by the user

            Basic probes should not override this one as it contains the full
            decryption logic.

            Returns True/False upon decryption success/failure.

        """
        self.preprocess(**k)
        mkeypool.try_credential_hash(sid, h)
        mks = mkeypool.getMasterKeys(self.dpapiblob.mkguid)
        for mk in mks:
            if mk.decrypted:
                self.dpapiblob.decrypt(mk.get_key(), self.entropy, k.get('strong', None))
                if self.dpapiblob.decrypted:
                    self.postprocess(**k)
                    return True

        return False

    def try_decrypt_with_password(self, password, mkeypool, sid, **k):
        """Decryption loop for general blobs with given user's password.
            Simply computes the hash then calls try_decrypt_with_hash()

            Return True/False upon decryption success/failure.

        """
        self.preprocess(**k)
        mkeypool.try_credential(sid, password)
        mks = mkeypool.getMasterKeys(self.dpapiblob.mkguid)
        for mk in mks:
            if mk.decrypted:
                self.dpapiblob.decrypt(mk.get_key(), self.entropy, k.get('strong', None))
                if self.dpapiblob.decrypted:
                    self.postprocess(**k)
                    return True

        return False