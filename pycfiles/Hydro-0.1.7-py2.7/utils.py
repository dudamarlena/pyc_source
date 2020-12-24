# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/hydro/common/utils.py
# Compiled at: 2015-05-12 04:50:31
__author__ = 'yanivshalev'
import hashlib

def create_cache_key(fingerprint):
    return hashlib.md5(fingerprint).hexdigest()