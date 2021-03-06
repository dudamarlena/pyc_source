# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sovereign/utils/auth.py
# Compiled at: 2020-04-29 02:35:50
# Size of source mod 2**32: 1644 bytes
from fastapi.exceptions import HTTPException
from sovereign import config
from sovereign.statistics import stats
from sovereign.schemas import DiscoveryRequest
from sovereign.utils.crypto import decrypt, KEY_AVAILABLE, InvalidToken

def validate_authentication_string(s: str):
    try:
        password = decrypt(s)
    except Exception:
        stats.increment('discovery.auth.failed')
        raise
    else:
        if password in config.passwords:
            stats.increment('discovery.auth.success')
            return True
        stats.increment('discovery.auth.failed')
        return False


def authenticate(request: DiscoveryRequest):
    if not config.auth_enabled:
        return
    if not KEY_AVAILABLE:
        raise RuntimeError('No Fernet key loaded, and auth is enabled. A fernet key must be provided via SOVEREIGN_ENCRYPTION_KEY. See https://vsyrakis.bitbucket.io/sovereign/docs/html/guides/encryption.html for more details')
    try:
        encrypted_auth = request.node.metadata['auth']
        with stats.timed('discovery.auth.ms'):
            assert validate_authentication_string(encrypted_auth)
    except KeyError:
        raise HTTPException(status_code=401, detail=f"Discovery request from {request.node.id} is missing auth field")
    except (InvalidToken, AssertionError):
        raise HTTPException(status_code=401, detail='The authentication provided was invalid')
    except Exception as e:
        try:
            description = getattr(e, 'detail', 'Unknown')
            raise HTTPException(status_code=400, detail=f"The authentication provided was malformed [Reason: {description}]")
        finally:
            e = None
            del e