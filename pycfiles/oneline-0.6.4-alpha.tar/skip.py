# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /cygdrive/c/Users/Nad/oneline/oneline/lib/lz4/nose-1.3.4-py2.7.egg/nose/plugins/skip.py
# Compiled at: 2014-09-06 21:58:19
"""
This plugin installs a SKIP error class for the SkipTest exception.
When SkipTest is raised, the exception will be logged in the skipped
attribute of the result, 'S' or 'SKIP' (verbose) will be output, and
the exception will not be counted as an error or failure. This plugin
is enabled by default but may be disabled with the ``--no-skip`` option.
"""
from nose.plugins.errorclass import ErrorClass, ErrorClassPlugin
try:
    from unittest.case import SkipTest
except ImportError:
    try:
        from unittest2.case import SkipTest
    except ImportError:

        class SkipTest(Exception):
            """Raise this exception to mark a test as skipped.
            """
            pass


class Skip(ErrorClassPlugin):
    """
    Plugin that installs a SKIP error class for the SkipTest
    exception.  When SkipTest is raised, the exception will be logged
    in the skipped attribute of the result, 'S' or 'SKIP' (verbose)
    will be output, and the exception will not be counted as an error
    or failure.
    """
    enabled = True
    skipped = ErrorClass(SkipTest, label='SKIP', isfailure=False)

    def options(self, parser, env):
        """
        Add my options to command line.
        """
        env_opt = 'NOSE_WITHOUT_SKIP'
        parser.add_option('--no-skip', action='store_true', dest='noSkip', default=env.get(env_opt, False), help='Disable special handling of SkipTest exceptions.')

    def configure(self, options, conf):
        """
        Configure plugin. Skip plugin is enabled by default.
        """
        if not self.can_configure:
            return
        self.conf = conf
        disable = getattr(options, 'noSkip', False)
        if disable:
            self.enabled = False