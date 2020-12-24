# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/minideblib/DebianSigVerifier.py
# Compiled at: 2007-11-06 15:08:00
import os
from minideblib.GPGSigVerifier import GPGSigVerifier

class DebianSigVerifier(GPGSigVerifier):
    _dpkg_ring = '/etc/dpkg/local-keyring.gpg'

    def __init__(self, keyrings=None, extra_keyrings=None):
        if keyrings is None:
            keyrings = [
             '/usr/share/keyrings/debian-keyring.gpg', '/usr/share/keyrings/debian-keyring.pgp']
        if os.access(self._dpkg_ring, os.R_OK):
            keyrings.append(self._dpkg_ring)
        if extra_keyrings is not None:
            keyrings += extra_keyrings
        GPGSigVerifier.__init__(self, keyrings)
        return