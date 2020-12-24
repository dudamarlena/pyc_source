# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/softwarefabrica/django/utils/runners.py
# Compiled at: 2009-11-08 05:19:13
from django.conf import settings
from django.test.simple import run_tests as django_test_runner
from django.test.simple import run_tests
from django.db.models.loading import get_app, get_apps

def run_tests(test_labels, verbosity=1, interactive=True, extra_tests=None, **kwargs):
    """
    Test runner that only runs tests for the apps listed
    in ``settings.TEST_APPS``.
    ``settings.TEST_APPS`` must be a list of app labels, as defined in
    http://docs.djangoproject.com/en/dev/topics/testing/#defining-a-test-runner
    """
    extra_tests = extra_tests or []
    app_labels = getattr(settings, 'TEST_APPS', test_labels)
    return django_test_runner(app_labels, verbosity=verbosity, interactive=interactive, extra_tests=extra_tests, **kwargs)


def profile_tests(*args, **kwargs):
    """Test runner to perform profiling."""
    try:
        import cProfile as profile
    except ImportError:
        import profile

    prof_file = getattr(settings, 'TEST_PROFILE', None)
    profile.runctx('run_tests(*args, **kwargs)', {'run_tests': run_tests, 'args': args, 'kwargs': kwargs}, {}, prof_file)
    return


def hotshot_profile_tests(*args, **kwargs):
    """
    Test runner to perform profiling with the hotshot profiler.

    To view profiling results with KCacheGrind, run:

    hotshot2calltree hotshot_tests.prof > cachegrind.out.01
    """
    import hotshot
    prof_file = getattr(settings, 'TEST_PROFILE', None)
    prof = hotshot.Profile(prof_file)
    prof.runctx('run_tests(*args, **kwargs)', {'run_tests': run_tests, 'args': args, 'kwargs': kwargs}, {})
    return