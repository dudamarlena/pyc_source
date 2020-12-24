# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dynip/init/console.py
# Compiled at: 2011-11-30 00:48:36
"""
Initializes a dynip environment.  Creates batch scripts and config files.
"""
import sys, os, shutil, argparse

def main():
    """
    Main entry point of init for console

    Expents sys.arg[1] to be the path to place the template files
    """
    parser = argparse.ArgumentParser(description='Set up configuration for a DynIP client/server pair')
    parser.add_argument('path', metavar='path', type=str, nargs=1, help='The path to store the DynIP configuration files')
    args = parser.parse_args()
    this_dir, this_filename = os.path.split(__file__)
    source_path = os.path.join(this_dir, 'example.conf')
    target_path = args.path[0]
    print ('Copying from {0} to {1}').format(source_path, target_path)
    shutil.copy2(source_path, target_path)


if __name__ == '__main__':
    sys.exit(main())