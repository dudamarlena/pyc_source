# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/narendra/.pyenv/versions/aws/lib/python3.6/site-packages/tvarit_api/resources/task.py
# Compiled at: 2019-09-30 09:28:30
# Size of source mod 2**32: 1697 bytes
from .base import Base

class Task(Base):

    def __init__(self, api):
        super(Task, self).__init__(api)
        self.api = api

    def get_task_by_id(self, task_id, brief=False, rdepends=False, resolve=None):
        if type(task_id) == list:
            task_id = ','.join([str(m) for m in task_id])
        params = dict(brief=brief,
          rdepends=rdepends,
          resolve=(resolve or []))
        endpoint = '/tasks/{}'.format(task_id)
        return self.api.GET(endpoint, params=params)

    def create_task(self, task, update_if_exists=False):
        params = dict(update_if_exists=update_if_exists)
        endpoint = '/tasks'
        return self.api.POST(endpoint, json=task, params=params)

    def update_task(self, task_id, task):
        endpoint = '/tasks/{}'.format(task_id)
        return self.api.PUT(endpoint, json=task)

    def upload_task_json(self, tasks, strict=False):
        params = dict(strict=strict)
        endpoint = '/tasks/json'
        return self.api.POST(endpoint, json=tasks, params=params)

    def list_tasks(self, detail=False, rdepends=False, resolve=None, limit=100, page=0):
        params = dict(detail=detail,
          rdepends=rdepends,
          resolve=(resolve or []),
          limit=limit,
          page=page)
        endpoint = '/tasks'
        return self.api.GET(endpoint, params=params)

    def delete_task_by_id(self, task_id):
        if type(task_id) == list:
            task_id = ','.join([str(m) for m in task_id])
        endpoint = '/tasks/{}'.format(task_id)
        return self.api.DELETE(endpoint)