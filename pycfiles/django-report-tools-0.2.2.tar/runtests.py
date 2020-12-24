# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/evan/Projects/report_tools/proj/tests/runtests.py
# Compiled at: 2014-02-02 20:55:19
import os, sys
os.environ['DJANGO_SETTINGS_MODULE'] = 'testproj.settings'
test_dir = os.path.dirname(__file__)
sys.path.insert(0, test_dir)
from django.test.utils import get_runner
from django.conf import settings

def runtests():
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=1, interactive=True)
    failures = test_runner.run_tests(['report_tools'])
    sys.exit(bool(failures))


if __name__ == '__main__':
    runtests()