# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/tfnz/cli/tfdescribe.py
# Compiled at: 2018-05-18 20:34:30
# Size of source mod 2**32: 1180 bytes
import json
from tfnz.cli import generic_cli, base_argparse
from tfnz.docker import Docker

def main():
    parser = base_argparse('tfdescribe', location=False)
    parser.add_argument('image', help='image UUID or tag to describe')
    generic_cli(parser, {None: describe_image}, quiet=False, location=False)


def describe_image(location, args):
    desc = Docker.description(args.image)
    print(json.dumps(desc, indent=2))


if __name__ == '__main__':
    main()