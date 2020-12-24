# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/srtmerge/cli.py
# Compiled at: 2014-01-14 16:27:13
__author__ = 'wistful'
__version__ = '1.0'
__release_date__ = '15/01/2014'
import os, sys
from .srt import srtmerge

def print_version():
    print 'srtmerge: version %s (%s)' % (__version__, __release_date__)


def print_error(message):
    print ('srtmerge error: {0}').format(message)


def _check_argv(args):
    """
    check command line arguments
    """
    inPaths = args['inPath']
    if len(inPaths) < 2:
        print_error('too few arguments')
        return False
    for path in inPaths:
        if not os.path.exists(path):
            print_error(('file {srt_file} does not exist').format(srt_file=path))
            return False

    return True


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('inPath', type=str, nargs='+', help='srt-files that should be merged')
    parser.add_argument('outPath', type=str, help='output file path')
    parser.add_argument('--offset', action='store_const', const=0, default=0, help='offset in msc (default: 0)')
    parser.add_argument('-d', '--disable-chardet', action='store_true', dest='nochardet', default=False, help='disable auto character encoding')
    parser.add_argument('--encoding', type=str, default='utf-8', help='encoding for the output file (utf-8)')
    parser.add_argument('--version', action='store_true', dest='version', help='print version')
    if '--version' in sys.argv:
        print_version()
        sys.exit(0)
    args = vars(parser.parse_args())
    if _check_argv(args):
        srtmerge(args.get('inPath'), args.get('outPath'), args.get('offset'), not args.get('nochardet'), args.get('encoding'))


if __name__ == '__main__':
    main()