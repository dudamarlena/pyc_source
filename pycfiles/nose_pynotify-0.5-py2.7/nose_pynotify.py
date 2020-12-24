# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/nose_pynotify.py
# Compiled at: 2011-08-04 19:58:32
"""
This module implements a pynotify-based notification system for nose tests.
Please see README.md for licensing info, an installation guide, and usage.
"""
import pynotify, os, sys
from nose.plugins import Plugin

class PyNotify(Plugin):
    """Subclass of nose.plugins.Plugin that displays a notification at the end
  of test suites, whenever enabled."""
    enabled = False
    name = 'pynotify'
    score = 2

    def __init__(self):
        """Constructor"""
        super(PyNotify, self).__init__()
        self.show_each_error = False
        self.show_each_failure = False
        self.cwd = os.getcwd()

    def addError(self, test, err):
        """Called upon encountering an error"""
        if self.show_each_error:
            title = test.shortDescription() or self.cwd
            n = pynotify.Notification(title, 'Error: ' + str(err[0].__name__) + '\n' + str(err[1]), 'gtk-no')
            n.show()

    def addFailure(self, test, err):
        """Called upon encountering a failure"""
        if self.show_each_failure:
            title = test.shortDescription() or self.cwd
            n = pynotify.Notification(title, 'Failed: ' + str(err[0].__name__) + '\n' + str(err[1]), 'gtk-no')
            n.show()

    def begin(self):
        """Called before running any tests, used for initialization"""
        pynotify.init(self.cwd)

    def configure(self, options, conf):
        """Configure the plugin based on provided options"""
        Plugin.configure(self, options, conf)
        if options.show_each_error:
            self.show_each_error = True
        if options.show_each_failure:
            self.show_each_failure = True

    def options(self, parser, env):
        """Called to allow plugin to register command line options with the parser"""
        Plugin.options(self, parser, env)
        parser.add_option('--show-each-error', default=env.get('NOSE_SHOW_EACH_ERROR'), action='store_true', dest='show_each_error', help='Produce a notification event on each error encountered while testing [NOSE_SHOW_EACH_ERROR]')
        parser.add_option('--show-each-failure', default=env.get('NOSE_SHOW_EACH_FAILURE'), action='store_true', dest='show_each_failure', help='Produce a notification event on each failure encountered while testing [NOSE_SHOW_EACH_FAILURE]')

    def finalize(self, result):
        """Called upon the completion of all tests"""
        errors = len(result.errors)
        failures = len(result.failures)
        successes = result.testsRun - errors - failures
        icon_name = 'gtk-yes' if result.wasSuccessful() else 'gtk-no'
        msg = '%s success%s, %s error%s, %s failure%s' % (
         successes,
         self.plural(successes, special=True),
         errors,
         self.plural(errors),
         failures,
         self.plural(failures))
        n = pynotify.Notification(self.cwd, msg, icon_name)
        n.show()

    def plural(self, n, special=False):
        """Returns empty string if n == 1, otherwise the 's' needed as a suffix"""
        suffix = 's' if not special else 'es'
        if n == 0 or n > 1:
            return suffix
        return ''