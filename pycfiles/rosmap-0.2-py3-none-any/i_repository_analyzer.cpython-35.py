# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/robotics/github_repository_cloner/repository_analyzers/offline/i_repository_analyzer.py
# Compiled at: 2019-02-05 07:28:59
# Size of source mod 2**32: 647 bytes
from abc import ABCMeta, abstractmethod

class IRepositoryAnalyzer(object):
    __doc__ = '\n    Interface for classes implementing Repository-analysis.\n    '
    __metaclass__ = ABCMeta

    @abstractmethod
    def analyze_repositories(self, path: str, repo_details: dict) -> None:
        """
        Analyzes all repositories directly under the root of the given path (does not recurse).
        :param path: Path to the repositories.
        :param repo_details: Details about the repositories.
        :return: None
        """
        raise NotImplementedError

    @abstractmethod
    def analyzes(self) -> str:
        raise NotImplementedError