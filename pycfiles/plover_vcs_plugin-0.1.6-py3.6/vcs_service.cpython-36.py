# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/plover_vcs/vcs/vcs_service.py
# Compiled at: 2020-04-03 01:04:01
# Size of source mod 2**32: 594 bytes
from abc import ABC, abstractmethod

class VcsService(ABC):

    def __init__(self, repo: str):
        """
        Creates the VcsService
        :param repo: repo path
        """
        pass

    @abstractmethod
    def commit(self, file: str, message: str):
        """
        Commits the given file to the underlying repo with the given message
        :param file: file to commit
        :param message: commit message
        """
        pass

    @abstractmethod
    def diff(self, file: str) -> str:
        """
        Commits the given file.
        :param file: file to commit
        :return:
        """
        pass