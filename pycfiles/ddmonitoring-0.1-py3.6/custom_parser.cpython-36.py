# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ddmonitoring/utils/custom_parser.py
# Compiled at: 2019-11-30 07:59:25
# Size of source mod 2**32: 1710 bytes
import cliff._argparse as _argparse
from cliff.app import App

class CustomParser:

    def __init__(self, description, version, deferred_help):
        """Return an argparse option parser for this application.
        Subclasses may override this method to extend
        the parser with more global options.
        :param description: full description of the application
        :paramtype description: str
        :param version: version number for the application
        :paramtype version: str
        """
        argparse_kwargs = {}
        self.parser = (_argparse.ArgumentParser)(description=description, 
         add_help=False, **argparse_kwargs)
        self.parser.add_argument('--version',
          action='version',
          version=('{0} {1}'.format(App.NAME, version)))
        self.parser.add_argument('--log-file',
          action='store',
          default=None,
          help='Specify a file to log output. Disabled by default.')
        if deferred_help:
            self.parser.add_argument('-h',
              '--help', dest='deferred_help',
              action='store_true',
              help='Show help message and exit.')
        else:
            self.parser.add_argument('-h',
              '--help', action=(help.HelpAction),
              nargs=0,
              default=self,
              help='Show help message and exit.')
        self.parser.add_argument('--debug',
          default=False,
          action='store_true',
          help='Show tracebacks on errors.')