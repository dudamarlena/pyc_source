# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mop/__main__.py
# Compiled at: 2020-04-04 14:54:13
# Size of source mod 2**32: 864 bytes
import sys, pathlib, logging, argparse
import nicfit.logger as addLoggingArgs
from .app import MopApp
from .__about__ import version

class ArgumentParser(argparse.ArgumentParser):

    def __init__(self):
        super().__init__(prog='mop')
        self._initArgs()

    def _initArgs(self):
        self.add_argument('--version', action='version', version=f"%(prog)s {version}")
        addLoggingArgs(self, hide_args=True)
        self.add_argument('path_args', nargs='*', metavar='PATH', type=(pathlib.Path), help='An audio file or directory of audio files.')


def main():
    logging.basicConfig(stream=(sys.stderr), level=(logging.INFO))
    cli = ArgumentParser()
    args = cli.parse_args()
    app = MopApp()
    return app.run(args)


if __name__ == '__main__':
    sys.exit(main() or 0)