# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /emmo/tests/test_query.py
# Compiled at: 2020-04-17 14:04:49
# Size of source mod 2**32: 486 bytes
from emmo import get_ontology
emmo = get_ontology('https://emmo-repo.github.io/versions/1.0.0-alpha/emmo-inferred.owl')
emmo.load()
query = f"\n    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n    PREFIX owl: <http://www.w3.org/2002/07/owl#>\n    SELECT ?cls\n    WHERE ?cls owl:subClassOf <{emmo.Physical.iri}> .\n    "
g = emmo.world.as_rdflib_graph()
print(list(g.query(query)))