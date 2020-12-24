# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python2.7/site-packages/grakopp/tool.py
# Compiled at: 2014-08-01 18:27:50
"""
Parse and translate an EBNF grammar into a C++ parser for
the described language.
"""
from __future__ import absolute_import, division, print_function, unicode_literals
import grako
from .codegen.cpp import codegen as codegen_cpp
from .codegen.hpp import codegen as codegen_hpp
from .codegen.pxd import codegen as codegen_pxd
from .codegen.pyx import codegen as codegen_pyx
codegen = {b'cpp': codegen_cpp, 
   b'hpp': codegen_hpp, 
   b'pxd': codegen_pxd, 
   b'pyx': codegen_pyx}
import codecs, argparse, os, pickle, sys
from grako.util import eval_escapes
from grako.exceptions import GrakoException
from grako.parser import GrakoGrammarGenerator
DESCRIPTION = b'GRAKO (for "grammar compiler") takes grammars in a variation of EBNF as input, and outputs a memoizing PEG/Packrat parser in Python.'
argparser = argparse.ArgumentParser(prog=b'grako', description=DESCRIPTION)
argparser.add_argument(b'filename', metavar=b'GRAMMAR', help=b'The filename of the Grako grammar')
argparser.add_argument(b'-f', b'--format', metavar=b'FORMAT', default=b'cpp', help=b'The output format (one of: ' + (b', ').join(codegen.keys()) + b')')
argparser.add_argument(b'-n', b'--no-nameguard', help=b'allow tokens that are prefixes of others', dest=b'nameguard', action=b'store_false', default=True)
argparser.add_argument(b'-m', b'--name', nargs=1, metavar=b'NAME', help=b'Name for the grammar (defaults to GRAMMAR base name)')
argparser.add_argument(b'-o', b'--output', metavar=b'FILE', help=b'output file (default is stdout)')
argparser.add_argument(b'-t', b'--trace', help=b'produce verbose parsing output', action=b'store_true')
argparser.add_argument(b'-w', b'--whitespace', metavar=b'CHARACTERS', help=b'characters to skip during parsing (use "" to disable)', default=None)
argparser.add_argument(b'-s', b'--statetype', metavar=b'TYPENAME', help=b'class name of the parser state (for stateful parsing)', default=None)

def genmodel(name, grammar, trace=False, filename=None):
    parser = GrakoGrammarGenerator(name, trace=trace)
    return parser.parse(grammar, filename=filename)


def _error(*args, **kwargs):
    print(file=sys.stderr, *args, **kwargs)


def main():
    try:
        args = argparser.parse_args()
    except Exception as e:
        _error(str(e))
        sys.exit(2)

    filename = args.filename
    name = args.name
    nameguard = args.nameguard
    outfile = args.output
    trace = args.trace
    whitespace = args.whitespace
    statetype = args.statetype
    if whitespace:
        whitespace = eval_escapes(args.whitespace)
    if name is None:
        name = os.path.splitext(os.path.basename(filename))[0]
    if outfile and os.path.isfile(outfile):
        os.unlink(outfile)
    grammar = codecs.open(filename, b'r', encoding=b'utf-8').read()
    if outfile:
        dirname = os.path.dirname(outfile)
        if dirname and not os.path.isdir(dirname):
            os.makedirs(dirname)
    try:
        model = genmodel(name, grammar, trace=trace, filename=filename)
        model.whitespace = whitespace
        model.nameguard = nameguard
        model.statetype = statetype
        renderer = args.format
        result = codegen[renderer](model)
        if outfile:
            with codecs.open(outfile, b'w', encoding=b'utf-8') as (f):
                f.write(result)
        else:
            print(result)
    except GrakoException as e:
        _error(e)
        sys.exit(1)

    return


if __name__ == b'__main__':
    main()