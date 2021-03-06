# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/PyMind/pymind.py
# Compiled at: 2013-06-11 17:50:10
__doc__ = '\nCopyright 2012 Alexey Kravets  <mr.kayrick@gmail.com>\n\nThis file is part of PyMind.\n\nPyMind is free software: you can redistribute it and/or modify\nit under the terms of the GNU General Public License as published by\nthe Free Software Foundation, either version 3 of the License, or\n(at your option) any later version.\n\nPyMind is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with PyMind.  If not, see <http://www.gnu.org/licenses/>.\n'
import argparse, ops, inspect, readline, signal
from settings import SettingsStorage
from mindmeister.auth import AuthToken
import os.path
from mindmeister.diagnostic import MindException
from argparse import RawTextHelpFormatter
import shlex, sys

def get_version_string():
    program_name = 'PyMind'
    program_version = '1.4.0'
    copyright_string = '\nCopyright 2012 Alexey Kravets  <mr.kayrick@gmail.com>\nFeel free to contact me via e-mail regarding any bugs and/or suggestions about PyMind.\nThis product uses the MindMeister API but is not endorsed or certified by MindMeister.\nLicense GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>\nThis is free software: you are free to change and redistribute it.\nThere is NO WARRANTY, to the extent permitted by law.\n    '
    return program_name + ' ' + program_version + copyright_string


def complain_invalid_command(method):
    print 'Invalid command ' + method + '. Use help to obtain the list of the avalible commands.'


def complain_invalid_args(method):
    print 'Invalid arguments for ' + method + '. Use help ' + method + ' to get command specific help.'


def shell_help(args):
    if len(args) == 0:
        print 'Avalible commands:'
        for command in shell_commands.keys():
            print command

        print "Use help `command' for additional information"
        return
    for arg in args:
        if shell_commands.has_key(arg):
            help('PyMind.ops.' + arg)
        else:
            complain_invalid_command(arg)


def shell():
    while 1:
        try:
            cmd = raw_input('pymind>>')
            command = shlex.split(cmd)
            if len(command) == 0:
                continue
            method = command[0]
            args = command[1:]
            if method == 'help':
                shell_help(args)
                continue
            if shell_commands.has_key(method):
                call = shell_commands[method]
                num_of_args = len(inspect.getargspec(call).args)
                if num_of_args != len(args):
                    complain_invalid_args(method)
                else:
                    shell_commands[method](*args)
                continue
            complain_invalid_command(method)
        except KeyboardInterrupt:
            print
            continue
        except EOFError:
            print
            return
        except MindException as err:
            print err


def login_and_start(method, args, proxy=None):
    settings = SettingsStorage(os.path.join(os.path.dirname(__file__), '../cfg/config.xml'))
    api_key = settings.data['api_key']
    secret = settings.data['secret']
    token = AuthToken(api_key, secret)
    token.setProxy(proxy)
    try:
        ops.login(token)
        method(*args)
        print 'Bye ' + ops.get_name() + '!'
    except MindException as err:
        print err


shell_commands = {}

class option_parser(argparse.Action):

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, 'dest', self.const)
        setattr(namespace, 'values', values)


def main():
    reload(sys)
    sys.setdefaultencoding('utf-8')
    parser = argparse.ArgumentParser(description='Minidmeister command line tool', formatter_class=RawTextHelpFormatter)
    parser.add_argument('--version', action='version', version=get_version_string())
    parser.add_argument('--proxy', nargs=1, help='Use proxy server PROXY')
    group = parser.add_mutually_exclusive_group(required=True)
    for curr in ops.ops:
        shell_commands[curr] = getattr(ops, curr)

    group.add_argument('--interactive', help='Interactive mode', nargs=0, action=option_parser, const=shell)
    for option, command in shell_commands.items():
        metavar = tuple(inspect.getargspec(command).args)
        group.add_argument('--' + option, help=command.__doc__, nargs=len(metavar), action=option_parser, const=command, metavar=metavar)

    args = parser.parse_args()
    if args.proxy != None:
        login_and_start(args.dest, args.values, args.proxy[0])
    else:
        login_and_start(args.dest, args.values)
    return


if __name__ == '__main__':
    main()