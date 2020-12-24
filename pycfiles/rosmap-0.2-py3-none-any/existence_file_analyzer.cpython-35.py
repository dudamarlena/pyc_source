# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/robotics/rosmap/rosmap/file_analyzers/existence_file_analyzer.py
# Compiled at: 2019-02-05 11:52:53
# Size of source mod 2**32: 1387 bytes
from .i_file_analyzer import IFileAnalyzer

class ExistenceFileAnalyzer(IFileAnalyzer):
    __doc__ = '\n    Checks if files exist, and saves true or false to the repo_detail.\n    '

    def analyze_files(self, path_list, repo_detail: dict):
        for path in path_list:
            self._ExistenceFileAnalyzer__analyze_file(path, repo_detail)

    def _ExistenceFileAnalyzer__analyze_file(self, path: str, repo_details: dict) -> None:
        file = path.split('/')[(-1)]
        repo_details['readme'] = repo_details['readme'] or 'readme' in file.lower()
        repo_details['changelog'] = repo_details['changelog'] or 'changelog' in file.lower()
        repo_details['continuous_integration'] = repo_details['continuous_integration'] or '.travis.yml' in file.lower() or '.gitlab-ci.yml' in file.lower() or 'bitbucket-pipelines' in file.lower()
        repo_details['rosinstall'] = repo_details['rosinstall'] or '.rosinstall' in file.lower()

    def initialize_fields(self, repo_detail: dict) -> None:
        details = ['readme', 'changelog', 'continuous_integration', 'rosinstall']
        for detail in details:
            try:
                repo_detail[detail]
            except KeyError:
                repo_detail[detail] = False