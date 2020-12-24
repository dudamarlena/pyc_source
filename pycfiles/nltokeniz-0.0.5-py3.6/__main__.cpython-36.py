# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nltokeniz/__main__.py
# Compiled at: 2017-01-17 01:27:55
# Size of source mod 2**32: 651 bytes
import argparse, json, sys
from .tokeniz import tokenize

def get_args():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('document_file', type=(argparse.FileType()),
      default=(sys.stdin))
    arg_parser.add_argument('-l', '--language', help='Follow ISO 639-1.')
    return arg_parser.parse_args()


def main():
    args = get_args()
    print(json.dumps(tokenize((args.document_file.read()), language=(args.language)),
      ensure_ascii=False,
      indent='\t'))


if __name__ == '__main__':
    main()