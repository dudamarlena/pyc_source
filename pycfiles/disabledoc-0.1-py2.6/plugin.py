# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/disabledoc/plugin.py
# Compiled at: 2011-06-28 18:47:58
import os
from nose.plugins import Plugin

class DisableDocstring(Plugin):
    """Tells unittest not to use docstrings as test names."""
    name = 'disable-docstring'

    def options(self, parser, env=os.environ):
        super(DisableDocstring, self).options(parser, env=env)
        parser.add_option('--disable-docstring', action='store_true', help=DisableDocstring.__doc__)

    def configure(self, options, conf):
        super(DisableDocstring, self).configure(options, conf)
        if options.disable_docstring:
            self.enabled = True
        if not self.enabled:
            return

    def describeTest(self, test):
        return '(%s) %s' % (test, test.test._testMethodName)