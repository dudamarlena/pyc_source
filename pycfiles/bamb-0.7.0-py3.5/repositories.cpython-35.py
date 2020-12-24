# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/service/repositories.py
# Compiled at: 2017-09-08 11:08:24
# Size of source mod 2**32: 455 bytes


class CrudRepository(object):

    def __init__(self, app=None, *args, **kwargs):
        pass

    @property
    def table_name(self):
        return ''

    def load(self, key, *args, **kwargs):
        pass

    def delete(self, key, *args, **kwargs):
        pass

    def save(self, obj, key, *args, **kwargs):
        pass


class TaskRepository(CrudRepository):

    @property
    def table_name(self):
        return 'tasks'