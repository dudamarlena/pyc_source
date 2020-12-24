# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/hstools/funcs/init.py
# Compiled at: 2019-10-23 10:32:23
# Size of source mod 2**32: 2620 bytes
import os, sys, json, base64, argparse
from getpass import getpass
from hstools import hydroshare

def init(loc='.'):
    fp = os.path.abspath(os.path.join(loc, '.hs_auth'))
    if os.path.exists(fp):
        print(f"Auth already exists: {fp}")
        remove = input('Do you want to replace it [Y/n]')
        if remove.lower() == 'n':
            sys.exit(0)
        os.remove(fp)
    usr = input('Enter HydroShare Username: ')
    pwd = getpass('Enter HydroShare Password: ')
    dat = {'usr':usr, 
     'pwd':pwd}
    cred_json_string = str.encode(json.dumps(dat))
    cred_encoded = base64.b64encode(cred_json_string)
    with open(fp, 'w') as (f):
        f.write(cred_encoded.decode('utf-8'))
    try:
        hydroshare.hydroshare(authfile=fp)
    except Exception:
        print('Authentication Failed')
        os.remove(fp)
        sys.exit(1)

    print(f"Auth saved to: {fp}")


def add_arguments(parser):
    parser.description = long_help()
    parser.add_argument('-d', '--dir', default='~', help='location to save authentication directory ')
    set_usage(parser)


def set_usage(parser):
    optionals = []
    for option in parser._get_optional_actions():
        if len(option.option_strings) > 0:
            ostring = f"[{option.option_strings[0]}]"
            if '--' in ostring:
                optionals.append(ostring)
            else:
                optionals.insert(0, ostring)

    positionals = []
    for pos in parser._get_positional_actions():
        positionals.append(pos.dest)

    parser.usage = f"%(prog)s {' '.join(positionals)} {' '.join(optionals)}"


def main(args):
    dir = os.path.expanduser(args.dir)
    try:
        if not os.path.exists(dir):
            os.makedirs(dir)
    except Exception as e:
        try:
            raise Exception(f"Could not save creds to directory {args.dir}: {e}")
            sys.exit(1)
        finally:
            e = None
            del e

    init(loc=dir)


def short_help():
    return 'Initialize a connection with HydroShare'


def long_help():
    return 'Initialize a connection with HydroShare using basic\n              username:password authentication. By default, credentials are\n              stored in the $HOME directory in .hs_auth. All other hstools\n              use this authentication to connect with HydroShare.'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=long_help)
    add_arguments(parser)
    args = parser.parse_args()
    main(args)