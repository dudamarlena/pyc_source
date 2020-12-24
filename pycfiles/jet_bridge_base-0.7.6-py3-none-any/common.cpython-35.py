# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/f1nal/Dropbox/python/jet-bridge/src/packages/jet_bridge_base/jet_bridge_base/utils/common.py
# Compiled at: 2019-10-30 05:24:12
# Size of source mod 2**32: 2241 bytes
import hashlib, random, time
try:
    random = random.SystemRandom()
    using_sysrandom = True
except NotImplementedError:
    import warnings
    warnings.warn('A secure pseudo-random number generator is not available on your system. Falling back to Mersenne Twister.')
    using_sysrandom = False

def get_random_string(length, allowed_chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', salt=''):
    """
    Returns a securely generated random string.

    The default length of 12 with the a-z, A-Z, 0-9 character set returns
    a 71-bit value. log_2((26+26+10)^12) =~ 71 bits
    """
    if not using_sysrandom:
        random.seed(hashlib.sha256(('%s%s%s' % (
         random.getstate(),
         time.time(),
         salt)).encode('utf-8')).digest())
    return ''.join(random.choice(allowed_chars) for i in range(length))


def find_index(list, predicate):
    for i, value in enumerate(list):
        if predicate(value, i):
            return i


def merge(destination, source):
    for key, value in source.items():
        if key == 'params':
            destination[key] = value
        else:
            if isinstance(value, dict):
                node = destination.setdefault(key, {})
                merge(node, value)
            else:
                if isinstance(value, list):
                    node = destination.setdefault(key, [])
                    for item in value:
                        index = find_index(node, lambda x, i: x['db_column'] == item['db_column'])
                        if index is None:
                            pass
                        else:
                            node[index]
                            merge(node[index], item)

                else:
                    destination[key] = value

    return destination