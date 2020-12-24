# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/skeletool/skeletool.py
# Compiled at: 2012-09-21 01:18:05
import sys
from options import *
from help import *
import help

class MainApp(object):

    def __init__(self, name='skeletool'):
        help.APPNAME = name

    def run(self):
        helpctrl = HelpController()
        optsctrl = OptionsController()
        opts, args = optsctrl.parse(sys.argv)
        try:
            action = optsctrl.action(args)
        except SyntaxError as ex:
            if ex.msg is not None:
                print ex
                print
            action = None

        if action is None:
            helpctrl.help()
            sys.exit(2)
        else:
            if 'h' in opts or 'help' in opts or len(args) < 2:
                helpctrl.help(args[0])
                sys.exit(2)
            dbinit(**opts)
            try:
                action(*args[2:], **opts)
            except SyntaxError as ex:
                helpctrl.help(args[0])
                sys.exit(2)

        return


def run():
    MainApp().run()


if __name__ == '__main__':
    run()