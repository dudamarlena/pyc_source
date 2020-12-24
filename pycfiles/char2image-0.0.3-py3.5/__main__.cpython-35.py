# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/char2image/__main__.py
# Compiled at: 2017-01-17 23:03:03
# Size of source mod 2**32: 690 bytes
import argparse, json, sys
from . import char2image

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('document_file', nargs='?', type=argparse.FileType(), default=sys.stdin)
    parser.add_argument('-s', '--size', type=int, default=32)
    parser.add_argument('-f', '--font-file', required=True)
    return parser.parse_args()


def main():
    args = get_args()
    print(json.dumps(char2image.char_to_image_dict({char for char in args.document_file.read()}, char2image.filename_to_font(args.font_file, args.size)), ensure_ascii=False))


if __name__ == '__main__':
    main()