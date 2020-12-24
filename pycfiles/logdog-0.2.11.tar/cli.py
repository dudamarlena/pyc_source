# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/miph/Development/logdog/python-logdog/logdog/cli.py
# Compiled at: 2015-04-25 19:47:14
"""logdog command line interface

Usage:
  logdog [<pipe-namespace>...] [options]
  logdog (-h | --help)
  logdog --version

Arguments:
  <pipe-namespace>          One or more pipe namespaces to be run

Options:
  -h --help                 Show this screen
  --version                 Show version
  -v --verbose              Run in verbose mode
  -l --log-level=<level>    Set internal logging level [default: INFO]
  -f --log-format=<format>  Set internal logging format [default: quiet]
  -c --config=<config>      Configuration file (yaml config)
  -s --sources=<file:...>   Force specify files to be watched
  -H --handler=<handler>    Force set handler for all sources
                            (e.g. --handler=viewers.console)
  --reset-indices           Remove current indices (will reset watching state)
"""
from __future__ import absolute_import, unicode_literals
from docopt import docopt
from logdog.app import Application
from logdog.core.config import ConfigLoader
from logdog.core.log import configure_logging
from logdog.version import __version__

def main():
    arguments = docopt(__doc__, version=(b'logdog {}').format(__version__))
    log_level = arguments.get(b'--log-level').upper()
    log_format = log_custom_format = arguments.get(b'--log-format')
    if log_format not in ('verbose', 'quiet'):
        log_format = b'custom'
    if arguments.get(b'--verbose'):
        log_level = b'DEBUG'
        log_format = b'verbose'
    configure_logging(log_level, log_format, log_custom_format)
    config_path = arguments.get(b'--config')
    loader = ConfigLoader(path=config_path)
    config = loader.load_config(default_only=not config_path)
    try:
        Application(active_namespaces=arguments.get(b'<pipe-namespace>'), config=config, force_handler=arguments.get(b'--handler'), force_sources=arguments.get(b'--sources'), reset_indices=arguments.get(b'--reset-indices')).run()
    except KeyboardInterrupt:
        pass


if __name__ == b'__main__':
    main()