# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.6/site-packages/akamu/demo/gsp.py
# Compiled at: 2012-10-17 10:28:36
__author__ = 'chimezieogbuji'
from akara.services import service, simple_service
from akamu.protocol.sparql import graph_store_protocol, sparql_rdf_protocol
from akamu.config.dataset import DestroyOrCreateDataset, GetGraphStoreForProtocol
SERVICE_ID = 'http://code.google.com/p/akamu/wiki/GraphStoreProtocol'

@service(SERVICE_ID, 'graph_store')
@graph_store_protocol()
def gsp_implementation():
    pass


@service(SERVICE_ID, 'sparql', wsgi_wrapper=sparql_rdf_protocol('/sparql', 'mysqlDataset'))
def sparql_rdf_protocol_service():
    pass


@simple_service('GET', SERVICE_ID, 'gsp.validator.clear', 'text/plain')
def validation():
    (dataset, gs_url) = GetGraphStoreForProtocol()
    DestroyOrCreateDataset(dataset)
    return ('Reset ', dataset)