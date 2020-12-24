# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/doh/utils.py
# Compiled at: 2017-12-16 15:37:57
# Size of source mod 2**32: 209 bytes
import string, random
UNRESERVED_CHARS = string.ascii_letters + string.digits + '-._~'

def random_padding():
    return ''.join(random.choice(UNRESERVED_CHARS) for _ in range(random.randint(10, 50)))