# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/robotics/rosmap/rosmap/repository_cloners/i_repository_cloner.py
# Compiled at: 2019-02-05 11:52:53
# Size of source mod 2**32: 785 bytes
from abc import ABCMeta, abstractmethod

class IRepositoryCloner(object):
    __doc__ = '\n    Interface for classes implementing cloning-functionality for different repository-types.\n    '
    __metaclass__ = ABCMeta

    @abstractmethod
    def clone_repositories(self, repository_set: set) -> None:
        """
        Clones repositories from URLs provided by repository set
        :param repository_set: A set containing repository-URLs.
        :return: None
        """
        raise NotImplementedError

    @abstractmethod
    def clones(self) -> str:
        """
        Returns which type of repository is cloned by this cloner.
        :return: A string designating which type of repository is cloned (e.g. "git", "hg", "svn", ...)
        """
        raise NotImplementedError