# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/robotics/github_repository_cloner/repository_analyzers/offline/abstract_repository_analyzer.py
# Compiled at: 2019-02-05 10:39:54
# Size of source mod 2**32: 3183 bytes
from repository_analyzers.offline.i_repository_analyzer import IRepositoryAnalyzer
from abc import ABCMeta, abstractmethod
import os

class AbstractRepositoryAnalyzer(IRepositoryAnalyzer):
    __doc__ = '\n    Abstract base class for repository-analysis plug-ins.\n    '
    __metaclass__ = ABCMeta

    def __init__(self, package_analyzers, file_analyzers):
        """
        Constructor for all classes that continue to implement this class.
        :param package_analyzers:
        :param file_analyzers:
        """
        self._repo_details = dict()
        self.package_analyzers = package_analyzers
        self.file_analyzers = file_analyzers

    @abstractmethod
    def _analyze(self, path, repo_details) -> iter:
        """
        Analyzes all repositories based on their repository type, and yield returns the origin URL.
        :param path: Path to the repositories.
        :param repo_details: Details to the repository.
        :return:
        """
        raise NotImplementedError

    def get_details(self, remote: str) -> None:
        """
        Gets the details of a repository based on its remote URL.
        :param remote: Remote URL.
        :return: None
        """
        if remote not in self._repo_details:
            self._repo_details[remote] = dict()
            self._repo_details[remote]['url'] = remote
        return self._repo_details[remote]

    def initialize_details(self, remote: str) -> None:
        """
        Initializes fields for file analyzers.
        :param remote: Remote URL.
        :return: None
        """
        for file_analyzer in self.file_analyzers:
            file_analyzer.initialize_fields(self.get_details(remote))

    def _AbstractRepositoryAnalyzer__process_files(self, directory: str, remote: str) -> None:
        """
        Analyzes all files inside a directory.
        :param directory: Repository root directory.
        :param remote: Remote
        :return: None.
        """
        self.initialize_details(remote)
        filelist = list()
        for path, subdirectory, files in os.walk(directory):
            for name in files:
                filelist.append(os.path.join(path, name))

        for file_anlayzer in self.file_analyzers:
            file_anlayzer.analyze_files(filelist, self.get_details(remote))

    def analyze_repositories(self, path: str, repo_details: dict) -> None:
        for repo_path, remote in self._analyze(path, repo_details):
            self._AbstractRepositoryAnalyzer__analyze_packages(repo_path, remote)
            self._AbstractRepositoryAnalyzer__process_files(repo_path, remote)

    def _AbstractRepositoryAnalyzer__analyze_packages(self, path: str, remote: str) -> None:
        """
        Analyze package-files of a repository.
        :param path: Path to root containing files to analyze.
        :param remote: Remote URL of the repository containing the file.
        :return: None
        """
        for package_analyzer in self.package_analyzers:
            if 'packages' not in self.get_details(remote):
                self.get_details(remote)['packages'] = list()
            self.get_details(remote)['packages'].extend(package_analyzer.analyze(path))