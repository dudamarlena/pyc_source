# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/robotics/github_repository_cloner/repository_analyzers/online/i_scs_analyzer.py
# Compiled at: 2019-01-31 09:12:31
# Size of source mod 2**32: 707 bytes
from abc import ABCMeta, abstractmethod

class ISCSRepositoryAnalyzer(object):
    __doc__ = '\n    Interface for classes implementing remote analysis of repositories from social coding sites (scs).\n    '
    __metaclass__ = ABCMeta

    @abstractmethod
    def analyze_repositories(self, repo_details: dict) -> None:
        """
        Analyzes repositories listed in repo_details.
        """
        raise NotImplementedError

    @abstractmethod
    def analyzes(self) -> str:
        """
        Returns which type of remote is analyzed by this analyzer.
        :return: A string designating which type of repository is cloned (e.g. "bitbucket", "github",...)
        """
        raise NotImplementedError