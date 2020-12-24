# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/notemodel/util/core.py
# Compiled at: 2020-04-15 05:55:02
# Size of source mod 2**32: 111 bytes
import hashlib

def get_file_md5(weight):
    m = hashlib.md5()
    m.update(weight)
    return m.hexdigest()