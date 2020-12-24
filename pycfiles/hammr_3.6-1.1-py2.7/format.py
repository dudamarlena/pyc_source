# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hammr/commands/format/format.py
# Compiled at: 2016-12-15 07:34:25
__author__ = 'UShareSoft'
from texttable import Texttable
from ussclicore.argumentParser import ArgumentParser, ArgumentParserError
from ussclicore.cmd import Cmd, CoreGlobal
from ussclicore.utils import generics_utils, printer
from hammr.utils import *
from hammr.utils.hammr_utils import *

class Format(Cmd, CoreGlobal):
    """List all the formats the user has access to (cloud, virtual, physical)"""
    cmd_name = 'format'

    def __init__(self):
        super(Format, self).__init__()

    def arg_list(self):
        doParser = ArgumentParser(prog=self.cmd_name + ' list', add_help=True, description='Displays all the machine image formats for the user')
        return doParser

    def do_list(self, args):
        try:
            printer.out('Getting generation formats for [' + self.login + '] ...')
            targetFormatsUser = self.api.Users(self.login).Targetformats.Getall()
            if targetFormatsUser is None or len(targetFormatsUser.targetFormats.targetFormat) == 0:
                printer.out('No generation formats available')
                return 0
            targetFormatsUser = generics_utils.order_list_object_by(targetFormatsUser.targetFormats.targetFormat, 'name')
            table = Texttable(200)
            table.set_cols_align(['l', 'l', 'l', 'l', 'c'])
            table.header(['Builder Type', 'Format', 'Category', 'Cloud Account Type', 'Access'])
            for item in targetFormatsUser:
                if item.access:
                    access = 'X'
                else:
                    access = ''
                if item.credAccountType is None:
                    credAccountType = ''
                else:
                    credAccountType = item.credAccountType
                table.add_row([
                 item.name, item.format.name, item.category.name, credAccountType,
                 access])

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