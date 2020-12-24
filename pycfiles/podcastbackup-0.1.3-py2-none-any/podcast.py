# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/podcastake/podcast.py
# Compiled at: 2016-03-23 05:45:18
import argparse, sys
BANNDER = '\nmy awsome project v1.0\n'

def main():
    if len(sys.argv) == 1:
        print BANNDER
        sys.argv.append('--help')
    parser = argparse.ArgumentParser()
    parser.add_argument('-q', '--quality', type=int, default=0, help='download video quality : 1 for the standard-definition; 3 for the super-definition')
    parser.add_argument('-v', '--verbose', default=0, help='print more debuging information')
    parser.add_argument('-s', '--store', help='where to save the downloaded podcasts')
    parser.add_argument('-c', '--config', default=0, help='read config from ~/.{project_name} or your specified file')
    parser.add_argument('urls', metavar='URL', nargs='+', help='album url')
    parser.add_argument('-b', '--banner', type=bool, default=True, help='show banner?')
    args = parser.parse_args()
    for url in args.urls:
        print ('downloading from {}').format(url)


if __name__ == '__main__':
    main()