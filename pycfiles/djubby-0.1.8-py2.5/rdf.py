# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/djubby/rdf.py
# Compiled at: 2010-04-26 06:15:48
from rdflib import URIRef

def str2uri(uri):
    if type(uri) == str or type(uri) == unicode:
        return URIRef(uri)
    else:
        return uri


def get_values(graph, subject=None, predicate=None):
    return graph.objects(subject=str2uri(subject), predicate=predicate)


def get_value(graph, subject=None, predicate=None, lang=None):
    if lang == None:
        try:
            return str(get_values(graph, subject, predicate).next())
        except StopIteration:
            return ''

    else:
        values = get_values(graph, subject, predicate)
        for value in values:
            if value.language == lang:
                return value

        return ''
    return


def get_predicates(graph, subject=None):
    return graph.predicate_objects(str2uri(subject))