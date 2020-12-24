# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/persist/task_repo.py
# Compiled at: 2017-09-08 11:08:24
# Size of source mod 2**32: 344 bytes
from service import repositories
from persist import simple_repository

class TaskRepositoryImpl(simple_repository.SimpleMongoDbRepository, repositories.TaskRepository):

    def __init__(self, app=None):
        simple_repository.SimpleMongoDbRepository.__init__(self, app=app)

    @property
    def table_name(self):
        return 'tasks'