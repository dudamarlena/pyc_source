# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/deepak.unni3/GIT/mvp-module-library-master/env/lib/python3.7/site-packages/Rhea/Rhea.py
# Compiled at: 2019-09-12 20:29:16
# Size of source mod 2**32: 5026 bytes
from SPARQLWrapper import SPARQLWrapper, JSON
from MyGene.mygene_client import QueryMyGene
from pprint import pprint
from UniProt.uniprot_sparql_wrapper import UniProtSparql

class RheaMethods(object):

    def __init__(self):
        self.endpoint = SPARQLWrapper('https://sparql.rhea-db.org/sparql')
        self.mygene = QueryMyGene()
        self.ups = UniProtSparql()

    def execute_query(self, query):
        self.endpoint.setQuery(query)
        self.endpoint.setReturnFormat(JSON)
        return self.endpoint.query().convert()

    def get_all_reactions_that_produce_compound(self, chebi):
        query = "PREFIX rh:<http://rdf.rhea-db.org/>\n            PREFIX ec:<http://purl.uniprot.org/enzyme/>\n            SELECT ?reaction ?reactionEquation  ?ecNumber ?chebi_id ?curatedOrder WHERE {\n              ?reaction rdfs:subClassOf rh:Reaction;\n                        rh:status rh:Approved;\n                        rh:ec ?ecNumber;\n                        rh:directionalReaction ?directional_reaction.\n              ?directional_reaction rh:status rh:Approved;\n                                    rh:products ?productside;\n                                    rh:equation ?reactionEquation.\n              ?productside rh:curatedOrder ?curatedOrder;\n                           rh:contains ?products.\n              ?products rh:compound ?small_molecule.\n              ?small_molecule rh:accession '%s';\n                              rh:accession ?chebi_id.\n            }\n        " % chebi
        return self.execute_query(query)

    def get_all_reactions_that_consume_compound(self, chebi):
        query = "PREFIX rh:<http://rdf.rhea-db.org/>\n        SELECT ?reaction ?reactionEquation  ?ecNumber ?chebi_id  ?curatedOrder ?substrates WHERE {\n              ?reaction rdfs:subClassOf rh:Reaction;\n                            rh:status rh:Approved;\n                            rh:ec ?ecNumber;\n                            rh:directionalReaction ?directional_reaction.\n                            \n              ?directional_reaction rh:status rh:Approved;\n                        rh:equation ?reactionEquation;\n                        rh:substrates ?substrateside.\n              ?substrateside rh:curatedOrder ?curatedOrder;\n                             rh:contains ?substrates.\n              ?substrates rh:compound ?small_molecule.\n              ?small_molecule rh:accession '%s';\n                              rh:accession ?chebi_id.\n            }\n        " % chebi
        return self.execute_query(query)

    def get_reaction_by_ec(self, ec):
        query = 'PREFIX rh:<http://rdf.rhea-db.org/>\n            PREFIX ec:<http://purl.uniprot.org/enzyme/>\n            SELECT ?reaction ?reactionEquation ?ecNumber ?chebi_id ?curatedOrder WHERE {\n              ?reaction rdfs:subClassOf rh:Reaction;\n                        rh:status rh:Approved;\n                        rh:ec ?ecNumber;\n                        rh:directionalReaction ?directional_reaction.\n              ?directional_reaction rh:products ?productside;\n                                    rh:equation ?reactionEquation.\n              ?productside rh:curatedOrder ?curatedOrder;\n                           rh:contains ?products.\n              ?products rh:compound ?small_molecule.\n              ?small_molecule rh:accession ?chebi_id.\n              FILTER (?ecNumber=ec:%s)\n            }\n        ' % ec
        return self.execute_query(query)

    def product2gene(self, chebi):
        outputs = []
        reactions = self.get_all_reactions_that_produce_compound(chebi=chebi)
        for reaction in reactions['results']['bindings']:
            if reaction['curatedOrder'] == 2:
                ec = reaction['ecNumber']['value'].split('/')[(-1)]
                output = {'input':chebi, 
                 'type':'products', 
                 'proteins':self.ups.ec2uniprot(ec=ec), 
                 'ec':ec, 
                 'rheaid':reaction['reaction']['value'], 
                 'reaction':reaction['reactionEquation']['value']}
                outputs.append(output)

        return outputs

    def substrate2gene(self, chebi):
        outputs = []
        reactions = self.get_all_reactions_that_consume_compound(chebi=chebi)
        for reaction in reactions['results']['bindings']:
            ec = reaction['ecNumber']['value'].split('/')[(-1)]
            output = {'input':chebi, 
             'type':'substrates', 
             'proteins':self.ups.ec2uniprot(ec=ec), 
             'ec':ec, 
             'rheaid':reaction['reaction']['value'], 
             'reaction':reaction['reactionEquation']['value']}
            outputs.append(output)

        return outputs

    def gene2product(self, ncbigene):
        mg = self.mygene.query_mygene(curie=ncbigene)
        uniprot = ''
        if len(mg) == 1:
            uniprot = ''.join(self.mygene.parse_uniprot(mg[0]))
        ec = self.ups.uniprot2ec(uniprot)