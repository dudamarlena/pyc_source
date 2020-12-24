# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/main/util.py
# Compiled at: 2018-12-20 02:38:21
# Size of source mod 2**32: 856 bytes
import hashlib

def read(filename, binary=True):
    with open(filename, 'rb' if binary else 'r') as (f):
        return f.read()


def get_md5(buf):
    m = hashlib.md5()
    m.update(buf)
    return m.hexdigest().lower()