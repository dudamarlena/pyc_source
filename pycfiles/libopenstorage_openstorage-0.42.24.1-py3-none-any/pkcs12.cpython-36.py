# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/cryptography/cryptography/hazmat/primitives/serialization/pkcs12.py
# Compiled at: 2020-01-10 16:25:38
# Size of source mod 2**32: 377 bytes
from __future__ import absolute_import, division, print_function

def load_key_and_certificates(data, password, backend):
    return backend.load_key_and_certificates_from_pkcs12(data, password)