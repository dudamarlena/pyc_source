# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ajdiaz/env/mole/lib/python2.7/site-packages/mole/script/client.py
# Compiled at: 2012-07-12 06:03:29
"""The scripts module provide and endpoint for console scripts.
"""
import os, sys, signal, argparse
from setproctitle import setproctitle
from mole.client import Client
from mole.script import Script
from mole.planner import Planner
from mole.helper import read_conf
from mole.helper import read_args
from mole.helper import AttrDict
DEFAULT_DIRCFG = '/etc/mole/'

class ScriptClient(object):
    """Main class to handle the client script"""

    def __call__(self):
        """Run the script"""
        args = read_args([
         (
          '-p', '--port', 'Use specific port to connect', int, 9900),
         (
          '-H', '--host', 'Use the host address to connect to', str, '127.0.0.1')], [
         'search'])
        config = AttrDict({'client': AttrDict({'host': args.host, 'port': args.port}), 
           'search': args.search})
        self.client = Client.from_type('basic', config.client)
        try:
            for x in self.client.run(config.search):
                print x

        except KeyboardInterrupt:
            self.client.cancel()


def main():
    client = ScriptClient()
    client()


if __name__ == '__main__':
    main()