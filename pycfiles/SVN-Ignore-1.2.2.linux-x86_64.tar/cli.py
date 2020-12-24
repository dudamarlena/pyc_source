# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/src/cli.py
# Compiled at: 2016-08-22 16:12:06
import sys, argparse, logging
from src.svn_ignore import SVNIgnore

def create_parser():
    parser = argparse.ArgumentParser(description='An utility that provides .svnignore functionality similar to GIT')
    parser.add_argument('directory', nargs='?', type=str, default='.', help='The root directory. Default is the working directory.')
    parser.add_argument('--no-recursive', dest='recursive', action='store_false', help='Do not apply the ignore file to child directories.', required=False, default=True)
    parser.add_argument('--overwrite', action='store_true', default=False, help='Overwrite the existing ignore property.', required=False)
    parser.add_argument('--verbose', action='store_true', default=False, help='Turn verbose mode on.', required=False)
    parser.add_argument('--ignore-file', type=str, default='.svnignore', help='The ignore file to look for. Default is .svnignore.')
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()
    if args.verbose:
        level = logging.DEBUG
    else:
        level = logging.WARNING
    logging.basicConfig(stream=sys.stdout, format='%(levelname)s: %(message)s', level=level)
    svn_ignore = SVNIgnore(directory=args.directory, recursive=args.recursive, overwrite=args.overwrite, ignore_file=args.ignore_file)
    svn_ignore.apply()


if __name__ == '__main__':
    main()