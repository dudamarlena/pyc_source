# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.4/site-packages/pmath/__init__.py
# Compiled at: 2015-04-02 14:19:20
# Size of source mod 2**32: 2117 bytes
"""
pmath [options] [statements...]

A simple script for performing math in the terminal, using Python functions and
syntax. I created this when I discovered how hard it was to get a cube root
using Bash or bc.

Note that 'from __future__ import division' is called, so '/' is float division,
and '//' is integer division.

Note that this is NOT sandboxed; a malicious user might be able to delete files
or do who knows what with it. Its meant for known safe input, like Bash or Python
is.

Separate arguments on the command line are treated as individual lines, and
lines are further split by semicolons.

If no arguments are given, stdin is read.

If multiple lines are given, all but the first are evaluated with 'exec' and the
same 'locals', so variables can be created and stored. The last line is evaluated
with 'eval', and only its output is printed.

Should work with Python 2.6+.

Examples:
$ pmath '3 + 4'
7
$ pmath -f'.4f' 'pow(2000, 1/3)'
12.5992
$ pmath -f'.4f' 'sin(pi/2)'
1.0000
$ pmath -c 'exp(1j*pi).real'
-1.0
$ pmath 'x=3;x+2'
5
$ echo '3+4' | pmath
7
"""
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