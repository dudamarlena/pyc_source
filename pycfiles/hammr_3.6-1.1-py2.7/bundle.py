# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hammr/commands/bundle/bundle.py
# Compiled at: 2016-12-15 07:34:25
import shlex
from texttable import Texttable
from ussclicore.argumentParser import ArgumentParser, ArgumentParserError
from ussclicore.cmd import Cmd, CoreGlobal
from ussclicore.utils import generics_utils, printer
from hammr.utils.hammr_utils import *
from uforge.objects.uforge import *
from hurry.filesize import size

class Bundle(Cmd, CoreGlobal):
    """List or delete existing bundles (mysoftware) on UForge"""
    cmd_name = 'bundle'

    def __init__(self):
        super(Bundle, self).__init__()

    def arg_list(self):
        doParser = ArgumentParser(prog=self.cmd_name + ' list', add_help=True, description='Lists all the bundles that have been registered in the UForge server')
        return doParser

    def do_list(self, args):
        try:
            printer.out('Getting all your bundles ...')
            bundles = self.api.Users(self.login).Mysoftware.Getall()
            bundles = bundles.mySoftwareList.mySoftware
            if bundles is None or len(bundles) == 0:
                printer.out('No bundles available')
            else:
                table = Texttable(800)
                table.set_cols_dtype(['t', 't', 't', 't', 't', 't'])
                table.header(['Id', 'Name', 'Version', 'Description', 'Size', 'Imported'])
                bundles = generics_utils.order_list_object_by(bundles, 'name')
                for bundle in bundles:
                    table.add_row([bundle.dbId, bundle.name, bundle.version, bundle.description, size(bundle.size), 'X' if bundle.imported else ''])

                print table.draw() + '\n'
                printer.out('Found ' + str(len(bundles)) + ' bundles')
            return 0
        except Exception as e:
            return handle_uforge_exception(e)

        return

    def help_list(self):
        doParser = self.arg_list()
        doParser.print_help()

    def arg_delete(self):
        doParser = ArgumentParser(prog=self.cmd_name + ' delete', add_help=True, description='Deletes an existing bundle')
        mandatory = doParser.add_argument_group('mandatory arguments')
        mandatory.add_argument('--id', dest='id', required=True, help='the ID of the bundle to delete')
        return doParser

    def do_delete(self, args):
        try:
            doParser = self.arg_delete()
            doArgs = doParser.parse_args(shlex.split(args))
            if not doArgs:
                return 2
            printer.out('Searching bundle with id [' + doArgs.id + '] ...')
            myBundle = self.api.Users(self.login).Mysoftware(doArgs.id).Get()
            if myBundle is None or type(myBundle) is not MySoftware:
                printer.out('Bundle not found', printer.WARNING)
            else:
                table = Texttable(800)
                table.set_cols_dtype(['t', 't', 't', 't', 't', 't'])
                table.header(['Id', 'Name', 'Version', 'Description', 'Size', 'Imported'])
                table.add_row([myBundle.dbId, myBundle.name, myBundle.version, myBundle.description, size(myBundle.size), 'X' if myBundle.imported else ''])
                print table.draw() + '\n'
                if generics_utils.query_yes_no('Do you really want to delete bundle with id ' + str(myBundle.dbId)):
                    self.api.Users(self.login).Mysoftware(myBundle.dbId).Delete()
                    printer.out('Bundle deleted', printer.OK)
        except ArgumentParserError as e:
            printer.out('ERROR: In Arguments: ' + str(e), printer.ERROR)
            self.help_delete()
        except Exception as e:
            return handle_uforge_exception(e)

        return

    def help_delete(self):
        doParser = self.arg_delete()
        doParser.print_help()