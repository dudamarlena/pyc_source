# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/marketplacecli/commands/entitlementcmds/entitlementcmds.py
# Compiled at: 2016-06-03 07:47:35
__author__ = 'UShareSoft'
from texttable import Texttable
from ussclicore.argumentParser import ArgumentParser, ArgumentParserError
from ussclicore.cmd import Cmd, CoreGlobal
from ussclicore.utils import printer
from marketplacecli.utils import marketplace_utils

class EntitlementCmds(Cmd, CoreGlobal):
    """Manage entitlements: list them all. This is restricted to administrators."""
    cmd_name = 'entitlement'

    def __init__(self):
        super(EntitlementCmds, self).__init__()

    def arg_list(self):
        do_parser = ArgumentParser(prog=self.cmd_name + ' list', add_help=True, description='List all the entitlements in UForge.')
        return do_parser

    def do_list(self, args):
        try:
            printer.out('Getting all the entitlements for the platform ...')
            all_entitlements = self.api.Entitlements.Getall(None)
            table = Texttable(200)
            table.set_cols_align(['l', 'l'])
            table.header(['Name', 'Description'])
            for entitlement in all_entitlements.entitlements.entitlement:
                table.add_row([entitlement.name, entitlement.description])

            print table.draw() + '\n'
            return 0
        except ArgumentParserError as e:
            printer.out('ERROR: In Arguments: ' + str(e), printer.ERROR)
            self.help_list()
        except Exception as e:
            return marketplace_utils.handle_uforge_exception(e)

        return

    def help_list(self):
        do_parser = self.arg_list()
        do_parser.print_help()