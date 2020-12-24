# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/fedservice/entity_statement/cache.py
# Compiled at: 2019-12-09 11:21:04
# Size of source mod 2**32: 1048 bytes
import logging
from cryptojwt.jwt import utc_time_sans_frac
logger = logging.getLogger(__name__)

class ESCache(object):

    def __init__(self, allowed_delta=300):
        self._db = {}
        self.allowed_delta = allowed_delta

    def __setitem__(self, key, value):
        self._db[key] = value

    def __getitem__(self, item):
        try:
            statement = self._db[item]
        except KeyError:
            return
        else:
            if isinstance(statement, dict):
                _now = utc_time_sans_frac()
                if _now < statement['exp'] - self.allowed_delta:
                    return statement
                del self._db[item]
                return
            else:
                return statement

    def __delitem__(self, key):
        del self._db[key]

    def __contains__(self, item):
        _val = self[item]
        if _val:
            return True
        return False