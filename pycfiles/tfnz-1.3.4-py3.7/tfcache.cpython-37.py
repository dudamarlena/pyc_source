# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/tfnz/cli/tfcache.py
# Compiled at: 2018-05-18 20:34:30
# Size of source mod 2**32: 1157 bytes
from tfnz.cli import generic_cli, base_argparse
from tfnz.docker import Docker

def main():
    parser = base_argparse('tfcache')
    parser.add_argument('image', help='image UUID or tag to upload to cache')
    generic_cli(parser, {None: cache_image}, quiet=False)


def cache_image(location, args):
    descr = Docker.description(args.image)
    location.ensure_image_uploaded((args.image), descr=descr)


if __name__ == '__main__':
    main()