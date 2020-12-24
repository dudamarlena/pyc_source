# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/pyTextUtil/textUtil.py
# Compiled at: 2015-08-17 03:45:34
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import logging as log, datetime

def parseArgument():
    import argparse
    parser = argparse.ArgumentParser(description='Processing String.')
    subparser = parser.add_subparsers(dest='cmd')
    search = subparser.add_parser('search')
    search.add_argument('term', help='string to search.')
    search.add_argument('--regex', help='search with regex.', action='store_true')
    delete = subparser.add_parser('delete')
    delete.add_argument('term', help='string to delete.')
    delete.add_argument('--regex', help='search with regex.', action='store_true')
    delete.add_argument('--duplicatedLines', help='delete duplicated lines', action='store_true')
    delete.add_argument('--withoutBlankLines', help='duplicated test without blank lines', action='store_true')
    trim = subparser.add_parser('trim')
    trim.add_argument('--lines', help='trim blank lines.', action='store_true')
    parser.add_argument('-i', '--input', help='file to process.')
    parser.add_argument('-o', '--output', help='file to save result.(default=stdout)')
    parser.add_argument('-v', '--verbose', help='verbose mode. (0~1, 0:quiet, 1:verbose. default=0)', action='store_true')
    args = parser.parse_args()
    if not args.input:
        parser.error("No input file provided. use '-i' or '--input'")
    if args.verbose:
        log.basicConfig(format='%(levelname)s: %(message)s', level=log.DEBUG)
    return args


def main():
    start = datetime.datetime.now()
    args = parseArgument()
    if args.cmd == 'search':
        import search
        search.contains(args.input, args.output, args.term, args.regex)
    elif args.cmd == 'delete':
        import delete
        if args.duplicatedLines:
            delete.duplicatedLines(args.input, args.output, args.withoutBlankLines)
        else:
            delete.contains(args.input, args.output, args.term, args.regex)
    elif args.cmd == 'trim':
        from trim import trim
        trim(args.input, args.output, args.lines)
    took = datetime.datetime.now() - start
    log.info('Done! (%dsec.)' % took.seconds)


if __name__ == '__main__':
    main()