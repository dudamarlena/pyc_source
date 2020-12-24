# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mautrix/util/signed_token.py
# Compiled at: 2019-11-21 01:01:47
# Size of source mod 2**32: 1335 bytes
from typing import Dict, Optional
from hashlib import sha256
import hmac, json, base64

def _get_checksum(key: str, payload: bytes) -> str:
    hasher = hmac.new((key.encode('utf-8')), msg=payload, digestmod=sha256)
    checksum = base64.urlsafe_b64encode(hasher.digest())
    return checksum.decode('utf-8').rstrip('=')


def sign_token(key: str, payload: Dict) -> str:
    payload_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode('utf-8'))
    checksum = _get_checksum(key, payload_b64)
    payload_str = payload_b64.decode('utf-8').rstrip('=')
    return f"{checksum}:{payload_str}"


def verify_token(key: str, data: str) -> Optional[Dict]:
    if not data:
        return
    try:
        checksum, payload = data.split(':', 1)
    except ValueError:
        return
    else:
        payload += (3 - (len(payload) + 3) % 4) * '='
        if checksum != _get_checksum(key, payload.encode('utf-8')):
            return
        payload = base64.urlsafe_b64decode(payload).decode('utf-8')
        try:
            return json.loads(payload)
        except json.JSONDecodeError:
            return