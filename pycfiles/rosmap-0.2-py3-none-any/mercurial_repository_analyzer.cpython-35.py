# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/robotics/github_repository_cloner/repository_analyzers/offline/mercurial_repository_analyzer.py
# Compiled at: 2019-02-05 07:51:55
# Size of source mod 2**32: 3102 bytes
from .abstract_repository_analyzer import AbstractRepositoryAnalyzer
import subprocess, os, logging

class MercurialRepositoryAnalyzer(AbstractRepositoryAnalyzer):
    __doc__ = '\n    Analysis plug-in for mercurial repositories.\n    '

    def count_repo_branches(self, repo_path: str, remote: str) -> None:
        """
        Counts the repository's branches.
        :param repo_path: path to the repository root.
        :param remote: remote uri of the branches
        :return: None
        """
        branches = subprocess.check_output('cd ' + repo_path + ';hg branches | wc -l', shell=True)
        self.get_details(remote)['branch_count'] = int(branches)

    def count_repo_contributors(self, repo_path: str, remote: str) -> None:
        """
        Counts the repository's contributors.
        :param repo_path: path to the repository root.
        :param remote: remote uri of the branches
        :return: None
        """
        contributors = subprocess.check_output('cd ' + repo_path + ';hg log --template "{author|person}\n" | sort | uniq | wc -l', shell=True)
        self.get_details(remote)['contributors'] = int(contributors)

    def extract_repo_url(self, repo_path: str) -> str:
        """
        Extracts the Remote URL from a given SVN repository-path.
        :param repo_path: path to the repository root.
        :return: Remote URL
        """
        try:
            return subprocess.check_output('cd ' + repo_path + ';hg paths default', shell=True).decode('utf-8').rstrip('\n')
        except subprocess.CalledProcessError:
            return ''

    def extract_last_repo_update(self, repo_path: str, remote: str) -> None:
        """
        Extracts the repository's last update-timestamp.
        :param repo_path: path to the repository root.
        :param remote: remote uri of the branches
        :return: None
        """
        timestamp = subprocess.check_output('cd ' + repo_path + ';hg log --limit 1 --template \'{date(date, "%s")}\'', shell=True)
        self.get_details(remote)['last_update'] = int(timestamp)

    def _analyze(self, path: str, repo_details: dict) -> None:
        self._repo_details = repo_details
        for folder in os.listdir(path):
            current_path = path + '/' + folder + ''
            logging.info('[MercurialRepositoryAnalyzer]: Analyzing:' + current_path)
            origin_url = self.extract_repo_url(current_path)
            if origin_url != '':
                self.count_repo_contributors(current_path, origin_url)
                self.count_repo_branches(current_path, origin_url)
                self.extract_last_repo_update(current_path, origin_url)
                yield (
                 current_path, origin_url)
            else:
                logging.warning('[MercurialRepositoryAnalyzer]: ' + current_path + ' is not a valid repository...')

    def analyzes(self):
        return 'hg'