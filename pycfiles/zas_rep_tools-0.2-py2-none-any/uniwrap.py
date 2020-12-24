# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/_d/md744_dn7ggffch8955xb93h0000gs/T/pip-install-xY4LYQ/uniseg/uniseg/samples/uniwrap.py
# Compiled at: 2018-07-23 18:20:27
from __future__ import absolute_import, division, print_function, unicode_literals
import argparse, io, sys
from locale import getpreferredencoding
from uniseg.wrap import tt_wrap

def argopen(file, mode, encoding=None, errors=None):
    closefd = True
    if file == b'-':
        closefd = False
        if b'r' in mode:
            file = sys.stdin.fileno()
        else:
            file = sys.stdout.fileno()
    return io.open(file, mode, encoding=encoding, errors=errors, closefd=closefd)


def main():
    encoding = getpreferredencoding()
    parser = argparse.ArgumentParser()
    parser.add_argument(b'-e', b'--encoding', default=encoding, help=b'file encoding (%(default)s)')
    parser.add_argument(b'-r', b'--ruler', action=b'store_true', help=b'show ruler')
    parser.add_argument(b'-t', b'--tab-width', type=int, default=8, help=b'tab width (%(default)d)')
    parser.add_argument(b'-l', b'--legacy', action=b'store_true', help=b'treat ambiguous-width letters as wide')
    parser.add_argument(b'-o', b'--output', default=b'-', help=b'leave output to specified file')
    parser.add_argument(b'-w', b'--wrap-width', type=int, default=60, help=b'wrap width (%(default)s)')
    parser.add_argument(b'-c', b'--char-wrap', action=b'store_true', help=b'wrap on grapheme boundaries instead of \n                        line break boundaries')
    parser.add_argument(b'file', nargs=b'?', default=b'-', help=b'input file')
    args = parser.parse_args()
    ruler = args.ruler
    tab_width = args.tab_width
    wrap_width = args.wrap_width
    char_wrap = args.char_wrap
    legacy = args.legacy
    encoding = args.encoding
    fin = argopen(args.file, b'r', encoding)
    fout = argopen(args.output, b'w', encoding)
    if ruler:
        if tab_width:
            ruler = (b'+' + b'-' * (tab_width - 1)) * (wrap_width // tab_width + 1)
            ruler = ruler[:wrap_width]
        else:
            ruler = b'-' * wrap_width
        print(ruler, file=fout)
    for para in fin:
        for line in tt_wrap(para, wrap_width, tab_width, ambiguous_as_wide=legacy, char_wrap=char_wrap):
            print(line.rstrip(b'\n'), file=fout)


if __name__ == b'__main__':
    main()