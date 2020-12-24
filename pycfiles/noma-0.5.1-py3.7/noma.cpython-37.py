# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/noma/noma.py
# Compiled at: 2019-09-25 06:48:41
# Size of source mod 2**32: 1561 bytes
"""Noma [node management]

Usage:  noma start
        noma stop
        noma check
        noma logs
        noma info
        noma lnd create
        noma lnd backup
        noma lnd autounlock
        noma lnd autoconnect [<path>]
        noma lnd savepeers
        noma lnd connectapp
        noma lnd connectstring
        noma (-h|--help)
        noma --version

Options:
  -h --help     Show this screen.
  --version     Show version.

"""
import os
from docopt import docopt
from noma import lnd
from noma import node

def lnd_fn(args):
    """
    lnd related functionality
    """
    if args['create']:
        lnd.check_wallet()
    else:
        if args['autounlock']:
            lnd.autounlock()
        else:
            if args['backup']:
                lnd.backup()
            else:
                if args['autoconnect']:
                    lnd.autoconnect(args['<path>'])
                else:
                    if args['savepeers']:
                        lnd.savepeers()
                    else:
                        if args['connectstring']:
                            lnd.connectstring()


def node_fn(args):
    """
    node related functionality
    """
    if args['info']:
        node.info()
    else:
        if args['start']:
            node.start()
        else:
            if args['stop']:
                node.stop()
            else:
                if args['logs']:
                    node.logs()
                else:
                    if args['check']:
                        node.check()


def main():
    """
    main noma entrypoint function
    """
    args = docopt(__doc__, version='Noma v0.5.1')
    if os.geteuid() == 0:
        if args['lnd']:
            lnd_fn(args)
        else:
            node_fn(args)
    else:
        print('Sorry! You must be root')


if __name__ == '__main__':
    main()