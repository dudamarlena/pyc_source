# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uforgecli/commands/subscription/subscription_admin.py
# Compiled at: 2017-03-01 08:38:06
__author__ = 'UShareSoft'
from texttable import Texttable
from ussclicore.argumentParser import ArgumentParser, ArgumentParserError
from ussclicore.cmd import Cmd, CoreGlobal
from uforgecli.utils import org_utils
from ussclicore.utils import printer
from ussclicore.utils import generics_utils
from uforgecli.utils.uforgecli_utils import *
from uforge.objects import uforge
from uforgecli.utils import uforgecli_utils
import pyxb, shlex

class Subscription_Admins(Cmd, CoreGlobal):
    """Manage subscription profile admins"""
    cmd_name = 'admin'

    def __init__(self):
        super(Subscription_Admins, self).__init__()

    def arg_add(self):
        doParser = ArgumentParser(prog=self.cmd_name + ' add', add_help=True, description='Add a user as a subscription profile administrator.')
        mandatory = doParser.add_argument_group('mandatory arguments')
        optional = doParser.add_argument_group('optional arguments')
        mandatory.add_argument('--name', dest='name', required=True, help='The name of the subscription profile')
        mandatory.add_argument('--admins', dest='admins', nargs='+', required=True, help='The login names to add as new subscription profile administrators.')
        optional.add_argument('--org', dest='org', required=False, help='The organization name. If no organization is provided, then the default organization is used.')
        return doParser

    def do_add(self, args):
        try:
            doParser = self.arg_add()
            doArgs = doParser.parse_args(shlex.split(args))
            if not doArgs:
                return 2
            printer.out('Getting subscription profile with name [' + doArgs.name + ']...')
            org = org_utils.org_get(self.api, doArgs.org)
            subscriptions = self.api.Orgs(org.dbId).Subscriptions().Getall(Search=None)
            exist = False
            for item in subscriptions.subscriptionProfiles.subscriptionProfile:
                if item.name == doArgs.name:
                    exist = True
                    admins = userProfiles()
                    admins.userProfiles = pyxb.BIND()
                    for admin in item.admins.admin:
                        already_admin = userProfile()
                        already_admin.loginName = admin.loginName
                        admins.userProfiles.append(already_admin)

                    for e in doArgs.admins:
                        new_admin = userProfile()
                        new_admin.loginName = e
                        admins.userProfiles.append(new_admin)
                        printer.out('Added ' + new_admin.loginName + ' as admin.')

                    self.api.Orgs(org.dbId).Subscriptions(item.dbId).Admins.Update(body=admins)
                    printer.out('Some users added as administrators of subscription profile [' + doArgs.name + ']...', printer.OK)

            if not exist:
                printer.out("Subscription profile requested don't exist in [" + org.name + ']')
            return 0
        except ArgumentParserError, e:
            printer.out('ERROR: In Arguments: ' + str(e), printer.ERROR)
            self.help_add()
        except Exception, e:
            return handle_uforge_exception(e)

        return

    def help_add(self):
        doParser = self.arg_add()
        doParser.print_help()

    def arg_remove(self):
        doParser = ArgumentParser(prog=self.cmd_name + ' remove', add_help=True, description='Remove one or more entitlements to a role within the specified organization')
        mandatory = doParser.add_argument_group('mandatory arguments')
        optional = doParser.add_argument_group('optional arguments')
        mandatory.add_argument('--name', dest='name', required=True, help='The name of the subscription profile')
        mandatory.add_argument('--admins', dest='admins', nargs='+', required=True, help='The login names of the users to be removed from the the subscription profile administrators')
        optional.add_argument('--org', dest='org', required=False, help='The organization name. If no organization is provided, then the default organization is used.')
        return doParser

    def do_remove(self, args):
        try:
            doParser = self.arg_remove()
            doArgs = doParser.parse_args(shlex.split(args))
            if not doArgs:
                return 2
            printer.out('Getting subscription profile with name [' + doArgs.name + ']...')
            org = org_utils.org_get(self.api, doArgs.org)
            subscriptions = self.api.Orgs(org.dbId).Subscriptions().Getall(Search=None)
            exist = False
            for item in subscriptions.subscriptionProfiles.subscriptionProfile:
                if item.name == doArgs.name:
                    exist = True
                    admins = userProfiles()
                    admins.userProfiles = pyxb.BIND()
                    for admin in item.admins.admin:
                        if admin.loginName not in doArgs.admins:
                            already_admin = user()
                            already_admin.loginName = admin.loginName
                            admins.userProfiles.append(already_admin)
                        else:
                            printer.out('Removed ' + admin.loginName + ' as admin.')

                    self.api.Orgs(org.dbId).Subscriptions(item.dbId).Admins.Update(admins)
                    printer.out('Some users removed as administrators of subscription profile [' + doArgs.name + ']...', printer.OK)

            if not exist:
                printer.out("Subscription profile requested don't exist in [" + org.name + ']')
            return 0
        except ArgumentParserError, e:
            printer.out('ERROR: In Arguments: ' + str(e), printer.ERROR)
            self.help_remove()
        except Exception, e:
            return handle_uforge_exception(e)

        return

    def help_remove(self):
        doParser = self.arg_remove()
        doParser.print_help()