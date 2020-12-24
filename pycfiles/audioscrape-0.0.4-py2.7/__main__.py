# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/audioscrape/__main__.py
# Compiled at: 2016-12-05 03:11:37
"""Download audio."""
import argparse, sys
from . import soundcloud, youtube

def download(query, include=None, exclude=None, quiet=False, overwrite=False):
    """Scrape various websites for audio."""
    youtube.scrape(query, include, exclude, quiet, overwrite)
    soundcloud.scrape(query, include, exclude, quiet, overwrite)


def main(args=None):
    """CLI for scraping audio."""
    if args is None:
        args = sys.argv[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument('query', default='Cerulean Crayons', nargs='?', help='search terms')
    parser.add_argument('-i', '--include', default=[], action='append', help='only download audio with this tag (this flag can be used multiple times)')
    parser.add_argument('-e', '--exclude', default=[], action='append', help='ignore results with this tag (this flag can be used multiple times)')
    parser.add_argument('-q', '--quiet', default=False, action='store_true', help='hide progress reporting')
    parser.add_argument('-o', '--overwrite', default=False, action='store_true', help='overwrite existing files')
    args = parser.parse_args()
    if not args.quiet:
        print ('Downloading audio from "{}" videos tagged {} and not {}.').format(args.query, args.include, args.exclude)
    download(args.query, args.include, args.exclude, args.quiet, args.overwrite)
    if not args.quiet:
        print 'Finished downloading audio.'
    return


if __name__ == '__main__':
    main()