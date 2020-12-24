# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\komidl\__main__.py
# Compiled at: 2019-10-12 01:12:13
# Size of source mod 2**32: 6665 bytes
"""
This module is the starting point for KomiDL where arguments are parsed and
passed to an instance of a KomiDL object
"""
import os, sys, argparse
import komidl.constants as constants
from komidl.komidl import KomiDL

def _init_args() -> argparse.Namespace:
    """Parse the arguments given"""
    parser = argparse.ArgumentParser(prog='komidl', usage='%(prog)s [OPTIONS] URL [URL...]',
      description='A downloader for image                                                   galleries',
      epilog='Author: DNSheng',
      add_help=False,
      formatter_class=(lambda prog: argparse.HelpFormatter(prog,
      max_help_position=90)))
    general_group = parser.add_argument_group('General Options')
    general_group.add_argument('-h', '--help', action='help',
      help='Print this help menu')
    general_group.add_argument('-v', '--version', action='version',
      version=(constants.VERSION),
      help='Print program version')
    general_group.add_argument('-y', '--yes', action='store_true',
      help='Yes to all prompts')
    general_group.add_argument('--list-extractors', action='store_true',
      help='List all supported extractors')
    general_group.add_argument('--logo', action='store_true',
      help='Print the KomiDL logo')
    download_group = parser.add_argument_group('Download Options')
    download_group.add_argument('--tags', action='store_true',
      help='Download gallery tags to a text file')
    download_group.add_argument('--directory', type=str,
      default='.',
      help='Download to a specific directory')
    download_group.add_argument('--lang', type=str,
      default='EN',
      help='Choose the preferred language with                                       ISO 639-1 codes if option for site                                       exists - case-insensitive (default: EN)')
    download_group.add_argument('--thread-size', type=int,
      default=3,
      help='Number of threads to download a gallery                                       with (default: 3)')
    export_group = parser.add_argument_group('Export Options')
    export_group.add_argument('--archive', type=str,
      choices=(constants.ARCHIVE_FORMATS),
      help='Archive the downloaded gallery')
    export_group.add_argument('--pdf', action='store_true',
      help='Export images downloaded to a PDF')
    export_group.add_argument('--keep', action='store_true',
      help='Keep gallery after exporting')
    parser.add_argument('URL', type=str,
      nargs='*',
      help='One or more gallery/page URLs')
    args = parser.parse_args()
    if not args.list_extractors:
        if not args.URL:
            if not args.logo:
                print('usage: komidl [OPTIONS] URL [URL...]')
                print('')
                print('komidl: error: You must provide at least one URL.')
                print('Type komidl --help to see a list of all options')
                sys.exit(0)
    return _preprocess_args(args)


def _preprocess_args(args: argparse.Namespace) -> argparse.Namespace:
    """Pre-process args before sending them to KomiDL."""
    if args.lang.lower() in constants.ISO_LANG_SET:
        args.lang = constants.ISO_LANG_SET[args.lang.lower()]
    else:
        args.lang = (
         args.lang.lower(),)
    args.directory = os.path.abspath(args.directory)
    return args


def main() -> None:
    """Init args and pass to KomiDL for downloading."""
    args = _init_args()
    komidl = KomiDL(args)
    if args.list_extractors:
        komidl.list()
    else:
        if args.logo:
            print(constants.KOMIDL_LOGO)
        else:
            try:
                komidl.download(args.URL)
            except KeyboardInterrupt:
                print('\nKeyboard interrupt detected -- exiting komidl')
                sys.exit(0)


if __name__ == '__main__':
    main()