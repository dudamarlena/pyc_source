# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/zoocli/completer.py
# Compiled at: 2015-06-15 16:40:55
# Size of source mod 2**32: 604 bytes
from climb.completer import Completer
from climb.paths import SEPARATOR, ROOT_PATH

class ZooCompleter(Completer):

    def path(self, arg, text):
        if arg:
            if not arg.endswith(SEPARATOR):
                absolute = arg.startswith(ROOT_PATH)
                arg = SEPARATOR.join(arg.split(SEPARATOR)[:-1])
                if absolute:
                    arg = ROOT_PATH + arg
            paths = [p for p in self._cli.commands.ls(path=arg).split() if p.startswith(text)]
            if len(paths) == 1:
                return ['{}/'.format(paths[0])]
            return paths