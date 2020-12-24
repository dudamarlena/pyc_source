# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sdehaan/Documents/Repositories/unicore-cms-django/cms/context_processors.py
# Compiled at: 2014-10-21 08:08:56
from django.conf import settings
from elasticgit import EG
from cms.models import ContentRepository

def workspace_changes(request):
    workspace = EG.workspace(settings.GIT_REPO_PATH, index_prefix=settings.ELASTIC_GIT_INDEX_PREFIX)
    repo = workspace.repo
    index = repo.index
    origin = repo.remote()
    fetch_info, = origin.fetch()
    remote_master = origin.refs.master
    return {'repo_changes': len(index.diff(remote_master.commit))}


def content_repositories(request):
    return {'content_repositories': ContentRepository.objects.all()}