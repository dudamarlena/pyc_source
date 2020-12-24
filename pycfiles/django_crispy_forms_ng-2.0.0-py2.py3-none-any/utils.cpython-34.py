# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/uranusjr/Documents/programming/python/django-crispy-forms/django-crispy-forms-ng/crispy_forms/tests/utils.py
# Compiled at: 2015-04-08 10:06:22
# Size of source mod 2**32: 3572 bytes
__all__ = ('override_settings', 'setup')
try:
    from django import setup
except ImportError:

    def setup():
        pass


try:
    from django.test.runner import DiscoverRunner
except ImportError:
    from django.test.simple import DjangoTestSuiteRunner

    class DiscoverRunner(DjangoTestSuiteRunner):

        def run_tests(self, tests, *args, **kwargs):
            tests = [test.replace('crispy_forms.tests.', 'crispy_forms.') for test in tests]
            return super(DiscoverRunner, self).run_tests(tests, *args, **kwargs)


try:
    from django.template import engines

    def get_template_from_string(s):
        return engines['django'].from_string(s)


except ImportError:
    from django.template import loader

    def get_template_from_string(s):
        return loader.get_template_from_string(s)


try:
    from django.test.utils import override_settings
except ImportError:
    from django.conf import settings, UserSettingsHolder
    from django.utils.functional import wraps

    class override_settings(object):
        __doc__ = "\n        Acts as either a decorator, or a context manager. If it's a decorator\n        it takes a function and returns a wrapped function. If it's a\n        contextmanager it's used with the ``with`` statement. In either event\n        entering/exiting are called before and after, respectively,\n        the function/block is executed.\n\n        This class was backported from Django 1.5\n\n        As django.test.signals.setting_changed is not supported in 1.3,\n        it's not sent on changing settings.\n        "

        def __init__(self, **kwargs):
            self.options = kwargs
            self.wrapped = settings._wrapped

        def __enter__(self):
            self.enable()

        def __exit__(self, exc_type, exc_value, traceback):
            self.disable()

        def __call__(self, test_func):
            from django.test import TransactionTestCase
            if isinstance(test_func, type):
                if not issubclass(test_func, TransactionTestCase):
                    raise Exception('Only subclasses of Django SimpleTestCase can be decorated with override_settings')
                original_pre_setup = test_func._pre_setup
                original_post_teardown = test_func._post_teardown

                def _pre_setup(innerself):
                    self.enable()
                    original_pre_setup(innerself)

                def _post_teardown(innerself):
                    original_post_teardown(innerself)
                    self.disable()

                test_func._pre_setup = _pre_setup
                test_func._post_teardown = _post_teardown
                return test_func

            @wraps(test_func)
            def inner(*args, **kwargs):
                with self:
                    return test_func(*args, **kwargs)

            return inner

        def enable(self):
            override = UserSettingsHolder(settings._wrapped)
            for key, new_value in self.options.items():
                setattr(override, key, new_value)

            settings._wrapped = override

        def disable(self):
            settings._wrapped = self.wrapped