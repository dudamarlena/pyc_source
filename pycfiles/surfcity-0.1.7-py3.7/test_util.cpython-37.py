# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/ssb/rpc/tests/test_util.py
# Compiled at: 2018-08-12 02:14:39
# Size of source mod 2**32: 1228 bytes
from base64 import b64decode
from unittest.mock import mock_open, patch
import pytest
from ssb.util import load_ssb_secret, ConfigException
CONFIG_FILE = '\n## Comments should be supported too\n{\n    "curve": "ed25519",\n    "public": "rsYpBIcXsxjQAf0JNes+MHqT2DL+EfopWKAp4rGeEPQ=ed25519",\n    "private": "/bqDBI/vGLD5qy3GxMsgHFgYIrrY08JfTzUaCYT6x0GuxikEhxezGNAB/Qk16z4wepPYMv4R+ilYoCnisZ4Q9A==",\n    "id": "@rsYpBIcXsxjQAf0JNes+MHqT2DL+EfopWKAp4rGeEPQ=.ed25519"\n}\n'
CONFIG_FILE_INVALID = CONFIG_FILE.replace('ed25519', 'foo')

def test_load_secret():
    with patch('ssb.util.open', mock_open(read_data=CONFIG_FILE), create=True):
        secret = load_ssb_secret()
    priv_key = b'\xfd\xba\x83\x04\x8f\xef\x18\xb0\xf9\xab-\xc6\xc4\xcb \x1cX\x18"\xba\xd8\xd3\xc2_O5\x1a\t\x84\xfa\xc7A'
    assert secret['id'] == '@rsYpBIcXsxjQAf0JNes+MHqT2DL+EfopWKAp4rGeEPQ=.ed25519'
    assert bytes(secret['keypair']) == priv_key
    assert bytes(secret['keypair'].verify_key) == b64decode('rsYpBIcXsxjQAf0JNes+MHqT2DL+EfopWKAp4rGeEPQ=')


def test_load_exception():
    with pytest.raises(ConfigException):
        with patch('ssb.util.open', mock_open(read_data=CONFIG_FILE_INVALID), create=True):
            load_ssb_secret()