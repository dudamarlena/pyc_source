# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Library/Python/2.6/site-packages/akamu/demo/protocol.py
# Compiled at: 2013-07-19 12:00:40
__author__ = 'chimezieogbuji'
from akara.services import simple_service, service
from akamu.protocol.grddlstore import grddl_graphstore_resource
SERVICE_ID = 'http://code.google.com/p/akamu/wiki/DiglotFileSystemProtocol'

def TestGraphUriFn(path, fName):
    return 'http://example.com%s' % path.split('.')[0]


def ReverseTransform(graph):
    from rdflib import Namespace, RDF
    from amara.writers.struct import structwriter, E, ROOT
    from cStringIO import StringIO
    FOAF = Namespace('http://xmlns.com/foaf/0.1/')
    V = Namespace('http://www.w3.org/2006/vcard/ns#')
    src = StringIO()
    w = structwriter(indent='yes', stream=src)

    def attributes(personUri):
        attr = {}
        for _name in graph.query('SELECT ?name [] a foaf:Person; foaf:businessCard [ v:fn ?name ]', initNs={'foaf': FOAF, 'v': V}):
            attr['name'] = _name

        return attr

    for person in graph.subjects(RDF.type, FOAF.Person):
        w.feed(ROOT(E('Patient', attributes(person))))

    return src.getvalue()


@service(SERVICE_ID, 'diglot')
@grddl_graphstore_resource('/diglot', TestGraphUriFn, caching=False)
def grddl_graphstore_protocol():
    pass