# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ajdiaz/env/mole/lib/python2.7/site-packages/mole/script/indexer.py
# Compiled at: 2013-01-16 04:51:37
"""The scripts module provide and endpoint for console scripts.
"""
import os, signal, argparse
from setproctitle import setproctitle
from mole.server import Server
from mole.script import Script
from mole.helper import read_conf
from mole.helper import read_args
DEFAULT_DIRCFG = '/etc/mole/'

class ScriptIndexer(object):
    """Main class to handle the indexer script"""

    def __call__(self):
        """Run the script"""
        args = read_args([
         (
          '-C', '--config', 'Use specific config dir', str, None)], [])
        if not args.config:
            args.config = os.getenv('MOLE_CONFIGDIR', None) or DEFAULT_DIRCFG
        config = read_conf(args.config)
        self.indexer = Server.from_type('index', config)
        self.indexer.run()
        try:
            signal.pause()
        except KeyboardInterrupt:
            self.indexer.cancel()

        return


def main():
    indexer = ScriptIndexer()
    indexer()


if __name__ == '__main__':
    main()