# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/src/behaviourplugin.py
# Compiled at: 2007-12-17 17:06:26
"""

"""
__docformat__ = 'restructuredtext en'
import logging, os, re, sys, textwrap
from nose.plugins.base import Plugin
log = logging.getLogger('nose.plugins.behaviourplugin')

class Specification(Plugin):
    """
        

        """

    def __init__(self):
        """
                
                """
        Plugin.__init__(self)

    def options(self, parser, env=os.environ):
        """
                Add command-line options for this plugin.
                """
        Plugin.options(parser, env=os.environ)

    def help(self):
        """
                Return a string for nose to use when invoked with -h.
                """
        return textwrap.dedent('Enable selection of specifications and behaviours. Also enable of converting names to English phrases for output')

    def configure(self, options, config):
        """
                Configure plugin from command line options.
                """
        Plugin.configure(options, config)

    def wantClass(self, cls):
        """
                Accept the class if its name ends with "_spec" or "Specification".
                """
        if cls.__name__.endswith('_spec') or cls.__name__.endswith('Specification'):
            return True
        else:
            return
        return

    def wantFunction(self, function):
        """
                Accept the function if its name starts with "should" or "Should".
                """
        if function.__name__ == 'runTest':
            return False
        if function.__name__.startswith('should') or function.__name__.startswith('Should'):
            return True
        else:
            return
        return

    def wantMethod(self, method):
        """
                Accept the method if its name starts with "should" or "Should".
                """
        if function.__name__ == 'runTest':
            return False
        if method.__name__.startswith('should') or method.__name__.startswith('Should'):
            return True
        else:
            return
        return