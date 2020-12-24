# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/adminish/index.py
# Compiled at: 2010-02-17 09:54:59
__doc__ = '\nIndexing and searching.\n'
import logging, os.path
from operator import itemgetter
from couchfti import index, search
from adminish.expand import expand
from dottedish import api
import xappy
log = logging.getLogger()

def create_classifier(model_type):

    def _classifier(doc):
        if doc.get('model_type') == model_type:
            return model_type

    return _classifier


def create_factory(model_type, i):

    def _factory(db, doc):
        ixdoc = xappy.UnprocessedDocument()
        ixdoc.id = doc['_id']
        for D in i:
            for data in D['data']:
                (data, num_items) = expand(data, doc)
                for n in xrange(num_items):
                    index_text = data % {'n': n} % api.dotted(doc)
                    print 'INDEX_TEXT', index_text
                    ixdoc.fields.append(xappy.Field(D['name'], index_text))

        return ixdoc

    return _factory


index_type = {'exact': xappy.FieldActions.INDEX_EXACT, 'full': xappy.FieldActions.INDEX_FREETEXT}

def create_fields(model_type, i):
    fields = []
    if len(i) == 0:
        return []
    for d in i:
        fields.append(([d['name'], index_type[d['type']]], {}))

    return fields


def create_indexes(config):
    indexes = {}
    for (type, data) in config['types'].items():
        if 'indexes' not in data or len(data['indexes']) == 0:
            continue
        index_data = data['indexes']
        index = {}
        index['path'] = type
        index['classifier'] = create_classifier(type)
        index['factories'] = {type: create_factory(type, index_data)}
        index['fields'] = create_fields(type, index_data)
        indexes[type] = index

    return indexes


class Indexer(index.Indexer):

    def __init__(self, db, path, **args):
        adminish_config = args.pop('adminish_config')
        indexes = create_indexes(adminish_config)
        index.Indexer.__init__(self, db, path, indexes, **args)


class Searcher(search.Searcher):

    def __init__(self, db, path, **args):
        adminish_config = args.pop('adminish_config')
        indexes = create_indexes(adminish_config)
        search.Searcher.__init__(self, db, path, indexes, **args)