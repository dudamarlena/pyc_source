# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\correspondence_tables\bin\correspondence_tables_cli.py
# Compiled at: 2020-01-19 13:34:44
# Size of source mod 2**32: 556 bytes
__doc__ = 'correspondence_tables CLI.\n\nUsage:\n  correspondence_tables-cli regenerate <dirpath>\n\nOptions:\n  -h --help     Show this screen.\n  --version     Show version.\n\n'
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