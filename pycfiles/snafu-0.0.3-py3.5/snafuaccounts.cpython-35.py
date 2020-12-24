# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/snafulib/snafuaccounts.py
# Compiled at: 2018-07-01 01:56:00
# Size of source mod 2**32: 1499 bytes
import sys, os.path, argparse, configparser

class SnafuAccounts:

    def __init__(self):
        self.accounts = {}

    def addaccount(self, key, secret, endpoint):
        accdb = os.path.expanduser('~/.snafu-accounts')
        if os.getenv('HOME') == '/':
            accdb = '/root/.snafu-accounts'
        c = configparser.ConfigParser()
        try:
            c.read(accdb)
        except:
            pass

        acc = 'account{}'.format(len(c.sections()))
        c.add_section(acc)
        c.set(acc, 'access_key_id', key)
        c.set(acc, 'secret_access_key', secret)
        if endpoint:
            c.set(acc, 'endpoint', endpoint)
        f = open(accdb, 'w')
        c.write(f)

    def run(self):
        parser = argparse.ArgumentParser(description='Snake Functions as a Service - Account Management')
        parser.add_argument('-a', '--add', help='add an account', action='store_true')
        parser.add_argument('-k', '--key-id', help='access key id')
        parser.add_argument('-s', '--secret-access-key', help='secret access key')
        parser.add_argument('-e', '--endpoint', help='tenant-specific static endpoint')
        args = parser.parse_args()
        if args.add:
            if not args.key_id or not args.secret_access_key:
                print('Error: Must specify both --key-id and --secret-access-key for --add.', file=sys.stderr)
                return
            self.addaccount(args.key_id, args.secret_access_key, args.endpoint)
        else:
            print('Error: Must specify --add.', file=sys.stderr)
            return


class SnafuAccountsRunner:

    def __init__(self):
        sa = SnafuAccounts()
        sa.run()