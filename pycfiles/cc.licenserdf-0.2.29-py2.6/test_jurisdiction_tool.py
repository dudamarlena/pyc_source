# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/cc/licenserdf/tests/test_jurisdiction_tool.py
# Compiled at: 2012-01-24 12:18:08
import pkg_resources, rdflib
from cc.licenserdf.tests.util import PrinterCollector, unordered_ensure_printer_printed
from cc.licenserdf.tools import jurisdiction

class MockOpts(object):
    pass


class MockSaveGraph(object):

    def __init__(self):
        self.graph = None
        self.save_path = None
        return

    def __call__(self, graph, save_path):
        self.graph = graph
        self.save_path = save_path


EXPECTED_INFO_OUTPUT_US = [
 'http://purl.org/dc/elements/1.1/title Etats-Unis',
 'http://purl.org/dc/elements/1.1/title United States',
 'http://purl.org/dc/elements/1.1/title United States',
 'http://creativecommons.org/ns#launched true',
 'http://purl.org/dc/elements/1.1/language en-us',
 'http://creativecommons.org/ns#jurisdictionSite http://creativecommons.org/worldwide/us/',
 'http://creativecommons.org/ns#defaultLanguage en-us',
 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type http://creativecommons.org/ns#Jurisdiction']

def test_info():
    opts = MockOpts()
    printer = PrinterCollector()
    opts.rdf_file = pkg_resources.resource_filename('cc.licenserdf.tests', 'rdf/jurisdictions.rdf')
    opts.jurisdiction = ['us']
    jurisdiction.info(opts, printer=printer)
    unordered_ensure_printer_printed(printer, EXPECTED_INFO_OUTPUT_US)


def test_launch():
    opts = MockOpts()
    opts.rdf_file = pkg_resources.resource_filename('cc.licenserdf.tests', 'rdf/jurisdictions.rdf')
    opts.jurisdiction = ['pl']
    graph_saver = MockSaveGraph()
    jurisdiction.launch(opts, save_graph=graph_saver)
    result = graph_saver.graph.value(subject=rdflib.URIRef('http://creativecommons.org/international/pl/'), predicate=rdflib.URIRef('http://creativecommons.org/ns#launched'))
    expected_result = rdflib.Literal('true', datatype=rdflib.URIRef('http://www.w3.org/2001/XMLSchema-datatypes#boolean'))
    assert result == expected_result
    assert graph_saver.save_path == opts.rdf_file


def test_add():
    opts = MockOpts()
    opts.rdf_file = pkg_resources.resource_filename('cc.licenserdf.tests', 'rdf/jurisdictions.rdf')
    opts.jurisdiction = ['it']
    opts.i18n_dir = pkg_resources.resource_filename('cc.i18n', 'i18n/')
    opts.juris_uri = 'http://www.creativecommons.it'
    opts.langs = 'en_US,sr_LATN'
    graph_saver = MockSaveGraph()
    jurisdiction.add(opts, __save_graph=graph_saver)
    assert graph_saver.save_path == opts.rdf_file
    assert rdflib.URIRef('http://creativecommons.org/international/it/') in [ i for i in graph_saver.graph.subjects() ]
    result = graph_saver.graph.value(subject=rdflib.URIRef('http://creativecommons.org/international/it/'), predicate=rdflib.URIRef('http://creativecommons.org/ns#launched'))
    expected_result = rdflib.Literal('false', datatype=rdflib.URIRef('http://www.w3.org/2001/XMLSchema-datatypes#boolean'))
    assert result == expected_result
    result = graph_saver.graph.value(subject=rdflib.URIRef('http://creativecommons.org/international/it/'), predicate=rdflib.URIRef('http://creativecommons.org/ns#jurisdictionSite'))
    expected_result = rdflib.URIRef('http://www.creativecommons.it')
    assert result == expected_result
    result = graph_saver.graph.triples((
     rdflib.URIRef('http://creativecommons.org/international/it/'),
     rdflib.URIRef('http://purl.org/dc/elements/1.1/title'),
     None))
    titles = {}
    for (subj, pred, obj) in result:
        titles[obj.language] = unicode(obj)

    assert titles['i18n'] == '${Italy}'
    assert titles['en'] == 'Italy'
    assert titles['it'] == 'Italia'
    return