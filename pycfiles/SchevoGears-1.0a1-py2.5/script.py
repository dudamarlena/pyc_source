# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/schevogears/script.py
# Compiled at: 2008-01-19 12:10:14
"""TurboGears command.

For copyright, license, and warranty, see bottom of file.
"""
import sys
from schevo.script.command import Command
usage = 'evo tg [args]\n\nInstalls Schevo extensions for TurboGears, then passes args to\ntg-admin.\n'

class TurboGears(Command):
    name = 'TurboGears with Schevo extensions'
    description = 'Schevo-extended Turbogears tg-admin.'

    def main(self, arg0, args):
        print
        print
        sys.argv = [
         arg0] + list(args)
        from schevogears import extension
        extension.install()
        extension.tg_admin([arg0] + list(args))


start = TurboGears