# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/villi/github/Tokenizer/src/tokenizer/main.py
# Compiled at: 2019-10-24 11:20:08
"""

    Tokenizer for Icelandic text

    Copyright (C) 2019 Miðeind ehf.
    Original author: Vilhjálmur Þorsteinsson

    This software is licensed under the MIT License:

        Permission is hereby granted, free of charge, to any person
        obtaining a copy of this software and associated documentation
        files (the "Software"), to deal in the Software without restriction,
        including without limitation the rights to use, copy, modify, merge,
        publish, distribute, sublicense, and/or sell copies of the Software,
        and to permit persons to whom the Software is furnished to do so,
        subject to the following conditions:

        The above copyright notice and this permission notice shall be
        included in all copies or substantial portions of the Software.

        THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
        EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
        MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
        IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
        CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
        TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
        SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

    This is an executable program wrapper (main module) for the Tokenizer
    package. It can be used to invoke the Tokenizer from the command line,
    or via fork() or exec(), with the command 'tokenize'. The main() function
    of this module is registered as a console_script entry point in setup.py.

"""
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
import sys, argparse, json
from functools import partial
from .tokenizer import TOK, tokenize_without_annotation
from .definitions import make_str
if sys.version_info >= (3, 0):
    ReadFile = argparse.FileType(b'r', encoding=b'utf-8')
    WriteFile = argparse.FileType(b'w', encoding=b'utf-8')
else:
    ReadFile = argparse.FileType(b'r')
    WriteFile = argparse.FileType(b'w')
parser = argparse.ArgumentParser(description=b'Tokenizes Icelandic text')
parser.add_argument(b'infile', nargs=b'?', type=ReadFile, default=sys.stdin, help=b'UTF-8 text file to tokenize')
parser.add_argument(b'outfile', nargs=b'?', type=WriteFile, default=sys.stdout, help=b'UTF-8 output text file')
parser.add_argument(b'--moses', help=b'Use Moses-compatible token splitting', action=b'store_true')
group = parser.add_mutually_exclusive_group()
group.add_argument(b'--csv', help=b'Output one token per line in CSV format', action=b'store_true')
group.add_argument(b'--json', help=b'Output one token per line in JSON format', action=b'store_true')

def main():
    """ Main function, called when the tokenize command is invoked """
    args = parser.parse_args()
    options = dict()

    def quote(s):
        """ Return the string s within double quotes, and with any contained
            backslashes and double quotes escaped with a backslash """
        return b'"' + s.replace(b'\\', b'\\\\').replace(b'"', b'\\"') + b'"'

    def gen(f):
        """ Generate the lines of text in the input file """
        for line in f:
            yield make_str(line)

    def val(t, quote_word=False):
        """ Return the value part of the token t """
        if t.val is None:
            return
        else:
            if t.kind == TOK.WORD:
                if quote_word:
                    return quote(t.val[0][0])
                return t.val[0][0]
            if t.kind == TOK.PERCENT or t.kind == TOK.NUMBER:
                return t.val[0]
            if t.kind == TOK.S_BEGIN:
                return
            return t.val

    json_dumps = partial(json.dumps, ensure_ascii=False, separators=(',', ':'))
    curr_line = []
    for t in tokenize_without_annotation(gen(args.infile), **options):
        if args.csv:
            if t.txt:
                print((b'{0},{1},{2}').format(t.kind, quote(t.txt), val(t, quote_word=True) or b''), file=args.outfile)
        elif args.json:
            d = dict(k=TOK.descr[t.kind])
            if t.txt is not None:
                d[b't'] = t.txt
            v = val(t)
            if v is not None:
                d[b'v'] = v
            print(json_dumps(d), file=args.outfile)
        elif t.kind in TOK.END:
            print((b' ').join(curr_line), file=args.outfile)
            curr_line = []
        elif t.txt:
            curr_line.append(t.txt)

    if curr_line:
        print((b' ').join(curr_line), file=args.outfile)
    return


if __name__ == b'__main__':
    main()