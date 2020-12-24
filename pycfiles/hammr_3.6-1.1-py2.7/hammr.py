# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hammr/hammr.py
# Compiled at: 2016-12-16 11:09:34
try:
    from termcolor import colored
except ImportError:

    def colored(string, a=None, b=None, attrs=None):
        return string


try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

import argparse, getpass, os, json, sys, shlex
from ussclicore.cmd import Cmd, CmdUtils
from ussclicore.argumentParser import CoreArgumentParser, ArgumentParser, ArgumentParserError
from ussclicore.utils import generics_utils
from ussclicore.utils import printer
import commands
from uforge.application import Api
from utils import *

class CmdBuilder(object):

    @staticmethod
    def generateCommands(class_):
        if not hasattr(class_, 'subCmds'):
            class_.subCmds = {}
        user = commands.user.User()
        class_.subCmds[user.cmd_name] = user
        template = commands.template.Template()
        class_.subCmds[template.cmd_name] = template
        _os = commands.os.Os()
        class_.subCmds[_os.cmd_name] = _os
        format = commands.format.Format()
        class_.subCmds[format.cmd_name] = format
        image = commands.image.Image()
        class_.subCmds[image.cmd_name] = image
        account = commands.account.Account()
        class_.subCmds[account.cmd_name] = account
        bundle = commands.bundle.Bundle()
        class_.subCmds[bundle.cmd_name] = bundle
        scan = commands.scan.Scan()
        class_.subCmds[scan.cmd_name] = scan
        quota = commands.quota.Quota()
        class_.subCmds[quota.cmd_name] = quota
        platform = commands.platform.Platform()
        class_.subCmds[platform.cmd_name] = platform


class Hammr(Cmd):

    def __init__(self):
        super(Hammr, self).__init__()
        self.prompt = 'hammr> '

    def do_exit(self, args):
        return True

    def do_quit(self, args):
        return True

    def arg_batch(self):
        doParser = ArgumentParser('batch', add_help=True, description='Execute hammr batch command from a file (for scripting)')
        mandatory = doParser.add_argument_group('mandatory arguments')
        mandatory.add_argument('--file', dest='file', required=True, help='hammr batch file commands')
        return doParser

    def do_batch(self, args):
        try:
            doParser = self.arg_batch()
            doArgs = doParser.parse_args(shlex.split(args))
            if not doArgs:
                return 2
            with open(doArgs.file) as (f):
                for line in f:
                    try:
                        self.run_commands_at_invocation([line])
                    except:
                        printer.out("bad command '" + line + "'", printer.ERROR)

                    print '\n'

        except IOError as e:
            printer.out('File error: ' + str(e), printer.ERROR)
            return
        except ArgumentParserError as e:
            printer.out('In Arguments: ' + str(e), printer.ERROR)
            self.help_batch()

    def help_batch(self):
        doParser = self.arg_batch()
        doParser.print_help()

    def cmdloop(self, args):
        if len(args):
            code = self.run_commands_at_invocation([str.join(' ', args)])
            sys.exit(code)
        else:
            self._cmdloop()


def generate_base_doc(app, hamm_help):
    myactions = []
    cmds = sorted(app.subCmds)
    for cmd in cmds:
        myactions.append(argparse._StoreAction(option_strings=[], dest=str(cmd), nargs=None, const=None, default=None, type=str, choices=None, required=False, help=str(app.subCmds[cmd].__doc__), metavar=None))

    return myactions


def set_globals_cmds(subCmds):
    for cmd in subCmds:
        if hasattr(subCmds[cmd], 'set_globals'):
            subCmds[cmd].set_globals(api, login, password)
            if hasattr(subCmds[cmd], 'subCmds'):
                set_globals_cmds(subCmds[cmd].subCmds)


