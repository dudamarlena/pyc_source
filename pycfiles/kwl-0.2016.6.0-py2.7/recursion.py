# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/kwl2text/recursion.py
# Compiled at: 2016-02-06 05:55:42
from __future__ import print_function, division, absolute_import, unicode_literals
from grako.parsing import graken, Parser
__version__ = (2016, 2, 6, 10, 55, 42, 5)
__all__ = [
 b'recursionParser',
 b'recursionSemantics',
 b'main']

class recursionParser(Parser):

    def __init__(self, whitespace=None, nameguard=True, **kwargs):
        super(recursionParser, self).__init__(whitespace=whitespace, nameguard=nameguard, comments_re=None, eol_comments_re=None, **kwargs)
        return

    @graken()
    def _sentence_(self):

        def block0():
            self._expression_()

        self._closure(block0)

    @graken()
    def _expression_(self):
        with self._choice():
            with self._option():
                self._token(b'{')
                self._expression_()
                self._token(b'}')
            with self._option():
                self._token(b'{')
                self._entry_()
                self._token(b'}')
            with self._option():
                self._entry_()
            self._error(b'no available options')

    @graken()
    def _entry_(self):
        self._token(b'1')


class recursionSemantics(object):

    def sentence(self, ast):
        return ast

    def expression(self, ast):
        return ast

    def entry(self, ast):
        return ast


def main(filename, startrule, trace=False, whitespace=None, nameguard=None):
    import json
    with open(filename) as (f):
        text = f.read()
    parser = recursionParser(parseinfo=False)
    ast = parser.parse(text, startrule, filename=filename, trace=trace, whitespace=whitespace, nameguard=nameguard)
    print(b'AST:')
    print(ast)
    print()
    print(b'JSON:')
    print(json.dumps(ast, indent=2))
    print()


if __name__ == b'__main__':
    import argparse, string, sys

    class ListRules(argparse.Action):

        def __call__(self, parser, namespace, values, option_string):
            print(b'Rules:')
            for r in recursionParser.rule_list():
                print(r)

            print()
            sys.exit(0)


    parser = argparse.ArgumentParser(description=b'Simple parser for recursion.')
    parser.add_argument(b'-l', b'--list', action=ListRules, nargs=0, help=b'list all rules and exit')
    parser.add_argument(b'-n', b'--no-nameguard', action=b'store_true', dest=b'no_nameguard', help=b"disable the 'nameguard' feature")
    parser.add_argument(b'-t', b'--trace', action=b'store_true', help=b'output trace information')
    parser.add_argument(b'-w', b'--whitespace', type=str, default=string.whitespace, help=b'whitespace specification')
    parser.add_argument(b'file', metavar=b'FILE', help=b'the input file to parse')
    parser.add_argument(b'startrule', metavar=b'STARTRULE', help=b'the start rule for parsing')
    args = parser.parse_args()
    main(args.file, args.startrule, trace=args.trace, whitespace=args.whitespace, nameguard=not args.no_nameguard)