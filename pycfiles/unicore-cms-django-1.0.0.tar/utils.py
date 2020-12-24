# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sdehaan/Documents/Repositories/unicore-cms-django/cms/utils.py
# Compiled at: 2014-10-23 14:22:21
from elasticgit import EG

def push_to_git(repo_path, index_prefix):
    workspace = EG.workspace(repo_path, index_prefix=index_prefix)
    if workspace.repo.remotes:
        repo = workspace.repo
        remote = repo.remote()
        remote.fetch()
        remote_master = remote.refs.master
        remote.push(remote_master.remote_head)