# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/lvmanager/main.py
# Compiled at: 2020-02-15 18:26:02
# Size of source mod 2**32: 3188 bytes
import argparse, os
import lvmanager.manager as manager
ROOT = os.getenv('HOME')

def buildArgs():
    """
    Helper function to build our args

    :return: Args ready to be parsed!
    :rtype: argparser
    """
    usage = 'CLI for managing and maintaining tokens and key/certs.'
    argparser = argparse.ArgumentParser(usage=usage)
    argparser.add_argument('-add',
      help='Adds a file to lcm [--name required]',
      nargs=1)
    argparser.add_argument('-delete',
      help='Delete a saved file [--name required]',
      nargs=1)
    argparser.add_argument('-setenv',
      help='Expose a saved file as an environmental variable [--name required]',
      nargs=1)
    argparser.add_argument('-name',
      help='Name to be used',
      nargs=1)
    argparser.add_argument('-ls',
      help='Display what currently stored',
      action='store_true')
    argparser.add_argument('-cleanup',
      help='Clean up exposed keys',
      action='store_true')
    argparser.add_argument('-e',
      help='Use encryption for values when storing or setting the environment [LVMANAGER_PW is needed as an environmental variable]',
      action='store_true')
    argparser.add_argument('-getkey',
      help='Get a new encryption key',
      action='store_true')
    return argparser


def parseArgs(args):
    """
    Helper function to parse our args

    :param argparser args: Args that have been provided by the user
    """
    if args.add:
        if not args.name:
            print('[Error] No -name provided!')
        else:
            if not manager.add(args.add[0], args.name[0], args.e):
                print(f"[Error] Unable to add {args.name}")
            else:
                print(f"Successfully added: {args.name[0]}")
    else:
        if args.delete:
            if manager.delete(args.delete[0]):
                print(f"Successfully deleted {args.delete[0]}")
            else:
                print(f"[Error] Unable to delete: {args.delete}")
        else:
            if args.setenv:
                if args.name:
                    name = args.name[0]
                else:
                    name = ''
                if manager.setenv(args.setenv[0], name, args.e):
                    print(f"Successfully copied to clipboard for: {name}")
                else:
                    print(f"[Error] Unable to setenv: {name}")
            else:
                if args.ls:
                    manager.ls() or print('[Error] Something went wrong :(')
                else:
                    if args.cleanup:
                        manager.cleanup() or print('[Error] Something went wrong :(')
                    else:
                        if args.getkey:
                            if not manager.generateKey():
                                print('[Error] Something went wrong :(')


def main():
    """
    Main function to parse args and take action
    """
    args = buildArgs().parse_args()
    if not os.path.exists(f"{ROOT}/.lvm"):
        os.mkdir(f"{ROOT}/.lvm")
    if not os.path.exists(f"{ROOT}/.exposed"):
        os.mkdir(f"{ROOT}/.exposed")
    parseArgs(args)