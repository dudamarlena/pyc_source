# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\correspondence_tables\bin\correspondence_tables_cli.py
# Compiled at: 2020-01-19 13:34:44
# Size of source mod 2**32: 556 bytes
"""correspondence_tables CLI.

Usage:
  correspondence_tables-cli regenerate <dirpath>

Options:
  -h --help     Show this screen.
  --version     Show version.

"""
from docopt import docopt
from correspondence_tables import generate_all
import sys

def main():
    try:
        args = docopt(__doc__, version='0.2')
        generate_all(args['<dirpath>'])
    except KeyboardInterrupt:
        print('Terminating CLI')
        sys.exit(1)


if __name__ == '__main__':
    main()