# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hammr/commands/user/user.py
# Compiled at: 2016-12-15 07:34:25
from texttable import Texttable
from ussclicore.argumentParser import ArgumentParser, ArgumentParserError
from ussclicore.cmd import Cmd, CoreGlobal
from ussclicore.utils import generics_utils, printer
from hammr.utils.hammr_utils import *

class User(Cmd, CoreGlobal):
    """Lists information about a user, including login, email, name, date created, and status"""
    cmd_name = 'user'

    def __init__(self):
        super(User, self).__init__()

    def arg_info(self):
        doParser = ArgumentParser(prog=self.cmd_name + ' info', add_help=True, description='Displays informations of provided user')
        return doParser

    def do_info(self, args):
        try:
            printer.out('Getting user [' + self.login + '] ...')
            user = self.api.Users(self.login).Get()
            if user is None:
                printer.out('user ' + self.login + 'does not exist', printer.ERROR)
            else:
                table = Texttable(200)
                table.set_cols_align(['c', 'l', 'c', 'c', 'c', 'c', 'c', 'c'])
                table.header(['Login', 'Email', 'Lastname', 'Firstname', 'Created', 'Active', 'Promo Code', 'Creation Code'])
                table.add_row([user.loginName, user.email, user.surname, user.firstName, user.created.strftime('%Y-%m-%d %H:%M:%S'), 'X', user.promoCode, user.creationCode])
                print table.draw() + '\n'
            return 0
        except ArgumentParserError as e:
            printer.out('ERROR: In Arguments: ' + str(e), printer.ERROR)
            self.help_info()
        except Exception as e:
            return handle_uforge_exception(e)

        return

    def help_info(self):
        doParser = self.arg_info()
        doParser.print_help()