# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/package_version_manager/directory_crawler.py
# Compiled at: 2020-04-11 12:42:38
# Size of source mod 2**32: 1684 bytes
from logging import getLogger
from os import scandir
from os.path import isdir, join
from package_version_manager.project_repository import ProjectRepository

class DirectoryCrawler:

    def __init__(self, target_dir, config, skip_confirmations):
        self.target_dir = target_dir
        self.config = config
        self.skip_confirmations = skip_confirmations
        self.to_update_project_repositories = []
        self.logger = getLogger(DirectoryCrawler.__name__)

    def find_repos_to_update(self):
        for entry in scandir(self.target_dir):
            if entry.is_dir():
                self._register_repo_if_relevant(entry)

    def update_repos(self):
        for repo in self.to_update_project_repositories:
            repo.update_version()
            repo.commit_in_version_branch()
            if not self.skip_confirmations:
                user_input = input(f"Push version branch for {repo.entry.name} ? Y/n")
                if user_input.lower() in ('n', 'no'):
                    continue
            repo.push_version_branch()
            repo.create_pull_request()

    def _register_repo_if_relevant(self, entry):
        if DirectoryCrawler._is_a_git_repo(entry):
            project_repo = ProjectRepository(entry, self.config)
            if project_repo.is_version_to_update():
                self.logger.info(f"{project_repo} will be updated")
                self.to_update_project_repositories.append(project_repo)
            else:
                self.logger.debug(f"{project_repo} is up to date")

    @staticmethod
    def _is_a_git_repo(entry):
        return isdir(join(entry, '.git'))