def check_credfile(credfile):
    if os.path.isfile(credfile):
        return credfile
    else:
        if not credfile.endswith('.json') and os.path.isfile(credfile + '.json'):
            return credfile + '.json'
        if os.path.isfile(hammr_utils.get_hammr_dir() + os.sep + credfile):
            return hammr_utils.get_hammr_dir() + os.sep + credfile
        if not credfile.endswith('.json') and os.path.isfile(hammr_utils.get_hammr_dir() + os.sep + credfile + '.json'):
            return hammr_utils.get_hammr_dir() + os.sep + credfile + '.json'
        return


CmdBuilder.generateCommands(Hammr)
app = Hammr()
myactions = generate_base_doc(app, hamm_help='')
mainParser = CoreArgumentParser(add_help=False)
CoreArgumentParser.actions = myactions
mainParser.add_argument('-a', '--url', dest='url', type=str, help='the UForge server URL endpoint to use', required=False)
mainParser.add_argument('-u', '--user', dest='user', type=str, help='the user name used to authenticate to the UForge server', required=False)
mainParser.add_argument('-p', '--password', dest='password', type=str, help='the password used to authenticate to the UForge server', required=False)
mainParser.add_argument('-c', '--credentials', dest='credentials', type=str, help='the credential file used to authenticate to the UForge server (default to ~/.hammr/credentials.json)', required=False)
mainParser.add_argument('-v', action='version', help='displays the current version of the hammr tool', version="%(prog)s version '" + constants.VERSION + "'")
mainParser.add_argument('-h', '--help', dest='help', action='store_true', help='show this help message and exit', required=False)
mainParser.set_defaults(help=False)
mainParser.add_argument('cmds', nargs='*', help='Hammr cmds')
mainArgs, unknown = mainParser.parse_known_args()
if mainArgs.help and not mainArgs.cmds:
    mainParser.print_help()
    exit(0)
if mainArgs.url is not None:
    url = mainArgs.url
if mainArgs.user is not None:
    if not mainArgs.password:
        mainArgs.password = getpass.getpass()
    username = mainArgs.user
    password = mainArgs.password
    sslAutosigned = True
else:
    credfile = 'credentials.json'
    if mainArgs.credentials is not None:
        credfile = mainArgs.credentials
    printer.out('no username nor password provided on command line, trying credentials file', printer.INFO)
    credpath = check_credfile(credfile)
    if credpath is None:
        printer.out('credentials file ' + credfile + ' not found\n', printer.ERROR)
        exit(1)
    printer.out('Using credentials file: ' + credpath, printer.INFO)
    try:
        json_data = open(credpath)
        data = json.load(json_data)
        json_data.close()
        if mainArgs.user:
            username = mainArgs.user
        elif 'user' in data:
            username = data['user']
        else:
            printer.out('username not found in credentials file', printer.ERROR)
        if mainArgs.password:
            password = mainArgs.password
        elif 'password' in data:
            password = data['password']
        else:
            printer.out('password not found in credentials file', printer.ERROR)
        if mainArgs.url:
            url = mainArgs.url
        elif 'url' in data:
            url = data['url']
        else:
            printer.out('url not found in credentials file', printer.ERROR)
        printer.out('Using url ' + url, printer.INFO)
        if 'acceptAutoSigned' in data:
            sslAutosigned = data['acceptAutoSigned']
        else:
            sslAutosigned = True
    except ValueError as e:
        printer.out('JSON parsing error in credentials file: ' + str(e), printer.ERROR)
    except IOError as e:
        printer.out('File error in credentials file: ' + str(e), printer.ERROR)

api = Api(url, username=username, password=password, headers=None, disable_ssl_certificate_validation=sslAutosigned, timeout=constants.HTTP_TIMEOUT)
if generics_utils.is_superviser_mode(username):
    login = generics_utils.get_target_username(username)
else:
    login = username
set_globals_cmds(app.subCmds)
if mainArgs.help and len(mainArgs.cmds) >= 1:
    argList = mainArgs.cmds + unknown
    argList.insert(len(mainArgs.cmds) - 1, 'help')
    app.cmdloop(argList)
elif mainArgs.help:
    app.cmdloop(mainArgs.cmds + unknown + ['-h'])
else:
    app.cmdloop(mainArgs.cmds + unknown)