# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/site-packages/gmssl/func.py
# Compiled at: 2020-03-10 11:26:45
# Size of source mod 2**32: 879 bytes
import sys
from random import choice
xor = lambda a, b: list(map(lambda x, y: x ^ y, a, b))
rotl = lambda x, n: x << n & 4294967295 | x >> 32 - n & 4294967295
get_uint32_be = lambda key_data: key_data[0] << 24 | key_data[1] << 16 | key_data[2] << 8 | key_data[3]
put_uint32_be = lambda n: [
 n >> 24 & 255, n >> 16 & 255, n >> 8 & 255, n & 255]
padding = lambda data, block=16: data + [16 - len(data) % block for _ in range(16 - len(data) % block)]
unpadding = lambda data: data[:-data[(-1)]]
if sys.version_info[0] == 2:
    list_to_bytes = lambda data: ''.join([chr(x) for x in data])
    bytes_to_list = lambda data: [ord(x) for x in data]
else:
    list_to_bytes = lambda data: (b'').join([bytes((i,)) for i in data])
    bytes_to_list = lambda data: [i for i in data]
random_hex = lambda x: ''.join([choice('0123456789abcdef') for _ in range(x)])