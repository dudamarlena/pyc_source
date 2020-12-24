# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/robotics/rosmap/rosmap/file_analyzers/cpp_file_analyzer.py
# Compiled at: 2019-02-05 11:52:53
# Size of source mod 2**32: 1329 bytes
from .i_file_analyzer import IFileAnalyzer
import subprocess

class CppFileAnalyzer(IFileAnalyzer):
    __doc__ = 'Analyzes C++ source and header files.'

    def initialize_fields(self, repo_detail: dict) -> None:
        try:
            repo_detail['cpplint_errors']
        except KeyError:
            repo_detail['cpplint_errors'] = 0

    def _CppFileAnalyzer__analyze_file(self, path: str, repo_detail: dict) -> None:
        try:
            cpplint_report = str(subprocess.check_output('cpplint --filter=-whitespace/tab,-whitespace/braces,-build/headerguard,-readability/streams,-build/include_order,-whitespace/newline,-whitespace/labels,-runtime/references ' + path, shell=True, stderr=subprocess.STDOUT))
            if 'Total errors found:' in cpplint_report:
                repo_detail['cpplint_errors'] += int(cpplint_report.split('\n')[(-2)].split(': ')[(-1)])
        except subprocess.CalledProcessError as error:
            cpplint_report = error.output
            repo_detail['cpplint_errors'] += int(cpplint_report.decode('utf-8').split('\n')[(-2)].split(': ')[(-1)])

    def analyze_files(self, path_list: list, repo_detail: dict):
        for file_path in filter(lambda k: k.endswith('.hpp') or k.endswith('.cpp') or k.endswith('.h'), path_list):
            self._CppFileAnalyzer__analyze_file(file_path, repo_detail)