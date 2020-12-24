# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-fat/egg/rhizome/interfaces.py
# Compiled at: 2006-10-13 18:34:19
from zope.interface import Interface, Attribute
from zope.interface.common.sequence import IReadSequence as ITuple

class IRDFStore(Interface):
    """rhizome is a wrapper for a complementary set of rdflib graphs
    and stores"""
    __module__ = __name__
    _store = Attribute('primary persistent store for rdf')
    _index = Attribute('persistent store for text indexing')
    graph = Attribute('the store as a Conjunctive Graph')
    index = Attribute('index store wrapped in a TextIndex Graph')
    eventgraph = Attribute('primary store wrapped in a EventGraph')
    graph_index = Attribute('tuple of the eventgraph and the index graph (w/ the indexsubscribed to the eventgraph)')
    sparql = Attribute('primary graph wrapped as a SPARQL graph')

    def query(select, where):
        """convenience method for submitting GraphPattern queries"""
        pass


class IRDFData(ITuple):
    """
    An IRDFData object is a tuplish or
    tuplish object composed of triples representing data
    interesting about an object for IRhizome.
    """
    __module__ = __name__


class IRDFCatalogData(IRDFData):
    """ A dispatch interface: Should generally represent complete set
    of rdf data to be cataloged."""
    __module__ = __name__


class IRDFCatalogDataSubset(IRDFCatalogData):
    """
    to be subclassed by dispatch interfaces.

    A subset of the complete set of rdf data(ie for updates).
    """
    __module__ = __name__


class ISPARQLQuery(IRDFData):
    """
    A query object: a tuple of tuples representing the graph pattern
    """
    __module__ = __name__
    select = Attribute('the elements to return')
    factory = Attribute('bindery for return')