# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/le_client/request.py
# Compiled at: 2016-07-21 12:15:56
# Size of source mod 2**32: 1574 bytes
import re
from .utils import openssl

class CertificateRequest(object):

    def __init__(self, filename):
        self.filename = filename

    def get_domains(self):
        domains = set()
        data = openssl('req', '-in', self.filename, '-noout', '-text').decode('utf-8')
        common_name = re.search('Subject:.*? CN=([^\\s,;/]+)', data)
        if common_name is not None:
            domains.add(common_name.group(1))
        subject_alt_names = re.search('X509v3 Subject Alternative Name:\\s*\\n\\s+([^\\n]+)\\n', data, re.MULTILINE | re.DOTALL)
        if subject_alt_names is not None:
            for san in subject_alt_names.group(1).split(', '):
                if san.startswith('DNS:'):
                    domains.add(san[4:])
                    continue

        return domains

    def as_der(self):
        return openssl('req', '-in', self.filename, '-outform', 'DER')