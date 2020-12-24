# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/work/lib/pyenv/versions/3.6.1/envs/maestro/lib/python3.6/site-packages/rest_framework/core/serializers/pickle.py
# Compiled at: 2018-10-12 04:43:03
# Size of source mod 2**32: 195 bytes
import pickle

class Handler:

    def dumps(self, value):
        return pickle.dumps(value, protocol=1)

    def loads(self, value):
        return pickle.loads(value)