# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/p.vorobyov/PycharmProjects/exyaru/commands/shell.py
# Compiled at: 2019-01-24 02:57:24
from commands import Command

class Shell(Command):
    DESCRIPTION = 'Run shell (using IPython if available)'

    def run(self):
        from app.models import *
        try:
            from IPython import embed
            embed()
        except ImportError:
            try:
                import readline
            except ImportError:
                pass

            import code
            variables = globals().copy()
            variables.update(locals())
            shell = code.InteractiveConsole(variables)
            shell.interact()