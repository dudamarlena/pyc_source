# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/slimit/slimit/minifier.py
# Compiled at: 2018-07-11 18:15:31
__author__ = 'Ruslan Spivak <ruslan.spivak@gmail.com>'
import sys, optparse, textwrap
from slimit import mangler
from slimit.parser import Parser
from slimit.visitors.minvisitor import ECMAMinifier

def minify(text, mangle=False, mangle_toplevel=False):
    parser = Parser()
    tree = parser.parse(text)
    if mangle:
        mangler.mangle(tree, toplevel=mangle_toplevel)
    minified = ECMAMinifier().visit(tree)
    return minified


def main(argv=None, inp=sys.stdin, out=sys.stdout):
    usage = textwrap.dedent('    %prog [options] [input file]\n\n    If no input file is provided STDIN is used by default.\n    Minified JavaScript code is printed to STDOUT.\n    ')
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-m', '--mangle', action='store_true', dest='mangle', default=False, help='mangle names')
    parser.add_option('-t', '--mangle-toplevel', action='store_true', dest='mangle_toplevel', default=False, help='mangle top level scope (defaults to False)')
    if argv is None:
        argv = sys.argv[1:]
    options, args = parser.parse_args(argv)
    if len(args) == 1:
        text = open(args[0]).read()
    else:
        text = inp.read()
    minified = minify(text, mangle=options.mangle, mangle_toplevel=options.mangle_toplevel)
    out.write(minified)
    return