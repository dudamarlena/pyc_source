# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/pytq-project/pytq/pkg/fingerprint.py
# Compiled at: 2017-11-23 13:02:06
import pickle, hashlib

def hash_data(data):
    """
    Fingerprint of the data.
    """
    m = hashlib.md5()
    m.update(pickle.dumps(data))
    return m.hexdigest()