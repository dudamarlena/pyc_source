# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/cc/licenserdf/tools/translate_rdf.py
# Compiled at: 2011-11-08 16:31:38
__doc__ = '\nTake an rdf file and update any translations that might be available\nfor translating.\n'
import os, glob
from argparse import ArgumentParser
from support import *

def get_args():
    """Get all args taken by this app"""
    parser = ArgumentParser(description='Take an rdf file and run it through the translation machinery.')
    parser.add_argument('-a', '--all', action='store_const', const=True, help='implies: translate_rdf cc/licenserdf/licenses/*.rdf')
    parser.add_argument('rdf_file', nargs='*')
    return parser.parse_args()


def cli():
    opts = get_args()
    if opts.all:
        opts.rdf_file = glob.glob('cc/licenserdf/licenses/*.rdf')
    if opts.rdf_file:
        count = 0
        for path in opts.rdf_file:
            if not os.path.exists(path):
                print 'That filename does not exist.'
                return 1
            graph = load_graph(path)
            translate_graph(graph)
            save_graph(graph, path)
            count += 1

        print 'Translated', count, 'file(s).'
    else:
        print 'You need to pass at least one argument.'