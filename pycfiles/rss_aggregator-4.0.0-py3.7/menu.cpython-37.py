# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\RssReader\menu.py
# Compiled at: 2019-12-13 17:50:55
# Size of source mod 2**32: 2090 bytes
"""Main module"""
import argparse
from RssReader.rssaggregator import RssParser
from RssReader.getting_news import get_cached_news

def main():
    try:
        parser = argparse.ArgumentParser(description='Test')
        parser.add_argument('--limit', action='store', dest='limit', help='Simple value',
          default=1)
        parser.add_argument('--verbose', action='store_true', help='increase output verbosity')
        parser.add_argument('--version', action='store_true', help='version of this program')
        parser.add_argument('--json', action='store_true', help='convert to json')
        parser.add_argument('--epub', action='store_true', help='convert to epub')
        parser.add_argument('--date', action='store', dest='date', help='get caching news by date')
        parser.add_argument('--output', action='store', help='name of directory')
        parser.add_argument('string', metavar='S', type=str)
        args = parser.parse_args()
        if args.verbose:
            with open('sample.log', 'r+') as (f):
                date = f.read()
                print(date)
        else:
            if args.version:
                print('iteration 4')
            else:
                if args.json:
                    print(RssParser(args.string, int(args.limit)).convert_to_json())
                else:
                    if args.epub:
                        if args.output:
                            RssParser(args.string, int(args.limit)).to_epub(args.output)
                        else:
                            RssParser(args.string, int(args.limit)).to_epub()
                    else:
                        if args.date:
                            RssParser(args.string, int(args.limit)).cache_news()
                            print(get_cached_news(args.date))
                        else:
                            if args.limit:
                                RssParser(args.string, int(args.limit)).printer()
                            else:
                                RssParser(args.string, int(args.limit)).printer()
    except Exception as e:
        try:
            print(e)
        finally:
            e = None
            del e


if __name__ == '__main__':
    main()