# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/surf_rdflib/writer.py
# Compiled at: 2011-04-12 03:29:54
__author__ = 'Cosmin Basca'
import warnings
from surf.plugin.writer import RDFWriter
from surf.rdf import ConjunctiveGraph
from reader import ReaderPlugin

class WriterPlugin(RDFWriter):

    def __init__(self, reader, *args, **kwargs):
        RDFWriter.__init__(self, reader, *args, **kwargs)
        if isinstance(self.reader, ReaderPlugin):
            self.__rdflib_store = self.reader.rdflib_store
            self.__rdflib_identifier = self.reader.rdflib_identifier
            self.__commit_pending_transaction_on_close = self.reader.commit_pending_transaction_on_close
            self.__graph = self.reader.graph
        else:
            self.__rdflib_store = kwargs.get('rdflib_store', 'IOMemory')
            self.__rdflib_identifier = kwargs.get('rdflib_identifier')
            self.__commit_pending_transaction_on_close = kwargs.get('commit_pending_transaction_on_close', True)
            self.__graph = ConjunctiveGraph(store=self.__rdflib_store, identifier=self.__rdflib_identifier)
            warnings.warn('Graph is not readable through the reader plugin', UserWarning)

    rdflib_store = property(lambda self: self.__rdflib_store)
    rdflib_identifier = property(lambda self: self.__rdflib_identifier)
    graph = property(lambda self: self.__graph)
    commit_pending_transaction_on_close = property(lambda self: self.__commit_pending_transaction_on_close)

    def _save(self, *resources):
        for resource in resources:
            s = resource.subject
            self.__remove(s)
            for (p, objs) in resource.rdf_direct.items():
                for o in objs:
                    self.__add(s, p, o)

        self.__graph.commit()

    def _update(self, *resources):
        for resource in resources:
            s = resource.subject
            for p in resource.rdf_direct:
                self.__remove(s, p)

            for (p, objs) in resource.rdf_direct.items():
                for o in objs:
                    self.__add(s, p, o)

        self.__graph.commit()

    def _remove(self, *resources, **kwargs):
        inverse = kwargs.get('inverse')
        for resource in resources:
            self.__remove(s=resource.subject)
            if inverse:
                self.__remove(o=resource.subject)

        self.__graph.commit()

    def _size(self):
        return len(self.__graph)

    def _add_triple(self, s=None, p=None, o=None, context=None):
        self.__add(s, p, o, context)

    def _set_triple(self, s=None, p=None, o=None, context=None):
        self.__remove(s, p, context=context)
        self.__add(s, p, o, context)

    def _remove_triple(self, s=None, p=None, o=None, context=None):
        self.__remove(s, p, o, context)

    def __add(self, s=None, p=None, o=None, context=None):
        self.log.info('ADD: %s, %s, %s, %s' % (s, p, o, context))
        self.__graph.add((s, p, o))

    def __remove(self, s=None, p=None, o=None, context=None):
        self.log.info('REM: %s, %s, %s, %s' % (s, p, o, context))
        self.__graph.remove((s, p, o))

    def index_triples(self, **kwargs):
        """ Index triples if this functionality is present.  
        
        Return `True` if successful.
        
        """
        return True

    def load_triples(self, source=None, publicID=None, format='xml', **args):
        """ Load files (or resources on the web) into the triple-store. """
        if source:
            self.__graph.parse(source, publicID=publicID, format=format, **args)
            return True
        return False

    def _clear(self, context=None):
        """ Clear the triple-store. """
        self.__graph.remove((None, None, None))
        return

    def close(self):
        self.__graph.close(commit_pending_transaction=self.__commit_pending_transaction_on_close)