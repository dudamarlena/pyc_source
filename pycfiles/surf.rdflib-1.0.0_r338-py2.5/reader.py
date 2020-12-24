# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/surf_rdflib/reader.py
# Compiled at: 2011-04-12 03:29:54
__author__ = 'Cosmin Basca'
try:
    from json import loads
except Exception, e:
    from simplejson import loads

from surf.plugin.query_reader import RDFQueryReader
from surf.rdf import ConjunctiveGraph

class ReaderPlugin(RDFQueryReader):

    def __init__(self, *args, **kwargs):
        RDFQueryReader.__init__(self, *args, **kwargs)
        self.__rdflib_store = kwargs.get('rdflib_store', 'IOMemory')
        self.__rdflib_identifier = kwargs.get('rdflib_identifier')
        self.__commit_pending_transaction_on_close = kwargs.get('commit_pending_transaction_on_close', True)
        self.__graph = ConjunctiveGraph(store=self.__rdflib_store, identifier=self.__rdflib_identifier)

    rdflib_store = property(lambda self: self.__rdflib_store)
    rdflib_identifier = property(lambda self: self.__rdflib_identifier)
    graph = property(lambda self: self.__graph)
    commit_pending_transaction_on_close = property(lambda self: self.__commit_pending_transaction_on_close)

    def _to_table(self, result):
        vars = [ unicode(var) for var in result.selectionF ]
        return [ dict(zip(vars, row)) for row in result ]

    def _ask(self, result):
        return result.askAnswer[0]

    def _execute(self, query):
        q_string = unicode(query)
        self.log.debug(q_string)
        return self.__graph.query(q_string)

    def execute_sparql(self, q_string, format=None):
        self.log.debug(q_string)
        result = self.__graph.query(q_string)
        return loads(result.serialize('json'))

    def close(self):
        self.__graph.close(commit_pending_transaction=self.__commit_pending_transaction_on_close)