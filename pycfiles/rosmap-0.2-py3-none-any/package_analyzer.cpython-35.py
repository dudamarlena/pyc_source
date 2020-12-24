# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/robotics/rosmap/rosmap/package_analyzers/package_analyzer.py
# Compiled at: 2019-02-05 11:52:53
# Size of source mod 2**32: 2132 bytes
from abc import ABCMeta, abstractmethod
import os

class PackageAnalyzer(object):
    __doc__ = '\n    Abstract base class for plug-ins seeking to implement package analysis.\n    '
    __metaclass__ = ABCMeta

    def __init__(self, settings):
        """
        Creates a new instance of a package-analyzer class.
        :param settings: settings containing information for the plug-ins.
        """
        self._settings = settings

    def add_dependency(self, dependant: str, dependency: str, packages: dict) -> None:
        """
        Adds a dependency
        :param dependant: The package that depends on the dependency
        :param dependency: The package that the dependant is dependent on.
        :param packages: The packages and depdendencies of this repository (key: package, value: list of dependencies).
        :return: None
        """
        if dependant not in packages:
            packages[dependant] = dict()
        if 'dependencies' not in packages[dependant]:
            packages[dependant]['dependencies'] = list()
        packages[dependant]['name'] = dependant
        packages[dependant]['dependencies'].append(dependency)

    @abstractmethod
    def _analyze(self, path: str) -> dict:
        """
        Analyze the current path for packages (recursively)
        :param path: Path to the repository that possibly contains files.
        :return: Dictionary with package-names and dependencies.
        """
        raise NotImplementedError

    def analyze(self, path: str) -> list:
        return list(self._analyze(path).values())

    def search_files(self, path: str, pattern: str) -> list:
        """
        Searches for files recursively in the file system matching the provided pattern.
        :param path: The path to search in.
        :param pattern: The pattern to search for.
        :return: A list of paths to the found files.
        """
        filellist = []
        for root, dirs, files in os.walk(path):
            for name in files:
                if name.endswith(pattern):
                    filellist.append(os.path.join(root, str(pattern)))

        return filellist