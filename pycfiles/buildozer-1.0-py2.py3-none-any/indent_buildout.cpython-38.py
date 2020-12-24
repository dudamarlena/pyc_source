# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/fantomas/dev/buildout-versions-checker-py3/bvc/scripts/indent_buildout.py
# Compiled at: 2020-03-06 05:53:09
# Size of source mod 2**32: 2389 bytes
__doc__ = 'Command line for (re)indenting buildout files'
import logging, sys
from argparse import ArgumentParser
from bvc.configparser import VersionsConfigParser
import bvc.logger as logger

def cmdline(argv=sys.argv[1:]):
    parser = ArgumentParser(description='(Re)indent buildout related files')
    parser.add_argument('sources',
      nargs='*',
      help='The buildout files to (re)indent')
    format_group = parser.add_argument_group('Formatting')
    format_group.add_argument('--indent',
      dest='indentation',
      type=int,
      default=(-1),
      help='Spaces used when indenting "key = value" (default: auto)')
    format_group.add_argument('--sorting',
      dest='sorting',
      default='',
      choices=[
     'alpha', 'ascii', 'length'],
      help='Sorting algorithm used on the keys when writing source file (default: None)')
    verbosity_group = parser.add_argument_group('Verbosity')
    verbosity_group.add_argument('-v',
      action='count',
      dest='verbosity',
      default=1,
      help='Increase verbosity (specify multiple times for more)')
    verbosity_group.add_argument('-q',
      action='count',
      dest='quietly',
      default=0,
      help='Decrease verbosity (specify multiple times for more)')
    if isinstance(argv, str):
        argv = argv.split()
    options = parser.parse_args(argv)
    verbose_logs = {0:100, 
     1:logging.WARNING, 
     2:logging.INFO, 
     3:logging.DEBUG}
    verbosity = min(3, max(0, options.verbosity - options.quietly))
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(verbose_logs[verbosity])
    logger.addHandler(console)
    if not options.sources:
        logger.warning('No files to (re)indent')
        sys.exit(0)
    for source in options.sources:
        config = VersionsConfigParser(indentation=(options.indentation),
          sorting=(options.sorting))
        config_readed = config.read(source)
        if config_readed:
            config.write(source)
            logger.warning('- %s (re)indented at %s spaces.', source, config.indentation)
        else:
            logger.warning('- %s cannot be read.', source)

    sys.exit(0)