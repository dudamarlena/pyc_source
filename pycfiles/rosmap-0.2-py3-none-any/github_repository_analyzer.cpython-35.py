# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/robotics/github_repository_cloner/repository_analyzers/online/github_repository_analyzer.py
# Compiled at: 2019-02-01 11:27:34
# Size of source mod 2**32: 3738 bytes
import dateutil.parser, logging
from .i_scs_analyzer import ISCSRepositoryAnalyzer
from api_bindings.github_api_bindings import GithubApiBindings

class GithubRepositoryAnalyzer(ISCSRepositoryAnalyzer):
    __doc__ = '\n    Analyzes repositories remotely on GitHub and extracts GitHub-specific information.\n    '

    def __init__(self, settings: dict):
        """
        Creates a new instance of the GithubRepositoryAnalyzer class.
        :param settings: settings containing github_username, github_password, and github_api_rate_limit
        """
        self._GithubRepositoryAnalyzer__api_bindings = GithubApiBindings(settings['github_username'], settings['github_password'], settings['github_api_rate_limit'])

    @staticmethod
    def initialize_values(repo_details: dict) -> None:
        """
        Initializes all values that might be needed in order to avoid exceptions.
        :param repo_details: details associated with the analyzed repository.
        :return:
        """
        if 'closed_pull_requests' not in repo_details:
            repo_details['closed_pull_requests'] = 0
        if 'issue_durations' not in repo_details:
            repo_details['issue_durations'] = list()
        if 'open_pull_requests' not in repo_details:
            repo_details['open_pull_requests'] = 0
        if 'open_issues' not in repo_details:
            repo_details['open_issues'] = 0

    def count_repo_stars(self, url: str, repo_details: dict) -> None:
        """
        Counts the stargazers for the repository.
        :param url: URL to the repository.
        :param repo_details: details of the repository associated with the URL
        :return:
        """
        repo_details['stars'] = self._GithubRepositoryAnalyzer__api_bindings.get_stargazer_count(url)

    def count_closed_issues(self, url: str, repo_details: dict) -> None:
        """
        Counts all closed issues and calculats how long they were open. Counts closed pull requests.
        :param  url: URL to the repository.
        :param repo_details: details of the repository associated with the URL
        :return: None
        """
        for issue in self._GithubRepositoryAnalyzer__api_bindings.get_issues(url, 'closed'):
            if self._GithubRepositoryAnalyzer__api_bindings.is_pull_request(issue):
                repo_details['closed_pull_requests'] += 1
            else:
                elapsed_time = dateutil.parser.parse(issue['closed_at']) - dateutil.parser.parse(issue['created_at'])
                repo_details['issue_durations'].append(elapsed_time.total_seconds())

    def count_open_issues(self, url: str, repo_details: dict) -> None:
        """
        Counts open issues and pull requests.
        :param url: URL to the repository to count the open issues.
        :param repo_details: details of the repository associated with the URL
        :return: None
        """
        for issue in self._GithubRepositoryAnalyzer__api_bindings.get_issues(url, 'open'):
            if self._GithubRepositoryAnalyzer__api_bindings.is_pull_request(issue):
                repo_details['open_pull_requests'] += 1
            else:
                repo_details['open_issues'] += 1

    def analyze_repositories(self, repo_details: dict) -> None:
        for url, details in repo_details.items():
            if 'github' in url:
                logging.info('[GithubRepositoryAnalyzer]: Fetching data from ' + url)
                self.initialize_values(details)
                self.count_repo_stars(url, details)
                self.count_closed_issues(url, details)
                self.count_open_issues(url, details)

    def analyzes(self):
        return 'github'