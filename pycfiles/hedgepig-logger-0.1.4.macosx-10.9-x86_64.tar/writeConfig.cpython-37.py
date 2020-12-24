# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/anaconda3/lib/python3.7/site-packages/hedgepig_logger/writeConfig.py
# Compiled at: 2019-04-12 16:58:02
# Size of source mod 2**32: 776 bytes
"""
Write a set of configuration options from the command line
"""
from . import log
import argparse
if __name__ == '__main__':

    def _cli():
        parser = argparse.ArgumentParser()
        parser.add_argument('-o', nargs=2, action='append')
        parser.add_argument('-t', dest='title')
        parser.add_argument('-l', '--logfile', dest='logfile', help='(REQUIRED) name of file to write configuration contents to',
          default=None)
        options = parser.parse_args()
        if not options.logfile:
            parser.print_help()
            exit()
        return options


    options = _cli()
    log.start(logfile=(options.logfile))
    log.writeConfig(settings=(options.o),
      title=(options.title))
    log.stop()