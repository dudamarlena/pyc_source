# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/universalcore/unicore-cms/cms/tasks.py
# Compiled at: 2016-05-07 04:51:23
from pyramid_celery import celery_app as app
from elasticgit import EG
from elasticgit.storage import RemoteStorageManager
from cms.views.utils import is_remote_repo_url

@app.task(ignore_result=True)
def pull(repo_url, index_prefix, es=None):
    if is_remote_repo_url(repo_url):
        sm = RemoteStorageManager(repo_url)
        sm.pull()
    else:
        workspace = EG.workspace(repo_url, index_prefix=index_prefix, es=es)
        workspace.pull()