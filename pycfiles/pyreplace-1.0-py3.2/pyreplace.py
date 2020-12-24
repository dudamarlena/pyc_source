# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pyreplace.py
# Compiled at: 2011-08-24 22:53:00
import argparse, os, sys, glob, re
from difflib import unified_diff
from os.path import join, isdir
DESCRIPTION = 'Recursively find and replace in file names and contents.'
EXAMPLE = 'Usage Examples:\nReplace foo with bar in filenames matching *.txt:\npyreplace -g *.txt -f foo bar\n\nFind and replace foo with bar in files matching *.txt (Contents):\npyreplace -g *.txt -c foo bar\n\nAs above with all files in current directory:\npyreplace -c foo bar\n\nAs above with all files in another directory:\npyreplace -d /home/foo -c foo bar\n'
parser = argparse.ArgumentParser(description=DESCRIPTION, epilog=EXAMPLE, formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('-d', '--directory', action='store', default='.', help='Set starting directory.')
parser.add_argument('-r', '--dry-run', action='store_true', help='Dont make any changes, just list what would happen.')
parser.add_argument('-v', '--verbose', action='store_true', help='Display changes made.')
parser.add_argument('-g', '--glob', metavar='EXPRESSION', action='store', default='*', help='Find files with matching extension. Example: *.txt')
parser.add_argument('-f', '--filename', metavar=('FIND', 'REPLACE'), action='store', nargs=2, help='Search filename for FIND and replace with REPLACE.')
parser.add_argument('-fi', '--filename-insensitive', action='store_true', help='Ignore capital/lowercase when searching filename.')
parser.add_argument('-c', '--contents', metavar=('FIND', 'REPLACE'), action='store', nargs=2, help='Search contents for FIND and replace with REPLACE.')
parser.add_argument('-ci', '--contents-insensitive', action='store_true', help='Ignore capital/lowercase when searching contents.')

def get_file_list():
    result = []
    for root, dirs, files in os.walk(args.directory):
        for item in glob.glob(join(root, args.glob)):
            if not isdir(item):
                result.append(item)
                continue

    return result


def process_filenames():
    opt_args = {}
    if args.filename_insensitive:
        opt_args['flags'] = re.IGNORECASE
    for f in get_file_list():
        result = re.sub(args.filename[0], args.filename[1], f, **opt_args)
        if not args.dry_run:
            os.rename(f, result)
        yield (
         f, result)


def process_contents():
    opt_args = {}
    if args.contents_insensitive:
        opt_args['flags'] = re.IGNORECASE
    for f in get_file_list():
        try:
            contents = open(f, 'r').read()
        except IOError as e:
            print(e)
            continue
        except UnicodeDecodeError:
            continue

        new_contents = re.sub(args.contents[0], args.contents[1], contents, **opt_args)
        if not args.dry_run:
            try:
                contents = open(f, 'w').write(new_contents)
            except IOError as e:
                print(e)
                continue

        diff = ''
        yield (f,
         unified_diff(contents.splitlines(1), new_contents.splitlines(1)))


def main():
    args = parser.parse_args()
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    if args.dry_run:
        print('*****' + ' Dummy run, no changes will be made. ' + '*****')
    if args.filename:
        if args.verbose or args.dry_run:
            print('Processing Filenames...')
        for result in process_filenames():
            if args.verbose or args.dry_run:
                print('Renaming %s to %s' % result)
                continue

    if args.contents:
        if args.verbose or args.dry_run:
            print('Processing Contents...')
        for result in process_contents():
            if args.verbose or args.dry_run:
                count = 0
                for line in result[1]:
                    if count == 0:
                        print('Made following changes to %s:' % result[0])
                    print(line, end='')
                    count += 1

                continue