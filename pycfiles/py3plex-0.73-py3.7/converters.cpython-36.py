# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/blazs/Py3Plex/py3plex/algorithms/hedwig/core/converters.py
# Compiled at: 2018-08-23 02:03:57
# Size of source mod 2**32: 1580 bytes
import rdflib

def convert_mapping_to_rdf(mapping_file):
    g = rdflib.graph.Graph()
    KT = rdflib.Namespace('http://kt.ijs.si/hedwig#')
    amp_uri = 'http://kt.ijs.si/ontology/hedwig#'
    obo_uri = 'http://purl.obolibrary.org/obo/'
    AMP = rdflib.Namespace(amp_uri)
    if include_induced_neighborhood:
        ntuple = [(k.split(':')[1], v) for k, v in predictions.items()]
    else:
        ntuple = [(x.split(' ')[0], x.split(' ')[1]) for x in community_map]
    id_identifier = 0
    uniGO = parse_gaf_file(mapping_file)
    for node, com in ntuple:
        try:
            id_identifier += 1
            u = rdflib.term.URIRef('%sexample#%s%s' % (amp_uri, node, str(id_identifier)))
            g.add((u, rdflib.RDF.type, KT.Example))
            g.add((u, KT.class_label, rdflib.Literal(str(com) + '_partition')))
            for goterm in uniGO[node]:
                if 'GO:' in goterm:
                    annotation_uri = rdflib.term.URIRef('%s%s' % (obo_uri, rdflib.Literal(goterm)))
                    blank = rdflib.BNode()
                    g.add((u, KT.annotated_with, blank))
                    g.add((blank, KT.annotation, annotation_uri))

        except:
            pass

    return g