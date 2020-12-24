# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/slab/main.py
# Compiled at: 2016-01-07 05:48:00
# Size of source mod 2**32: 3046 bytes
import argparse, os
from .utils import argtype_dir_input, argtype_dir_output
from .config import AUTODOC_OPTIONS
from .core import build_tree, Module
from .formats import AVAILABLE_FORMATS, format_maker, add_arguments
__all__ = ('main', )

def get_parser(supported_formats):
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, description='Process apidoc templates instantiating them in actual ReST files.')
    parser.add_argument('root_dir', type=argtype_dir_input, help='Root directory of the package to be documented.')
    parser.add_argument('excludes', metavar='[exclude_path, ...]', nargs=argparse.REMAINDER, help='Path to be excluded from search.')
    parser.add_argument('-o', '--output-dir', dest='destdir', type=argtype_dir_output, required=True, help='Directory to place all output files.')
    parser.add_argument('-f', '--force', action='store_true', dest='force', default=False, help='Overwrite existing files.')
    add_arguments(parser)
    extra = parser.add_argument_group('Advanced options')
    extra.add_argument('--format', dest='format', choices=supported_formats, default='apidoc', help='Output format.')
    extra.add_argument('--toc-filename', dest='toc_filename', default='modules', help='Toc filename.')
    extra.add_argument('--autodoc-options', dest='autodoc_options', type=list, default=AUTODOC_OPTIONS, help='Sphinx Autodoc options. If omitted, the value of environment variable SPHINX_APIDOC_OPTIONS will be used.')
    return parser


def write(path, content, options):
    if content:
        if not options.force and os.path.exists(path):
            print('File {} exists, skipping.'.format(path))
        else:
            with open(path, 'w') as (outfile):
                outfile.write(content)


def main(argv, enabled_formats=AVAILABLE_FORMATS):
    parser = get_parser(enabled_formats)
    args = parser.parse_args(argv[1:])
    root = build_tree(args.root_dir)
    fmt = format_maker(args.format, args)
    if not args.notoc:
        toc = fmt.toc((root,))
        outfile = os.path.join(args.destdir, args.toc_filename + '.' + args.suffix)
        write(outfile, toc, args)
    excluded_types = set()
    if not args.separatemodules:
        excluded_types.add(Module)
    for docitem in root.docitems():
        if docitem.__class__ not in excluded_types:
            content = fmt.render(docitem)
            outfile = os.path.abspath(os.path.join(args.destdir, docitem.qualname + '.' + args.suffix))
            write(outfile, content, args)
            continue