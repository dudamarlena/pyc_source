# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sotetsuk/.pyenv/versions/3.5.1/lib/python3.5/site-packages/somecommand/main.py
# Compiled at: 2016-07-23 07:40:25
# Size of source mod 2**32: 518 bytes
"""Some command
Usage:
  somecommand <subcommand>
  somecommand (-h | --help)
  somecommand --version
Options:
  -h --help             Show this screen.
  --version             Show version.
"""
from docopt import docopt
from somecommand.subcommands import foo, bar

def helloworld():
    print('hello world')


def main():
    args = docopt(__doc__, version='some-command 0.0.1')
    if args['<subcommand>'] == 'foo':
        foo()
    else:
        if args['<subcommand>'] == 'bar':
            bar()
        else:
            helloworld()