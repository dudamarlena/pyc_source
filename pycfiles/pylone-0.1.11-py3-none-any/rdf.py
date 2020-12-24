# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pylon\io\rdf.py
# Compiled at: 2010-12-26 13:36:33
__doc__ = ' Defines classes for reading and writing cases.\n'
import os.path, logging
from rdflib.Graph import Graph
from rdflib import URIRef, Literal, BNode, Namespace
from rdflib import RDF
from pylon.io.common import _CaseWriter, _CaseReader, BUS_ATTRS, BRANCH_ATTRS, GENERATOR_ATTRS
logger = logging.getLogger(__name__)

class RDFReader(_CaseReader):
    """ Defines a reader for pickled cases.
    """

    def read(self, file_or_filename):
        """ Loads a case from RDF.
        """
        if isinstance(file_or_filename, basestring):
            fname = os.path.basename(file_or_filename)
            logger.info('Loading RDF case file [%s].' % fname)
            file = None
            try:
                try:
                    file = open(file_or_filename, 'rb')
                except:
                    logger.error('Error loading %s.' % fname)
                    return

            finally:
                if file is not None:
                    case = self._parse_rdf(file)
                    file.close()

        else:
            file = file_or_filename
            case = self._parse_rdf(file)
        return case

    def _parse_rdf(self, file):
        """ Returns a case from the given file.
        """
        store = Graph()
        store.parse(file)
        print len(store)


class RDFWriter(_CaseWriter):
    """ Writes cases as RDF/XML.
    """

    def __init__(self, case):
        super(RDFWriter, self).__init__(case)
        self.store = Graph()
        self.bus_map = {}

    def _write_data(self, file):
        super(RDFWriter, self)._write_data(file)
        NS_PYLON = Namespace('http://rwl.github.com/pylon/')
        self.store.bind('pylon', 'http://rwl.github.com/pylon/')
        for bus in self.case.buses:
            bus_node = BNode()
            self.bus_map[bus] = bus_node
            self.store.add((bus_node, RDF.type, NS_PYLON['Bus']))
            for attr in BUS_ATTRS:
                self.store.add((bus_node,
                 NS_PYLON[attr],
                 Literal(getattr(bus, attr))))

        for branch in self.case.branches:
            branch_node = BNode()
            self.store.add((branch_node, RDF.type, NS_PYLON['Branch']))
            for attr in BRANCH_ATTRS:
                self.store.add((branch_node,
                 NS_PYLON[attr],
                 Literal(getattr(branch, attr))))

        for generator in self.case.generators:
            g_node = BNode()
            self.store.add((g_node, RDF.type, NS_PYLON['Generator']))
            for attr in GENERATOR_ATTRS:
                self.store.add((g_node,
                 NS_PYLON[attr],
                 Literal(getattr(generator, attr))))

        file.write(self.store.serialize(format='pretty-xml', max_depth=3))


if __name__ == '__main__':
    import sys
    from pylon.case import Case, Bus, Branch
    from pylon.generator import Generator
    bus1 = Bus()
    bus2 = Bus()
    case = Case(buses=[bus1, bus2], branches=[
     Branch(bus1, bus2)], generators=[
     Generator(bus1)])
    RDFWriter(case).write(sys.stdout)