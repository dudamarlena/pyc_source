# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rtownley/Projects/stonehenge/stonehenge/bin/stonehenge.py
# Compiled at: 2018-08-31 14:07:54
# Size of source mod 2**32: 746 bytes
import os, sys
from stonehenge.cli_utils import print_help
from stonehenge.new_project import generate_stonehenge_file
from stonehenge.build_project import build_project_from_stonehenge_file
COMMANDS = {'new':generate_stonehenge_file, 
 'build':build_project_from_stonehenge_file}

def main():
    try:
        command = sys.argv[1]
    except IndexError:
        print_help()
        return
    else:
        if command in COMMANDS:
            COMMANDS[command]()
        else:
            msg = 'ERROR: Invalid parameter supplied: {0}\n\n'.format(sys.argv[1])
            print_help(msg=msg)


if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stonehenge.settings')
    main()