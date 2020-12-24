# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dalou/www/VALDYS/MANAGER/app/utils/security.py
# Compiled at: 2017-11-07 12:27:53
# Size of source mod 2**32: 1394 bytes
import hashlib, random
from django.utils.http import base36_to_int, int_to_base36
__all__ = [
 'random_token', 'request_uid_token']

def random_token(extra=None, hash_func=hashlib.sha256):
    if extra is None:
        extra = []
    else:
        if not isinstance(extra, list) or not isinstance(extra, tuple):
            extra = [
             str(extra)]
    bits = [str(e) for e in extra] + [str(random.SystemRandom().getrandbits(512))]
    return hash_func(''.join(bits).encode('utf-8')).hexdigest()


def request_uid_token(request):
    from django.contrib.auth.tokens import default_token_generator
    uid = int_to_base36(request.user.id)
    token = default_token_generator.make_token(request.user)
    return (uid, token)