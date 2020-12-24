# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/xaralis/Workspace/elladev/ella/test_ella/__init__.py
# Compiled at: 2013-07-24 08:14:41
"""
In this package, You can find test environment for Ella unittest project.
As only true unittest and "unittest" (test testing programming unit, but using
database et al) are there, there is not much setup around.

If You're looking for example project, take a look into example_project directory.
"""
import os
test_runner = None
old_config = None
os.environ['DJANGO_SETTINGS_MODULE'] = 'test_ella.settings'

def setup():
    global old_config
    global test_runner
    from django.test.simple import DjangoTestSuiteRunner
    from ella.utils.installedapps import call_modules
    test_runner = DjangoTestSuiteRunner()
    test_runner.setup_test_environment()
    old_config = test_runner.setup_databases()
    call_modules(('register', ))


def teardown():
    from shutil import rmtree
    from django.conf import settings
    test_runner.teardown_databases(old_config)
    test_runner.teardown_test_environment()
    rmtree(settings.MEDIA_ROOT, ignore_errors=True)