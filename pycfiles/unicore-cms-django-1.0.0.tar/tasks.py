# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sdehaan/Documents/Repositories/unicore-cms-django/cms/tasks.py
# Compiled at: 2014-10-22 08:06:46
from celery import task
from cms import utils

@task(serializer='json')
def push_to_git(repo_path, index_prefix):
    utils.push_to_git(repo_path, index_prefix)