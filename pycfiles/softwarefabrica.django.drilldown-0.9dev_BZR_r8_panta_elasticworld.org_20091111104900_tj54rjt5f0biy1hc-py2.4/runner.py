# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/softwarefabrica/django/drilldown/tests/runner.py
# Compiled at: 2009-09-16 05:57:52
from django.conf import settings
from django.test.simple import run_tests as django_test_runner
from django.db.models.loading import get_app, get_apps

def run_tests(test_labels, verbosity=1, interactive=True, extra_tests=None, **kwargs):
    """Test runner that only runs tests for the apps listed
    in ``settings.TEST_APPS``.
    ``settings.TEST_APPS`` must be a list of app labels, as defined in
    http://docs.djangoproject.com/en/dev/topics/testing/#defining-a-test-runner
    """
    extra_tests = extra_tests or []
    app_labels = getattr(settings, 'TEST_APPS', test_labels)
    return django_test_runner(app_labels, verbosity=verbosity, interactive=interactive, extra_tests=extra_tests, **kwargs)