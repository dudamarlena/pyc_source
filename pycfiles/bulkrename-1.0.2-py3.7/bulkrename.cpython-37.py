# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\bulkrename\bulkrename.py
# Compiled at: 2018-08-20 08:06:42
# Size of source mod 2**32: 3988 bytes
import sys, shlex, os, bulkrename, secrets, json
from bulkrename import argpar, utils

def renamer(exclude=[], logs=None, char=8, revertfile=True):
    backup = {}
    for file in os.listdir():
        name = file.split('.')
        randomname = secrets.token_urlsafe(char)
        if exclude:
            if name[(-1)] in exclude or f".{name[(-1)]}" in exclude:
                if logs:
                    print(f"Skipped {file}")
                    continue
        if logs:
            print(f"Renamed {file} to {randomname}.{name[(-1)]}")
        try:
            newfilename = f"{randomname}.{name[(-1)]}"
            os.rename(file, newfilename)
            backup[file] = newfilename
        except PermissionError:
            print(f"Skipped {file}, permission denied")

    if revertfile:
        with open('bulkrn_backup.json', 'w') as (d):
            json.dump(backup, d)


def reverter(filename='bulkrn_backup.json', logs=False):
    try:
        with open(filename, 'r') as (d):
            data = json.load(d)
    except FileNotFoundError:
        utils.exitcode(f"Couldn't find any file called bulkrn_backup.json in {os.getcwd()}")

    for file in data:
        if logs:
            print(f"Reverted {file} back to {data[file]}")
        try:
            os.rename(data[file], file)
        except FileExistsError:
            print(f"Skipped {file}, name {data[file]} is already in the folder")
        except FileNotFoundError:
            print(f"Skipped {file}, couldn't find the file")

    os.remove(filename)
    print('Reverted names in current folder')


def shell():
    arguments = argpar.getarg()
    parser = argpar.Arguments(description='Rename multiple files in a folder to random characters')
    parser.add_argument('-v', '--version', action='store_true', help='Show the version number and exit')
    parser.add_argument('-l', '--logs', action='store_true', help='Shows which files it renames')
    parser.add_argument('-r', '--revert', action='store_true', help='Revert the renames with a backup file inside the target')
    parser.add_argument('-nb', '--nobackup', action='store_true', help='Prevent the script to dump a JSON backup')
    parser.add_argument('-e', '--exclude', nargs='+', help='Exclude file extensions')
    parser.add_argument('-c', '--characters', nargs='?', type=int, metavar='NUM', default=8, help='Amount inserteded to Python token_urlsafe (Rename length)')
    try:
        args = parser.parse_args(shlex.split(arguments))
    except Exception as e:
        try:
            utils.exitcode(e)
        finally:
            e = None
            del e

    if args.characters:
        if not 1 <= args.characters <= 25:
            utils.exitcode('You can only have a value between 1 to 25, stopped script...')
        if not args.characters == 8:
            print(f"Character length: {args.characters}")
    if args.version:
        utils.exitcode(bulkrename.__version__)
    else:
        if args.revert:
            reverter(logs=(args.logs))
            sys.exit(0)
        else:
            if args.exclude:
                toexclude = ', '.join(args.exclude)
                print(f"Excluding file types: {toexclude}")
            elif args.logs:
                print('Rename logs: Enabled')
            else:
                print('Rename logs: Disabled')
            nobackup = True
            if args.nobackup:
                nobackup = False
                print('Backup names: Disabled')
            else:
                print('Backup names: Enabled')
        print(f"Current target: {os.getcwd()}\n")
        if utils.query_yes_no('Are you sure you want to rename all files inside here?'):
            renamer(exclude=(args.exclude),
              logs=(args.logs),
              char=(args.characters),
              revertfile=nobackup)
        else:
            print('Stopped...')


def main():
    try:
        shell()
    except KeyboardInterrupt:
        print('\nCancelling...')


if __name__ == '__main__':
    main()