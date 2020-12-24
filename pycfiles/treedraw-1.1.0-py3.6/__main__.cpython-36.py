# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/treedraw/__main__.py
# Compiled at: 2017-10-18 08:30:25
# Size of source mod 2**32: 1018 bytes
import sys, argparse
from .render import Renderer
from .parser import Parser

def main():
    p = argparse.ArgumentParser(description='Render a tree image from a .tree file', add_help=False)
    p.add_argument('input', type=str, help='input .tree file')
    p.add_argument('output', type=str, help='output filename (.png only for now)')
    p.add_argument('-w', '--width', default=800, type=int, help='output file width in pixels')
    p.add_argument('-h', '--height', default=600, type=int, help='output file height in pixels')
    p.add_argument('-b', '--border', default=2, type=int, help='border width of nodes in tree')
    p.add_argument('--help', action='help', help='show this help message and exit')
    args = p.parse_args()
    parser = Parser(args.input)
    renderer = Renderer(args.output, args.width, args.height, args.border)
    print('Parsing...')
    tree = parser.make_tree()
    print('Rendering...')
    renderer.render_tree(tree)
    print('Done.')


if __name__ == '__main__':
    main()