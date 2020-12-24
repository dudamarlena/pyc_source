# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/char2image/chars2images_main.py
# Compiled at: 2017-01-17 23:02:50
# Size of source mod 2**32: 800 bytes
import argparse, json, sys
from . import char2image

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('character_file', nargs='?', type=argparse.FileType(), default=sys.stdin)
    parser.add_argument('-s', '--size', type=int, default=32)
    parser.add_argument('-f', '--font-file', required=True)
    parser.add_argument('-u', '--unknown-char', default='�')
    return parser.parse_args()


def main():
    args = get_args()
    print(json.dumps(char2image.chars_to_images([line.strip() for line in args.character_file], char2image.filename_to_font(args.font_file, args.size), unknown_char=args.unknown_char), ensure_ascii=False))


if __name__ == '__main__':
    main()