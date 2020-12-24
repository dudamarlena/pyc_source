# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\gitpullall\gitpullall.py
# Compiled at: 2018-11-13 02:57:43
# Size of source mod 2**32: 1874 bytes
import os, sys, gitpullall, subprocess
try:
    from argparse import ArgumentParser as ArgParser
except ImportError:
    from optparse import OptionParser as ArgParser

def printcmd(cmd):
    """Call the command, then end with a blank space."""
    subprocess.call(cmd, shell=True)
    print('')


def version():
    """Display the current version of the command."""
    print(gitpullall.__version__)
    sys.exit(0)


def parse_args():
    """Parge the arguments."""
    description = "Calls the command 'git pull' on all subfolders"
    parser = ArgParser(description=description)
    try:
        parser.add_argument = parser.add_option
    except AttributeError:
        pass

    parser.add_argument('--version', action='store_true', help='Show the version number and exit')
    options = parser.parse_args()
    if isinstance(options, tuple):
        args = options[0]
    else:
        args = options
    return args


def shell():
    """Shell commands for the different methods."""
    args = parse_args()
    if args.version:
        version()
    gitcounter = 0
    for g in os.listdir():
        try:
            if os.path.isdir(g):
                if '.git' in os.listdir(g):
                    print(g)
                    printcmd('cd {} && git pull'.format(g))
                    gitcounter += 1
        except PermissionError:
            print('{}\nSkipping this folder because no permission/wrong folder\n'.format(g))

    print('Successfully git pulled on {} subfolder{}'.format(gitcounter, '' if gitcounter == 1 else 's'))


def main():
    """Caller for everything in the background."""
    try:
        shell()
    except KeyboardInterrupt:
        print('\nCancelling...')


if __name__ == '__main__':
    main()