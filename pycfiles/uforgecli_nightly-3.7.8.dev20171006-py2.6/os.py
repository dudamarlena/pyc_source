# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uforgecli/commands/os/os.py
# Compiled at: 2017-08-17 09:51:42
__author__ = 'UShareSoft'
from ussclicore.argumentParser import ArgumentParser, ArgumentParserError
from ussclicore.cmd import Cmd, CoreGlobal
from texttable import Texttable
from uforgecli.utils.org_utils import org_get
from ussclicore.utils import generics_utils, printer
from ussclicore.utils.generics_utils import order_list_object_by
from uforgecli.utils.uforgecli_utils import *
from os_milestone import Os_Milestone_Cmd
from uforgecli.utils.compare_utils import compare
from uforgecli.utils import *
from uforgecli.utils.texttable_utils import *
from hurry.filesize import size
import shlex

class Os_Cmd(Cmd, CoreGlobal):
    """Administer operating systems/distributions (list/info etc)"""
    cmd_name = 'os'

    def __init__(self):
        self.generate_sub_commands()
        super(Os_Cmd, self).__init__()

    def generate_sub_commands(self):
        if not hasattr(self, 'subCmds'):
            self.subCmds = {}
        osMilestone = Os_Milestone_Cmd()
        self.subCmds[osMilestone.cmd_name] = osMilestone

    def arg_list(self):
        doParser = ArgumentParser(add_help=True, description='List all the operating systems (globally on the platform).  You must be a super-user to use this command')
        return doParser

    def do_list(self, args):
        try:
            osList = self.api.Distributions.Getall()
            osList = osList.distributions.distribution
            if len(osList) is None:
                printer.out('No operating systems.')
                return 0
            printer.out('List of distributions :')
            table = init_texttable(['Id', 'Distribution', 'Version', 'Architecture', 'Access', 'Visible', 'Release Date'], 200, [
             'c', 'c', 'c', 'c', 'c', 'c', 'c'], [
             't', 'a', 't', 'a', 'a', 'a', 'a'])
            for item in osList:
                if item.active:
                    active = 'X'
                else:
                    active = ''
                if item.visible:
                    visible = 'X'
                else:
                    visible = ''
                if item.releaseDate is None:
                    releaseDate = 'Unknown'
                else:
                    releaseDate = item.releaseDate
                table.add_row([item.dbId, item.name, item.version, item.arch, active, visible, releaseDate])

            print table.draw() + '\n'
            return 0
        except ArgumentParserError, e:
            printer.out('In Arguments: ' + str(e), printer.ERROR)
            self.help_list()
        except Exception, e:
            print_uforge_exception(e)

        return

    def help_list(self):
        doParser = self.arg_list()
        doParser.print_help()