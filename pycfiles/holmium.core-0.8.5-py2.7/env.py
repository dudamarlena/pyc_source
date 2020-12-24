# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/holmium/core/env.py
# Compiled at: 2016-02-28 21:16:09
"""
utilities for managing the holmium runtime
environment
"""
import atexit, copy, sys
from nose.plugins.skip import SkipTest
from six import reraise
from holmium.core.config import configure

class LazyWebDriver(object):
    """
    lazily initializes the webdriver on the first
    attribute access
    """

    def __init__(self, driver_cls, holmium_config):
        self._driver_cls = driver_cls
        self._holmium_config = holmium_config
        self._instance = None
        return

    def __getattribute__(self, item):
        safe_getter = lambda i: object.__getattribute__(self, i)
        safe_setter = lambda i, v: object.__setattr__(self, i, v)
        try:
            return object.__getattribute__(self, item)
        except AttributeError:
            instance = safe_getter('_instance')
            if not instance:
                try:
                    args = configure(safe_getter('_holmium_config'))
                    instance = safe_getter('_driver_cls')(**args)
                except:
                    traceback = sys.exc_info()[2]
                    browser = safe_getter('_holmium_config').browser
                    reraise(SkipTest, SkipTest('unable to initialize driver (name: %s)' % (browser.strip() or 'None')), traceback)

                safe_getter('_post_create_callback')()
                safe_setter('_instance', instance)
            return getattr(instance, item)

    def __eq__(self, other):
        return other and self._driver_cls == other._driver_cls

    def _post_create_callback(self):
        """
        register the driver to be shutdown on process exit
        """
        atexit.register(object.__getattribute__(self, 'safe_quit'))

    def safe_quit(self):
        """
        quit the driver if the instance was initialized
        """
        try:
            try:
                instance = object.__getattribute__(self, '_instance')
                if instance:
                    instance.quit()
            except SkipTest:
                pass

        finally:
            object.__setattr__(self, '_instance', None)

        return

    def safe_clear(self):
        """
        clear the cookies if the driver was initialized
        """
        try:
            self.delete_all_cookies()
        except SkipTest:
            pass


class LazyWebDriverList(list):
    """
    fake-ish list to be used to lazily
    initialize new drivers based on the
    first one created
    """

    def __init__(self, *a, **k):
        list.__init__(self, *a, **k)
        self.append(0)

    def __getitem__(self, item):
        if item == 0:
            return ENV.get('driver', None)
        else:
            try:
                return list.__getitem__(self, item)
            except IndexError:
                if ENV.get('driver', None):
                    driver = copy.copy(ENV['driver'])
                    driver._instance = None
                    self.insert(item, driver)
                    return driver
                return

            return

    def __iter__(self):
        yield ENV['driver']
        for item in self[1:]:
            yield item


ENV = {}