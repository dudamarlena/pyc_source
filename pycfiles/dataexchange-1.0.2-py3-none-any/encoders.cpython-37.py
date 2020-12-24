# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\dataexchange\dataexchange\json\encoders.py
# Compiled at: 2020-01-21 00:50:52
# Size of source mod 2**32: 149 bytes
import json

def jsonencoder(data):
    with open(data) as (file):
        obj = file.read()
        obj = json.loads(obj)
        return obj