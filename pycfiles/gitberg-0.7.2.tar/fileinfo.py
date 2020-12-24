# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/eric/github/local/gitberg/gitenberg/metadata/fileinfo.py
# Compiled at: 2020-01-02 14:52:16
import rdflib
from datetime import datetime
from six import text_type as unicodestr
from rdflib_jsonld import serializer
from .pg_rdf import unblank_node, context

def htm_modified(file_path):
    g = rdflib.Graph()
    try:
        g.load(file_path)
    except IOError:
        return

    ld = serializer.from_rdf(g, context_data=context, base=None, use_native_types=False, use_rdf_type=False, auto_compact=False, startnode=None, index=False)
    graph = ld['@graph']
    nodes = {}
    for obj in graph:
        if isinstance(obj, dict):
            obj = obj.copy()
            if '@id' in obj and obj['@id'].startswith('_'):
                nodeid = obj['@id']
                node = nodes.get(nodeid, {})
                del obj['@id']
                node.update(obj)
                nodes[nodeid] = node

    newnodes = []
    top = None
    for obj in unblank_node(graph, nodes):
        try:
            if obj['@type'] == 'pgterms:file':
                if unicodestr(obj['@id']).endswith('.htm'):
                    return obj['dcterms:modified']['@value']
        except:
            pass

    return


def htm_modified_date(file_path):
    mod = htm_modified(file_path)
    if mod:
        return datetime.strptime(mod, '%Y-%m-%dT%H:%M:%S')