# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/robotics/rosmap/rosmap/file_analyzers/i_file_analyzer.py
# Compiled at: 2019-02-05 11:52:53
# Size of source mod 2**32: 457 bytes
from abc import ABCMeta, abstractmethod

class IFileAnalyzer(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def initialize_fields(self, repo_detail: dict) -> None:
        """
        Initialize fields on repo_detail needed for analysis of this file-type.
        :param repo_detail:
        :return:
        """
        raise NotImplementedError

    def analyze_files(self, path_list, repo_detail: dict):
        raise NotImplementedError