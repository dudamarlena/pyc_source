# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jos/utils.py
# Compiled at: 2014-03-10 08:13:26
import hashlib
from datetime import datetime

def gen_timestamp():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def sign(secret, params):
    """generate signature based on app secret and parameters.

    :param secret: a valid app secret
    :param params: parameters which are required to generate valid signature.
                   should be a dict.
    """
    keys = params.keys()
    keys.sort()
    p_string = ('').join('%s%s' % (key, params[key]) for key in keys)
    p_string = ('').join([secret, p_string, secret])
    sign = hashlib.md5(p_string).hexdigest().upper()
    return sign