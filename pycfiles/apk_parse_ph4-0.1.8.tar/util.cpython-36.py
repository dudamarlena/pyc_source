# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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