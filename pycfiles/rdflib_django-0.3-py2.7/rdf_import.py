# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/rdflib_django/management/commands/rdf_import.py
# Compiled at: 2012-09-29 04:46:32
"""
Management command for parsing RDF into the store.
"""
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
import sys
from django.db import transaction
from rdflib.graph import Graph
from rdflib.term import URIRef, BNode
from rdflib_django import utils

class Command(BaseCommand):
    """
    Command object for importing RDF.
    """
    option_list = BaseCommand.option_list + (
     make_option('--store', '-s', type='string', dest='store', help='RDF data will be imported into the store with this identifier. If not specified, the default store ' + 'is used.'),
     make_option('--context', '-c', type='string', dest='context', help='RDF data will be imported into a context with this identifier. If not specified, a new blank ' + 'context is created.'),
     make_option('--format', '-f', type='string', dest='format', default='xml', help='Format of the RDF data. This option accepts all formats allowed by rdflib. Defaults to xml.'))
    help = ('Imports an RDF resource.\n\nExamples:\n    {0} rdf_import my_file.rdf\n    {0} rdf_import --format n3 my_file.n3\n    {0} rdf_import --context http://zoowizard.eu http://zoowizard.eu/datasource/zoochat/294\n    ').format(sys.argv[0])
    args = 'file-or-resource'

    @transaction.commit_on_success
    def handle(self, *args, **options):
        if not args:
            raise CommandError('No file or resource specified.')
        info = options.get('verbosity') >= 2
        store_id = options.get('store')
        context_id = options.get('context')
        source = args[0]
        if info:
            print ('Parsing {0}').format(source)
        intermediate = Graph()
        try:
            intermediate.parse(source, format=options.get('format'))
        except Exception as e:
            raise CommandError(e)

        if info:
            print ('Parsed {0} triples').format(len(intermediate))
        identifier = URIRef(context_id) if context_id else BNode()
        graph = utils.get_named_graph(identifier, store_id=store_id)
        if info:
            print ('Storing {0} triples').format(len(intermediate))
        for triple in intermediate:
            graph.add(triple)

        if info:
            print 'Done'