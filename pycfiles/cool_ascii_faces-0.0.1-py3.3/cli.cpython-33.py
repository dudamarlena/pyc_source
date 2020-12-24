# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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