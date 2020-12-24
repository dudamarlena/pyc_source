# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/quincy/Code/valuehorizon-people/people/tests/runtests.py
# Compiled at: 2015-05-27 12:16:54
"""
This script is a trick to setup a fake Django environment, since this reusable
app will be developed and tested outside any specifiv Django project.

Via ``settings.configure`` you will be able to set all necessary settings
for your app and run the tests as if you were calling ``./manage.py test``.

"""
import re, sys
from django.conf import settings
import coverage
from fabric.api import abort, lcd, local
from fabric.colors import green, red
import people.settings.test_settings as test_settings
if not settings.configured:
    settings.configure(**test_settings.__dict__)
from django_coverage.coverage_runner import CoverageRunner
from django_nose import NoseTestSuiteRunner

class NoseCoverageTestRunner(CoverageRunner, NoseTestSuiteRunner):
    """Custom test runner that uses nose and coverage"""

    def run_tests(self, *args, **kwargs):
        results = super(NoseCoverageTestRunner, self).run_tests(*args, **kwargs)
        coverage._the_coverage.data.write_file('.coverage')
        return results


def runtests(*test_args):
    failures = NoseCoverageTestRunner(verbosity=2, interactive=True).run_tests(test_args)
    with lcd(settings.COVERAGE_REPORT_HTML_OUTPUT_DIR):
        total_line = local('grep -n Total index.html', capture=True)
        match = re.search('^(\\d+):', total_line)
        total_line_number = int(match.groups()[0])
        percentage_line_number = total_line_number + 4
        percentage_line = local(('awk NR=={0} index.html').format(percentage_line_number), capture=True)
        match = re.search('<td>(\\d.+)%</td>', percentage_line)
        percentage = float(match.groups()[0])
    if percentage < 100:
        pass
    print green(('Coverage is {0}%').format(percentage))
    sys.exit(failures)


if __name__ == '__main__':
    runtests(*sys.argv[1:])