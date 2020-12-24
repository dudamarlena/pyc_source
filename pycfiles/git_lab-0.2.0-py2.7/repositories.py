# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/git_lab/apis/projects/repositories.py
# Compiled at: 2014-03-13 04:08:17
from git_lab.apis.projects.models import Project

class ProjectsRepository(object):

    def __init__(self, client=None, project=None):
        u"""
        @param client : GitLabクライアント
        @type  client : gitlab.Gitlab
        """
        from git_lab.utils import get_client, get_project
        self.client = client if client is not None else get_client()
        self.project = project if project is not None else get_project()
        return

    def get_project(self, project_id=None):
        u"""プロジェクトIDでプロジェクト情報を取得する。

        @param project_id : 取得するプロジェクトのID、指定しない場合configに設定されているID
        @type  project_id : str | None
        """
        id_ = project_id if project_id is not None else self.project
        p = self.client.getproject(id_)
        if p is False:
            return
        else:
            return Project(p)
            return