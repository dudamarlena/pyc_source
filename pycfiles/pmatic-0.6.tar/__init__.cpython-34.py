# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib/python3.4/site-packages/pmath/__init__.py
# Compiled at: 2015-04-02 14:19:20
# Size of source mod 2**32: 2117 bytes
__doc__ = "\npmath [options] [statements...]\n\nA simple script for performing math in the terminal, using Python functions and\nsyntax. I created this when I discovered how hard it was to get a cube root\nusing Bash or bc.\n\nNote that 'from __future__ import division' is called, so '/' is float division,\nand '//' is integer division.\n\nNote that this is NOT sandboxed; a malicious user might be able to delete files\nor do who knows what with it. Its meant for known safe input, like Bash or Python\nis.\n\nSeparate arguments on the command line are treated as individual lines, and\nlines are further split by semicolons.\n\nIf no arguments are given, stdin is read.\n\nIf multiple lines are given, all but the first are evaluated with 'exec' and the\nsame 'locals', so variables can be created and stored. The last line is evaluated\nwith 'eval', and only its output is printed.\n\nShould work with Python 2.6+.\n\nExamples:\n$ pmath '3 + 4'\n7\n$ pmath -f'.4f' 'pow(2000, 1/3)'\n12.5992\n$ pmath -f'.4f' 'sin(pi/2)'\n1.0000\n$ pmath -c 'exp(1j*pi).real'\n-1.0\n$ pmath 'x=3;x+2'\n5\n$ echo '3+4' | pmath\n7\n"
from __future__ import division, print_function
import sys, math, cmath
from optparse import OptionParser
parser = OptionParser(usage=__doc__)
parser.add_option('-c', '--cmath', action='store_true', help='use complex math')
parser.add_option('-f', '--format', default='', help="How to format the result, e.g. '.3f'")

def evaluator(args, globald, format=''):
    locald = {}
    for arg in args[:-1]:
        exec(arg, globald, locald)

    arg = args[(-1)]
    value = eval(arg, globald, locald)
    return '{value:{format}}'.format(value=value, format=format)


def main():
    opts, args = parser.parse_args()
    globald = vars(math) if not opts.cmath else vars(cmath)
    globald = dict([(k, v) for k, v in globald.items() if k[:1] != '_'])
    if len(args) == 0:
        args = [line for line in sys.stdin]
    args = [splitarg.strip() for arg in args for splitarg in arg.split(';')]
    print(evaluator(args, globald, format=opts.format))


if __name__ == '__main__':
    main()