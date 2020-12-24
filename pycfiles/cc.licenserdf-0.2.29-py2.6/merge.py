# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/cc/licenserdf/tools/merge.py
# Compiled at: 2011-07-11 14:56:02
import pkg_resources, sys, os, optparse
from rdflib.Graph import Graph
from rdflib import Namespace, RDF, URIRef, Literal
import support

def create_option_parser():
    """Return an optparse.OptionParser configured for the merge script."""
    parser = optparse.OptionParser()
    parser.add_option('-o', '--output-file', dest='output_file', default=pkg_resources.resource_filename('cc.licenserdf', 'rdf/index.rdf'), help='Output file for merged RDF.')
    return parser


def merge(input_files):
    """Return a single rdflib Graph containing the contents of input_files.
    input_files should be a sequence of filenames to load."""
    store = support.graph()
    for filename in input_files:
        print 'reading %s...' % filename
        store.load(filename)

    return store


def cli():
    """Primary command line interface for the merge tool."""
    (options, input_files) = create_option_parser().parse_args()
    if len(input_files) < 2:
        print 'You must specify at least two files to merge.'
        sys.exit(1)
    output_fn = os.path.abspath(os.path.join(os.getcwd(), options.output_file))
    support.save_graph(merge(input_files), output_fn)
    print 'wrote %s' % output_fn


if __name__ == '__main__':
    cli()