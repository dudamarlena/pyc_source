# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\robotframework_metrics\keyword_stats.py
# Compiled at: 2020-03-14 04:42:30
# Size of source mod 2**32: 872 bytes
from robot.api import ResultVisitor

class KeywordStats(ResultVisitor):
    total_keywords = 0
    passed_keywords = 0
    failed_keywords = 0

    def __init__(self, ignore_library, ignore_type):
        self.ignore_library = ignore_library
        self.ignore_type = ignore_type

    def start_keyword(self, kw):
        keyword_library = kw.libname
        if any((library in keyword_library for library in self.ignore_library)):
            pass
        else:
            keyword_type = kw.type
            if any((library in keyword_type for library in self.ignore_type)):
                pass
            else:
                self.total_keywords += 1
                if kw.status == 'PASS':
                    self.passed_keywords += 1
                else:
                    self.failed_keywords += 1