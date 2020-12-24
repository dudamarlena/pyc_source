# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/andrewcrosio/projects/expenses/virtualenv/lib/python3.4/site-packages/diffcoverage/settings.py
# Compiled at: 2016-02-03 09:01:46
# Size of source mod 2**32: 354 bytes
"""Settings file"""
import re
COVERAGE_PATH = '.coverage'
IGNORED_NAME_PORTIONS = [re.compile('(?:^|[_.-])test.py'), re.compile('(?:\\b|^)docs/')]
REQUIRED_NAME_PORTIONS = [re.compile('\\.py$')]
OUTPUT_COVERAGE_DOC = 'diff_coverage_html'
COMPARE_WITH_BRANCH = 'master'
XML_REPORT_FILE = 'coverage.xml'
HTML_REPORT_DIR = 'coverage_html'