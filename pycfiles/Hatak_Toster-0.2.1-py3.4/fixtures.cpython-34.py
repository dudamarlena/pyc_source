# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/haplugin/toster/fixtures.py
# Compiled at: 2014-11-30 09:58:41
# Size of source mod 2**32: 650 bytes
fixtures = {}

class Fixtures(object):

    def __init__(self, db, application):
        self.db = db
        self.fixtures = fixtures
        self.application = application

    def _create(self, cls, **kwargs):
        obj = cls.get_or_create(self.db, **kwargs)
        data = self.fixtures.get(cls.__name__, {})
        data[kwargs['name']] = obj
        self.fixtures[cls.__name__] = data
        return obj

    def _create_nameless(self, cls, **kwargs):
        obj = cls.get_or_create(self.db, **kwargs)
        data = self.fixtures.get(cls.__name__, [])
        data.append(obj)
        self.fixtures[cls.__name__] = data
        return obj