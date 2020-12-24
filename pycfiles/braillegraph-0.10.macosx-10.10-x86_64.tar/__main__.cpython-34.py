# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.4/site-packages/braillegraph/__main__.py
# Compiled at: 2014-11-25 19:12:17
# Size of source mod 2**32: 3356 bytes
"""A library for creating graphs using Unicode braille characters.

https://pypi.python.org/pypi/braillegraph

Someone on reddit posted a screenshot of their xmobar setup, which used braille
characters to show the loads of their four processor cores, as well as several
other metrics. I was impressed that you could fit so much data into a single
line. I immediately set out to implement braille bar graphs for myself.

The characters this script outputs are in the Unicode Braille Patterns section,
code points 0x2800 through 0x28FF. Not all fonts support these characters, so
if you can't see the examples below check your font settings.

There are two ways to use this package: imported in Python code, or as a
command line script.

To use the package in Python, import it and use the vertical_graph and
horizontal_graph functions.

    >>> from braillegraph import vertical_graph, horizontal_graph
    >>> vertical_graph([3, 1, 4, 1])
    '⡯⠥'
    >>> horizontal_graph([3, 1, 4, 1])
    '⣆⣇'

To use the package as a script, run it as

    % python -m braillegraph vertical 3 1 4 1 5 9 2 6
    ⡯⠥
    ⣿⣛⣓⠒⠂
    % python -m braillegraph horizontal 3 1 4 1 5 9 2 6
    ⠀⠀⢀
    ⠀⠀⣸⢠
    ⣆⣇⣿⣼

For a description of the arguments and flags, run

    % python -m braillegraph --help
"""
import argparse
from .braillegraph import horizontal_graph, vertical_graph

def run():
    """Display the arguments as a braille graph on standard output."""
    parser = argparse.ArgumentParser(prog='python -m braillegraph', description='Print a braille bar graph of the given integers.')
    parser.add_argument('-n', '--no-newline', action='store_const', dest='end', const='', default=None, help='do not print the trailing newline character')
    subparsers = parser.add_subparsers(title='directions')
    horizontal_parser = subparsers.add_parser('horizontal', help='a horizontal graph')
    horizontal_parser.set_defaults(func=lambda args: horizontal_graph(args.integers))
    horizontal_parser.add_argument('integers', metavar='N', type=int, nargs='+', help='an integer')
    vertical_parser = subparsers.add_parser('vertical', help='a vertical graph')
    vertical_parser.set_defaults(func=lambda args: vertical_graph(args.integers, sep=args.sep))
    vertical_parser.add_argument('integers', metavar='N', type=int, nargs='+', help='an integer')
    vertical_parser.add_argument('-s', '--sep', action='store', default=None, help='separator for groups of bars')
    args = parser.parse_args()
    print(args.func(args), end=args.end)


if __name__ == '__main__':
    run()