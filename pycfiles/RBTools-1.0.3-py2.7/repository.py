# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/rbtools/utils/repository.py
# Compiled at: 2020-04-14 20:27:46
from __future__ import unicode_literals

def get_repository_id(repository_info, api_root, repository_name=None):
    """Get the repository ID from the server.

    This will compare the paths returned by the SCM client
    with those on the server, and return the id of the first
    match.
    """
    detected_paths = repository_info.path
    if not isinstance(detected_paths, list):
        detected_paths = [
         detected_paths]
    repositories = api_root.get_repositories(only_fields=b'id,name,mirror_path,path', only_links=b'')
    for repo in repositories.all_items:
        if repo.name == repository_name or repo.path in detected_paths or getattr(repo, b'mirror_path', None) in detected_paths:
            return repo.id

    return