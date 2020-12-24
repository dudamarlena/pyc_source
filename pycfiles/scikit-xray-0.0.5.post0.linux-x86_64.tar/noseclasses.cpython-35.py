# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/edill/mc/lib/python3.5/site-packages/skxray/testing/noseclasses.py
# Compiled at: 2016-03-04 05:19:32
# Size of source mod 2**32: 4590 bytes
"""
This module is for decorators related to testing.

Much of this code is inspired by the code in matplotlib.  Exact copies
are noted.
"""
from __future__ import absolute_import, division, print_function
import six, os
from nose.plugins.errorclass import ErrorClass, ErrorClassPlugin

class KnownFailureDidNotFailTest(Exception):
    __doc__ = 'Raise this exception to mark a test should have failed but did not.'


class KnownFailureTest(Exception):
    __doc__ = 'Raise this exception to mark a test as a known failing test.'


class KnownFailure(ErrorClassPlugin):
    __doc__ = "Plugin that installs a KNOWNFAIL error class for the\n    KnownFailureClass exception.  When KnownFailureTest is raised,\n    the exception will be logged in the knownfail attribute of the\n    result, 'K' or 'KNOWNFAIL' (verbose) will be output, and the\n    exception will not be counted as an error or failure.\n\n    "
    enabled = True
    knownfail = ErrorClass(KnownFailureTest, label='KNOWNFAIL', isfailure=False)

    def options(self, parser, env=os.environ):
        env_opt = 'NOSE_WITHOUT_KNOWNFAIL'
        parser.add_option('--no-knownfail', action='store_true', dest='noKnownFail', default=env.get(env_opt, False), help='Disable special handling of KnownFailureTest exceptions')

    def configure(self, options, conf):
        if not self.can_configure:
            return
        self.conf = conf
        disable = getattr(options, 'noKnownFail', False)
        if disable:
            self.enabled = False