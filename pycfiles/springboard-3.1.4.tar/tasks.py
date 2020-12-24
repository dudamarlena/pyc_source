# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/universalcore/springboard/springboard/tasks.py
# Compiled at: 2015-11-17 11:55:31
from pyramid_celery import celery_app as app
from elasticgit import EG
from elasticgit.storage import RemoteStorageManager
from springboard.utils import is_remote_repo_url, parse_repo_name

@app.task(ignore_result=True)
def pull(repo_url, index_prefix=None, es=None):
    if is_remote_repo_url(repo_url):
        sm = RemoteStorageManager(repo_url)
        sm.pull()
    else:
        index_prefix = index_prefix or parse_repo_name(repo_url)
        workspace = EG.workspace(repo_url, index_prefix=index_prefix, es=es)
        workspace.pull()