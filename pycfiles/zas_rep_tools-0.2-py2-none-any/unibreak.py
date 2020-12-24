# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/_d/md744_dn7ggffch8955xb93h0000gs/T/pip-install-xY4LYQ/uniseg/uniseg/samples/unibreak.py
# Compiled at: 2018-07-23 18:20:27
from __future__ import absolute_import, division, print_function, unicode_literals
import io, sys
from uniseg.codepoint import code_points
from uniseg.graphemecluster import grapheme_clusters
from uniseg.wordbreak import words
from uniseg.sentencebreak import sentences
from uniseg.linebreak import line_break_units

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
    import argparse
    from locale import getpreferredencoding
    parser = argparse.ArgumentParser()
    parser.add_argument(b'-e', b'--encoding', default=getpreferredencoding(), help=b'text encoding of the input (%(default)s)')
    parser.add_argument(b'-l', b'--legacy', action=b'store_true', help=b"legacy mode (makes sense only with\n                        '--mode l')")
    parser.add_argument(b'-m', b'--mode', choices=[
     b'c', b'g', b'l', b's', b'w'], default=b'w', help=b'breaking algorithm (%(default)s)\n                        (c: code points, g: grapheme clusters,\n                        s: sentences l: line breaking units, w: words)')
    parser.add_argument(b'-o', b'--output', default=b'-', help=b'leave output to specified file')
    parser.add_argument(b'file', nargs=b'?', default=b'-', help=b'input text file')
    args = parser.parse_args()
    encoding = args.encoding
    fin = argopen(args.file, b'r', encoding)
    fout = argopen(args.output, b'w', encoding)
    _words = {b'c': code_points, b'g': grapheme_clusters, 
       b'l': lambda x: line_break_units(x, args.legacy), 
       b's': sentences, 
       b'w': words}[args.mode]
    for line in fin:
        for w in _words(line):
            print(w, file=fout)


if __name__ == b'__main__':
    main()