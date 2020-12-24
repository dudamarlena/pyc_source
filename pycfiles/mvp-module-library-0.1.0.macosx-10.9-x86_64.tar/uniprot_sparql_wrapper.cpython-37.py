# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/deepak.unni3/GIT/mvp-module-library-master/env/lib/python3.7/site-packages/UniProt/uniprot_sparql_wrapper.py
# Compiled at: 2019-09-12 20:29:16
# Size of source mod 2**32: 1661 bytes
from SPARQLWrapper import SPARQLWrapper, JSON

class UniProtSparql(object):

    def __init__(self):
        self.endpoint = SPARQLWrapper('http://sparql.uniprot.org/sparql/')

    def execute_query(self, query):
        self.endpoint.setQuery(query)
        self.endpoint.setReturnFormat(JSON)
        return self.endpoint.query().convert()

    def ec2uniprot(self, ec):
        query = '\n         PREFIX up:<http://purl.uniprot.org/core/> \n        PREFIX ec:<http://purl.uniprot.org/enzyme/> \n        PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#> \n        SELECT ?protein \n        WHERE\n        {\n         ?protein up:enzyme ?enzyme.\n          FILTER (?enzyme=ec:%s)\n        }\n        ' % ec
        results = self.execute_query(query=query)
        uniprots = []
        for hit in results['results']['bindings']:
            uniprots.append(hit['protein']['value'].split('/')[(-1)])

        return uniprots

    def uniprot2ec(self, uniprot):
        query = '\n        BASE <http://purl.uniprot.org/uniprot/> \n        PREFIX ec:<http://purl.uniprot.org/enzyme/>\n        PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#> \n        PREFIX up:<http://purl.uniprot.org/core/> \n        \n        SELECT ?protein ?enzyme\n        WHERE\n        {\n            VALUES ?protein {<%s>}\n            ?protein a up:Protein;\n                up:enzyme ?enzyme.\n            ?enzyme rdfs:subClassOf ?ecClass. \n        }\n        ' % uniprot
        results = self.execute_query(query=query)
        ecnumbers = []
        for hit in results['results']['bindings']:
            ecnumbers.append(hit['enzyme']['value'].split('/')[(-1)])

        return ecnumbers