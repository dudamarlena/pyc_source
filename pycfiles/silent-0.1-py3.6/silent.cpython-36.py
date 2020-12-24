# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/silent/silent.py
# Compiled at: 2018-03-03 09:01:17
# Size of source mod 2**32: 1432 bytes
import argparse, sys
from .client import Client

class Silent:
    PROJECT_URL = 'https://github.com/vinyasns/silent'

    def __init__(self):
        self._parser = None
        self._setup_parsers()
        self._args = self._parser.parse_args()

    def _setup_parsers(self):
        self._parser = argparse.ArgumentParser(description='A commandline client for file.io',
          epilog=('Project Page: ` {0} `'.format(Silent.PROJECT_URL)),
          formatter_class=(argparse.RawTextHelpFormatter))
        self._parser.add_argument('file', help='File to be uploaded anonymously')
        self._parser.add_argument('-e', '--expiry', help='Expiry time for the file on server.\nFollowing formats are allowed,\nNw, expires in N weeks\nNm, expires in N months\nNy, expires in N years\nWhere N is a positive integer')

    def run(self):
        if not self._args.file:
            self._parser.print_help()
            print(':(')
            sys.exit(1)
        silent = Client(self._args)
        silent.run()


def main():
    app = Silent()
    app.run()


if __name__ == '__main__':
    main()