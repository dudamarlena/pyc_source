# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hammr/commands/platform/platform.py
# Compiled at: 2016-12-15 07:34:25
from texttable import Texttable
from ussclicore.argumentParser import ArgumentParser, ArgumentParserError
from ussclicore.cmd import Cmd, CoreGlobal
from ussclicore.utils import generics_utils, printer
from hammr.utils import *
from hammr.utils.hammr_utils import *

class Platform(Cmd, CoreGlobal):
    """List platforms available"""
    cmd_name = 'platform'

    def __init__(self):
        super(Platform, self).__init__()

    def arg_list(self):
        doParser = ArgumentParser(add_help=True, description='List all the target platform I can access.')
        return doParser

    def do_list(self, args):
        try:
            printer.out('Getting target platform :')
            targetPlatformsUser = self.api.Users(self.login).Targetplatforms.Getall()
            if targetPlatformsUser is None or len(targetPlatformsUser.targetPlatforms.targetPlatform) == 0:
                printer.out('There is no target platform')
                return 0
            targetPlatformsUser = generics_utils.order_list_object_by(targetPlatformsUser.targetPlatforms.targetPlatform, 'name')
            printer.out('Target platform list:')
            table = Texttable(200)
            table.set_cols_align(['c', 'c', 'c', 'c'])
            table.header(['Id', 'Name', 'Type', 'Access'])
            for item in targetPlatformsUser:
                if item.access:
                    access = 'X'
                else:
                    access = ''
                table.add_row([item.dbId, item.name, item.type, access])

            print table.draw() + '\n'
            return 0
        except ArgumentParserError as e:
            printer.out('In Arguments: ' + str(e), printer.ERROR)
            self.help_list()
        except Exception as e:
            return handle_uforge_exception(e)

        return

    def help_list(self):
        doParser = self.arg_list()
        doParser.print_help()