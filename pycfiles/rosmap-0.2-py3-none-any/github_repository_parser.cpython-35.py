# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/robotics/rosmap/rosmap/repository_parsers/github_repository_parser.py
# Compiled at: 2019-04-12 11:02:21
# Size of source mod 2**32: 1044 bytes
from rosmap.api_bindings.github_api_bindings import GithubApiBindings
from .i_repository_parser import IRepositoryParser

class GithubRepositoryParser(IRepositoryParser):
    __doc__ = '\n    Parses repository-URLs from GitHub using the GitHub-search API.\n    '

    def __init__(self, settings: dict):
        """
        Creates a new instance of the GithubRepositoryParser class.
        :param settings: Settings dict containing keys github_username, github_password (token works as well), as well as
        search-API rate limit.
        """
        self._GithubRepositoryParser__api_bindings = GithubApiBindings(settings['github_username'], settings['github_password'], settings['github_search_rate_limit'])
        self._GithubRepositoryParser__settings = settings

    def parse_repositories(self, repository_dict: dict) -> None:
        repository_dict['git'].update(self._GithubRepositoryParser__api_bindings.get_urls_of_topic(self._GithubRepositoryParser__settings['github_search_topic']))