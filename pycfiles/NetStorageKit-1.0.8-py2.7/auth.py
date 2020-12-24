# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/netstoragekit/auth.py
# Compiled at: 2015-06-17 02:27:40
import hmac, hashlib, logging
from time import time
from random import getrandbits
from .utils import get_remote_path
log = logging.getLogger(__name__)

def get_data(key_name, timestamp=None, unique_id=None):
    """Gets the X-Akamai-ACS-Auth-Data header value.

    Args:
        key_name: The NS Upload Account key_name as configured in Luna.
        timestamp: Optional timestamp (mainly for testing purposes).
        unique_id: Optional unique identifier (mainly for testing purposes).

    Returns:
        The header value.
    """
    values = [
     '5',
     '0.0.0.0',
     '0.0.0.0',
     str(timestamp or int(time())),
     str(unique_id or getrandbits(64)),
     key_name]
    data = str((', ').join(values))
    log.debug(data)
    return data


def get_sign_string(cpcode, path, data, action):
    """Gets the X-Akamai-ACS-Auth-Sign sign string.

    Args:
        cpcode: The CPCode.
        path: The remote path, without cpcode.
        data: The data header value.
        action: The action header value.

    Returns:
        The sign string.
    """
    values = [
     data,
     get_remote_path(cpcode, path) + '\n',
     'x-akamai-acs-action:' + action + '\n']
    sign_string = str(('').join(values))
    log.debug(sign_string.replace('\n', '\\n'))
    return sign_string


def get_sign(key, cpcode, path, data, action):
    """Gets the X-Akamai-ACS-Auth-Sign header value.

    Args:
        key: The NS Upload Account key as configured in Luna.
        cpcode: The CPCode.
        path: The remote path, without cpcode.
        data: The data header value.
        action: The action header value.

    Returns:
        The base 64 encoded header value.
    """
    msg = get_sign_string(cpcode, path, data, action)
    digest = hmac.new(str(key), msg=msg, digestmod=hashlib.sha256).digest()
    sign = digest.encode('base64').strip()
    log.debug(sign)
    return sign