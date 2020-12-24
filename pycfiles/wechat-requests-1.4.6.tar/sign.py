# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: f:\pipeline\wechat\src\wechat\sign.py
# Compiled at: 2018-05-18 06:19:50
import time, hmac, random, string, hashlib
from . import settings
from .compat import str, range, unicode
__all__ = [
 'random_nonce_str', 'sign_for_pay', 'sign_for_jsapi']

def random_nonce_str(length):
    if length <= 0:
        raise ValueError('length must > 0')
    return ('').join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


def _build_sign_str(sign_key, **kwargs):
    keys = sorted(kwargs.keys())
    _sign_str_parts = []
    for key in keys:
        if key == 'sign':
            continue
        val = kwargs[key]
        if val is None or isinstance(val, str) and len(val) == 0:
            continue
        val = str(val)
        _sign_str_parts.append(('{}={}&').format(key, val))

    if sign_key is not None:
        return ('').join(_sign_str_parts) + ('key={}').format(sign_key)
    else:
        return ('').join(_sign_str_parts)
        return


def sign_for_pay(sign_key, **kwargs):
    if 'sign_type' in kwargs:
        sign_type = kwargs['sign_type']
    else:
        sign_type = settings.SIGN_TYPE
    if sign_type not in ('MD5', 'HMAC-SHA256'):
        raise ValueError('only surpport MD5 and HMAC-SHA256')
    sign_str = _build_sign_str(sign_key, **kwargs)
    sign_bytes = sign_str.encode('utf-8')
    if sign_type == 'MD5':
        return hashlib.md5(sign_bytes).hexdigest().upper()
    else:
        if type(sign_key) is unicode:
            sign_key = sign_key.encode('utf-8')
        return hmac.new(sign_key, msg=sign_bytes, digestmod=hashlib.sha256).hexdigest().upper()


def sign_for_jsapi(jsapi_ticket, url, nonce=None, timestamp=None):
    if nonce is None:
        nonce = random_nonce_str(16)
    if timestamp is None:
        timestamp = int(time.time())
    _dict = {'nonceStr': nonce, 
       'jsapi_ticket': jsapi_ticket, 
       'timestamp': timestamp, 
       'url': url}
    tosign_str = ('&').join([ '%s=%s' % (key.lower(), _dict[key]) for key in sorted(_dict) ])
    if type(tosign_str) == unicode:
        tosign_str = tosign_str.encode('utf-8')
    _dict['signature'] = hashlib.sha1(tosign_str).hexdigest()
    return _dict