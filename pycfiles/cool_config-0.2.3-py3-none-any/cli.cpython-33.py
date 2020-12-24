# uncompyle6 version 3.6.7
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\coolasciifaces\cli.py
# Compiled at: 2014-01-24 04:45:11
# Size of source mod 2**32: 444 bytes
from argparse import ArgumentParser
from coolasciifaces import all_faces, face

def main():
    parser = ArgumentParser(description='get some cool ascii faces')
    parser.add_argument('-a', '--all', help='print all faces', dest='show_all', action='store_true')
    args = parser.parse_args()
    if args.show_all:
        [print(f) for f in all_faces()]
    else:
        print(face())


if __name__ == '__main__':
    main()