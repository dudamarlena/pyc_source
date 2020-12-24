# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nslocalizer/main.py
# Compiled at: 2019-02-23 14:43:19
# Size of source mod 2**32: 4375 bytes
import sys, argparse
from .version import __version__ as PYLOCALIZER_VERSION
import Helpers.Logger as Logger
import Executor.Executor as Executor

def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser(description='nslocalizer is a tool for identifying unused or missing localization string usage in Xcode projects')
    parser.add_argument('--version',
      help='Displays the version information',
      action='version',
      version=PYLOCALIZER_VERSION)
    parser.add_argument('--project',
      metavar='<Xcode project path>',
      help='specify the path to the .xcodeproj file',
      required=True,
      action='store')
    parser.add_argument('--target',
      metavar='<target name>',
      help='specify the name of targets to analyze, this accepts multiple target names',
      type=str,
      default=(list()),
      required=True,
      action='store',
      nargs='*')
    parser.add_argument('--find-missing',
      help='look for localized strings that are missing from any of the .strings files',
      default=False,
      action='store_true')
    parser.add_argument('--find-unused',
      help='look for localized strings that are not used in the code',
      default=False,
      action='store_true')
    parser.add_argument('--quiet',
      help='Silences all logging output',
      default=False,
      action='store_true')
    parser.add_argument('--verbose',
      help='Adds verbosity to logging output',
      default=False,
      action='store_true')
    parser.add_argument('--ignore',
      help='Specify languages to ignore (by code; eg: German = de).',
      type=str,
      default=(list()),
      nargs='*')
    parser.add_argument('--no-ansi',
      help='Disables the ANSI color codes as part of the logger',
      default=False,
      action='store_true')
    parser.add_argument('--error',
      help='Changes warnings to errors',
      default=False,
      action='store_true')
    parser.add_argument('--debug',
      help=(argparse.SUPPRESS),
      default=False,
      action='store_true')
    args = parser.parse_args(argv)
    Logger.disableANSI(args.no_ansi)
    Logger.enableDebugLogger(args.debug)
    Logger.isVerbose(args.verbose)
    Logger.isSilent(args.quiet)
    ignored_locales = ', '.join(args.ignore)
    Logger.write().info('Ignoring languages: %s' % ignored_locales)
    Executor.run(args)


if __name__ == '__main__':
    main()