# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/robotics/rosmap/rosmap/repository_parsers/i_repository_parser.py
# Compiled at: 2019-02-05 11:52:53
# Size of source mod 2**32: 445 bytes
from abc import ABCMeta, abstractmethod

class IRepositoryParser(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def parse_repositories(self, repository_dict: dict) -> None:
        """
        Parses repository URLs and adds them to the dictionary.
        :param repository_dict: The dictionary to add the repository URLs to (key: repo-type, value: repo-url)
        :return: None
        """
        raise NotImplementedError