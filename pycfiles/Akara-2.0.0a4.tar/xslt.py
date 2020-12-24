# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Library/Python/2.6/site-packages/akamu/demo/xslt.py
# Compiled at: 2013-03-08 14:26:58
__author__ = 'chimezieogbuji'
import cgi, amara
from akamu.xslt import xslt_rest
from akara.services import simple_service
from cStringIO import StringIO
from amara.writers.struct import structwriter, E, NS, ROOT
from amara.lib import U
from akara import request
from akamu.diglot import Manager, Resource
from akamu.xslt import TransformWithAkamuExtensions
from akamu.config.dataset import DestroyOrCreateDataset
from akamu.config.diglot import GetDiglotManager
SERVICE_ID = 'http://example.com/xslt_rest'

def MakeFoafGraph(name='Chimezie Ogbuji'):
    src = StringIO()
    w = structwriter(indent='yes', stream=src)
    w.feed(ROOT(E('Patient', {'name': U(name), 'gender': 'Male'})))
    return src.getvalue()


@simple_service('GET', SERVICE_ID, 'xslt_rest_get', 'application/rdf+xml')
@xslt_rest('test/foaf.xslt', source=MakeFoafGraph, srcIsFn=True)
def rest_service(name='Chimezie Ogbuji'):
    pass


@simple_service('POST', SERVICE_ID, 'xslt_rest_post', 'application/rdf+xml')
@xslt_rest('test/foaf.xslt', source=MakeFoafGraph, srcIsFn=True)
def rest_service_post(body, ctype):
    pass


@simple_service('GET', SERVICE_ID, 'diglot_extensions_basic_test')
def test_diglot_extensions_basic(rootPath):

    def TestGraphUriFn(path, fName):
        return 'http://example.com%s' % path.split('.')[0]

    DestroyOrCreateDataset('mysqlDataset')
    mgr = GetDiglotManager(TestGraphUriFn)
    rt = TransformWithAkamuExtensions('<Root/>', open('test/diglot_extension_test1.xslt').read(), mgr)
    DestroyOrCreateDataset('mysqlDataset')
    doc = amara.parse(rt)
    assert doc.xml_select('/Answer/sparql:sparql/sparql:boolean[text() = "true"]', prefixes={'sparql': 'http://www.w3.org/2005/sparql-results#'})
    assert doc.xml_select('/Answer/Patient[@name = "Uche Ogbuji"]')
    assert doc.xml_select('/Answer/AfterChange/Patient[@name = "Chimezie Ogbuji"]')
    assert doc.xml_select('/Answer/AfterChange/FoundPatientViaExtensionFunction')
    return 'Success'