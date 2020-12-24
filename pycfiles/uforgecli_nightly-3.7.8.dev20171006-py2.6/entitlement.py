# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uforgecli/commands/entitlement/entitlement.py
# Compiled at: 2017-03-01 08:38:06
__author__ = 'UShareSoft'
from ussclicore.argumentParser import ArgumentParser, ArgumentParserError
from ussclicore.cmd import Cmd, CoreGlobal
from texttable import Texttable
from uforgecli.utils.org_utils import org_get
from ussclicore.utils import generics_utils, printer
from uforgecli.utils.uforgecli_utils import *
from uforgecli.utils import *
import shlex

class Entitlement_Cmd(Cmd, CoreGlobal):
    """Administration of all the entitlements in UForge for RBAC"""
    cmd_name = 'entitlement'

    def __init__(self):
        super(Entitlement_Cmd, self).__init__()

    def arg_list(self):
        doParser = ArgumentParser(add_help=True, description='List all the entitlements in UForge')
        return doParser

    def do_list(self, args):
        try:
            doParser = self.arg_list()
            doArgs = doParser.parse_args(shlex.split(args))
            if not doArgs:
                return 2
            printer.out('Getting entitlements list of the UForge :')
            entList = self.api.Entitlements.Getall()
            if entList is None:
                printer.out('No entitlements found.', printer.OK)
            else:
                entList = generics_utils.order_list_object_by(entList.entitlements.entitlement, 'name')
                printer.out('Entitlement list for the UForge :')
                table = Texttable(200)
                table.set_cols_align(['l', 'l'])
                table.header(['Name', 'Description'])
                table.set_cols_width([30, 60])
                for item in entList:
                    table.add_row([item.name, item.description])

                print table.draw() + '\n'
            return 0
        except ArgumentParserError, e:
            printer.out('ERROR: In Arguments: ' + str(e), printer.ERROR)
            self.help_list()
        except Exception, e:
            return handle_uforge_exception(e)

        return

    def help_list(self):
        doParser = self.arg_list()
        doParser.print_help()