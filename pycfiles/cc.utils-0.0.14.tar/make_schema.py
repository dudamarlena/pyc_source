# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/cc/licenserdf/tools/make_schema.py
# Compiled at: 2011-07-11 14:56:02
import os, optparse, pkg_resources
from StringIO import StringIO
import rdfadict
from rdfadict.sink.graph import GraphSink
from rdflib import URIRef
from rdflib.Graph import ConjunctiveGraph as Graph
from rdflib.syntax.serializers.PrettyXMLSerializer import PrettyXMLSerializer

def create_option_parser():
    """Return an optparse.OptionParser configured for the merge script."""
    parser = optparse.OptionParser()
    parser.add_option('-i', '--input-file', dest='input_file', default='cc/licenserdf/rdf/ns.html', help='Input file containing HTML + RDFa.')
    parser.add_option('-o', '--output-file', dest='output_file', default='cc/licenserdf/rdf/schema.rdf', help='Output file for RDF schema.')
    return parser


def remove_assertions(store):
    """Remove assertions from the generated schema."""
    store.remove((URIRef('http://creativecommons.org/ns'), None, None))
    return


def schemafy(html_file):
    """Extract RDF from RDFa-annotated [html_file]; return a L{Graph} 
    containing the RDF."""
    store = Graph()
    store.bind('cc', 'http://creativecommons.org/ns#')
    store.bind('dc', 'http://purl.org/dc/elements/1.1/')
    store.bind('dcq', 'http://purl.org/dc/terms/')
    store.bind('rdf', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#')
    store.bind('xsd', 'http://www.w3.org/2001/XMLSchema-datatypes#')
    store.bind('owl', 'http://www.w3.org/2002/07/owl#')
    store.bind('xhtml', 'http://www.w3.org/1999/xhtml/vocab#')
    parser = rdfadict.RdfaParser()
    parser.parse_file(file(html_file), 'http://creativecommons.org/ns', sink=GraphSink(store))
    remove_assertions(store)
    return store


def cli():
    """Command line interface for make_schema:

    Take an RDFa annotated HTML document and generate schema.rdf from it."""
    (options, args) = create_option_parser().parse_args()
    output_fn = os.path.abspath(os.path.join(os.getcwd(), options.output_file))
    output_file = open(output_fn, 'w')
    output_file.write(schemafy(options.input_file).serialize(max_depth=1))
    output_file.close()