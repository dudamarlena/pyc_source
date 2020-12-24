# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pwkeeper/pwkeeper.py
# Compiled at: 2016-05-22 12:07:36
# Size of source mod 2**32: 1372 bytes
import argparse, os
from .models import PWKeeper
from . import settings

def main():
    parser = argparse.ArgumentParser(description='Manage your passwords with pwkeeper.')
    parser.add_argument('-n', type=int, help="With 'generate', the length of the generated password")
    parser.add_argument('-p', action='store_true', help='Show passwords in cleartext when searching')
    parser.add_argument('command', nargs='*', help='[add|edit|save|generate|<search>]')
    args = parser.parse_args()
    if not os.path.exists(settings.DATA_DIR):
        print('Initializing new data directory in %s ...' % settings.DATA_DIR)
        key = PWKeeper.initialize()
        print()
        print('Generated AES key: %s' % key)
        print('AES key file:      %s' % settings.KEY_FILE)
        print('Password file:     %s' % settings.PASSWORD_FILE)
        exit()
    if not args.command:
        parser.print_help()
        exit()
    pw = PWKeeper()
    if args.command[0] == 'add':
        pw.add_password()
    else:
        if args.command[0] == 'edit':
            pw.edit_plaintext()
        else:
            if args.command[0] == 'save':
                pw.save_plaintext()
            else:
                if args.command[0] == 'generate':
                    print(PWKeeper.generate(args.n or settings.DEFAULT_PASSWORD_LENGTH))
                else:
                    pw.search(args.command, args.p)


if __name__ == '__main__':
    main()