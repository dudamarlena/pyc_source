# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/bitwarden_simple_cli/models/domain/SymmetricCryptoKey_test.py
# Compiled at: 2019-04-19 09:41:11
# Size of source mod 2**32: 773 bytes
import pytest
import bitwarden_simple_cli.models.domain.SymmetricCryptoKey as SymmetricCryptoKey
from bitwarden_simple_cli.tests.fixtures_common import common_data
from base64 import b64decode, b64encode

def test_symmetric_crypto_key_aes_cbc_256_b64():
    key = b64decode(common_data('protected_key_decoded'))
    sck = SymmetricCryptoKey(key)
    assert sck.encType.value == 0
    assert sck.encKey == key
    assert sck.macKey is None


def test_symmetric_crypto_key_aes_cbc_256_hmac_sha_256_b64():
    key = b64decode(common_data('BW_SESSION'))
    sck = SymmetricCryptoKey(key)
    assert sck.encType.value == 2
    assert sck.encKeyB64 == b'Tyy0rDgzvA/jgHsqUtKIgNnAWaRtHKZoSs6pa10qWQc='
    assert sck.macKeyB64 == b'9EJhbXdv8Z/EzScvBbtpz0TVQ6Z95O7buPVtaUFVPGY='