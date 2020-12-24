# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ComicThief/ct.py
# Compiled at: 2017-02-05 15:00:14
# Size of source mod 2**32: 1078 bytes
from argparse import ArgumentParser
from .main import ComicThief
OPTIONS = [
 (
  ('-s', '--search'), {'help': 'search'}),
 (
  ('-xs', '--xsearch'), {'help': 'exact search to narrow more than one result'}),
 (
  ('-e', '--episode'), {'help': 'choose episode', 'type': str})]

def add_arguments(parser):
    for option, kwargs in OPTIONS:
        parser.add_argument(*option, **kwargs)


def download_episode(episode):
    episode_url = result.get(episode)
    if episode_url:
        ct.download_episode(episode_url, episode)


if __name__ == '__main__':
    ct = ComicThief()
    parser = ArgumentParser()
    add_arguments(parser)
    args = parser.parse_args()
    if args.search:
        pass
    print('Searching..')
    results = ct.search(args.search)
    if results == 1 and args.episode:
        download_episode(args.episode)
else:
    if args.xsearch:
        result = ct.exact_search(args.xsearch)
        if args.episode:
            download_episode(args.episode)
    else:
        print('Use -s (normal search) or -xs (exact search).')