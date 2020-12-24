# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/simon/Dropbox/Projects/django-chimps/chimps/runtests/runtests.py
# Compiled at: 2013-09-19 05:33:20
# Size of source mod 2**32: 639 bytes
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'chimps.runtests.settings'
import django
from django.conf import settings
from django.test.utils import get_runner

def main():
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    module_name = 'chimps.tests'
    if django.VERSION[0] == 1:
        if django.VERSION[1] < 6:
            module_name = 'chimps'
    failures = test_runner.run_tests([module_name])
    sys.exit(failures)


if __name__ == '__main__':
    main()