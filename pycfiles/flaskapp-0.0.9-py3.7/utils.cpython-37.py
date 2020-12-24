# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/flaskapp/base/utils.py
# Compiled at: 2019-07-24 05:34:04
# Size of source mod 2**32: 164 bytes
import hashlib

def get_hash(data, salt):
    m = len(salt) // 2
    sdata = salt[:m] + data + salt[m:]
    return hashlib.sha256(sdata.encode('utf-8')).hexdigest()