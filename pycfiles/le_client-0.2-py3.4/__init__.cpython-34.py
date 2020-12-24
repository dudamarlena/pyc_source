# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/le_client/__init__.py
# Compiled at: 2016-07-21 12:15:56
# Size of source mod 2**32: 1143 bytes
from .keys import ECKeyFile, RemoteKey
from .request import CertificateRequest
from .acme import ACMEAuthority, UnexpectedHTTPStatus

def get_certificate(account_key, csr, webroot, register=True, no_www=True):
    acme = ACMEAuthority(account_key)
    if register:
        acme.register()

    def make_path(dn):
        if no_www:
            if dn.startswith('www.'):
                dn = dn[4:]
        return webroot.format(dn)

    return acme.get_certificate(csr, make_path)