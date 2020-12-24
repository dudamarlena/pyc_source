# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/robotics/github_repository_cloner/repository_analyzers/offline/git_repository_analyzer.py
# Compiled at: 2019-02-05 07:51:56
# Size of source mod 2**32: 2542 bytes
from .abstract_repository_analyzer import AbstractRepositoryAnalyzer
from git import Repo
from git import InvalidGitRepositoryError
import subprocess, os, logging

class GitRepositoryAnalyzer(AbstractRepositoryAnalyzer):
    __doc__ = '\n    Analysis plug-in for Git-Repositories.\n    '

    def count_repo_branches(self, repo_path: str, remote: str) -> None:
        """
        Counts the repository's branches.
        :param repo_path: path to the repository root.
        :param remote: remote uri of the branches
        :return: None
        """
        branches = subprocess.check_output('cd ' + repo_path + ';git branch -a | wc -l', shell=True)
        self.get_details(remote)['branch_count'] = int(branches)

    def count_repo_contributors(self, repo_path: str, remote: str) -> None:
        """
        Counts the repository's contributors.
        :param repo_path: path to the repository root.
        :param remote: remote uri of the branches
        :return: None
        """
        contributors = subprocess.check_output('cd ' + repo_path + ';git shortlog -s HEAD | wc -l', shell=True)
        self.get_details(remote)['contributors'] = int(contributors)

    def extract_last_repo_update(self, repo_path: str, remote: str) -> None:
        """
        Extracts the repository's last update-timestamp.
        :param repo_path: path to the repository root.
        :param remote: remote uri of the branches
        :return: None
        """
        timestamp = subprocess.check_output('cd ' + repo_path + ';git log -1 --format=%ct', shell=True)
        self.get_details(remote)['last_update'] = int(timestamp)

    def _analyze(self, path: str, repo_details: dict) -> iter:
        self._repo_details = repo_details
        for folder in os.listdir(path):
            current_path = path + '/' + folder + ''
            logging.info('[GitRepositoryAnalyzer]: Analyzing:' + current_path)
            try:
                repo = Repo(path + '/' + folder + '/')
            except InvalidGitRepositoryError:
                continue

            origin_url = repo.remotes.origin.url
            self.count_repo_contributors(current_path, origin_url)
            self.count_repo_branches(current_path, origin_url)
            self.extract_last_repo_update(current_path, origin_url)
            yield (
             current_path, origin_url)

    def analyzes(self):
        return 'git'