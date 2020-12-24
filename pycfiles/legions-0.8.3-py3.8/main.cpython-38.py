# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/legions/main.py
# Compiled at: 2020-05-07 10:49:55
# Size of source mod 2**32: 375 bytes
import sys
from nubia import Nubia, Options
from legions.plugin import LegionPlugin
from legions import commands

def main():
    plugin = LegionPlugin()
    shell = Nubia(name='legions',
      command_pkgs=commands,
      plugin=plugin,
      options=Options(persistent_history=True))
    sys.exit(shell.run())


if __name__ == '__main__':
    main()