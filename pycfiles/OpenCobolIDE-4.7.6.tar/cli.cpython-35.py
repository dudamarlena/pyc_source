# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-4yaip7h6/keyring/keyring/cli.py
# Compiled at: 2016-12-29 05:40:26
# Size of source mod 2**32: 3369 bytes
"""Simple command line interface to get/set password from a keyring"""
from __future__ import print_function
import getpass
from optparse import OptionParser
import sys
from . import get_keyring, set_keyring, get_password, set_password, delete_password
from . import core

class CommandLineTool(object):

    def __init__(self):
        self.parser = OptionParser(usage='%prog [get|set|del] SERVICE USERNAME')
        self.parser.add_option('-p', '--keyring-path', dest='keyring_path', default=None, help='Path to the keyring backend')
        self.parser.add_option('-b', '--keyring-backend', dest='keyring_backend', default=None, help='Name of the keyring backend')

    def run(self, argv):
        opts, args = self.parser.parse_args(argv)
        try:
            kind, service, username = args
        except ValueError:
            if len(args) == 0:
                self.parser.print_help()
                return 1
            self.parser.error('Wrong number of arguments')

        if opts.keyring_backend is not None:
            try:
                if opts.keyring_path:
                    sys.path.insert(0, opts.keyring_path)
                backend = core.load_keyring(opts.keyring_backend)
                set_keyring(backend)
            except (Exception,):
                e = sys.exc_info()[1]
                self.parser.error('Unable to load specified keyring: %s' % e)

        if kind == 'get':
            password = get_password(service, username)
            if password is None:
                return 1
            self.output_password(password)
            return 0
        if kind == 'set':
            password = self.input_password("Password for '%s' in '%s': " % (
             username, service))
            set_password(service, username, password)
            return 0
        if kind == 'del':
            password = self.input_password("Deleting password for '%s' in '%s': " % (
             username, service))
            delete_password(service, username)
            return 0
        self.parser.error("You can only 'get', 'del' or 'set' a password.")

    def input_password(self, prompt):
        """Ask for a password to the user.

        This mostly exists to ease the testing process.
        """
        return getpass.getpass(prompt)

    def output_password(self, password):
        """Output the password to the user.

        This mostly exists to ease the testing process.
        """
        print(password, file=sys.stdout)


def main(argv=None):
    """Main command line interface."""
    if argv is None:
        argv = sys.argv[1:]
    cli = CommandLineTool()
    return cli.run(argv)


if __name__ == '__main__':
    sys.exit(main())