# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mendeley2biblatex/__init__.py
# Compiled at: 2016-07-20 10:13:03
# Size of source mod 2**32: 1329 bytes
import sys
from argparse import ArgumentParser
from mendeley2biblatex.library_converter import LibraryConverter
__all__ = [
 'bib_entry', 'library_converter']

def main():
    """Set this script some command line options. See usage."""
    parser = ArgumentParser(description='Convert a sqlite database from mendeley to bibetex')
    parser.add_argument('-q', '--quiet', action='store_true', default=False, dest='quiet', help='Do not display any information.')
    parser.add_argument('-f', '--folder', default=None, dest='folder', help='Limit output to mendeley folder')
    parser.add_argument('-o', '--output', dest='bibtex_file', default=sys.stdout, help='BibTeX file name, else output will be printed to stdout')
    parser.add_argument('input', metavar='INPUT_FILE', nargs='?', help='the mendeley database')
    parser.add_argument('--version', action='version', version='mendeley2biblatex')
    args = parser.parse_args()
    if not args.input:
        parser.error('No file specified')
    LibraryConverter.convert_library(args.input, args.bibtex_file, args.quiet, args.folder)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted by user')