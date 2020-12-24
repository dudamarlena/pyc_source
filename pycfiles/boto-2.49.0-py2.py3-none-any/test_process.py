# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/botnee/test/test_process.py
# Compiled at: 2012-08-16 08:19:59
__doc__ = '\nTesting of the text processing capabilities\n'
import botnee

def test_process_doc(test_data):
    try:
        for data in test_data:
            [ botnee.process.text.process_doc(doc, True) for doc in data['docs'] ]
            data['meta_dict'] = {}
            data['data_dict'] = {}

        result = True
    except Exception, e:
        print e
        result = False
        botnee.debug.debug_here()

    return (result, test_data)


def test_create_guid_indices(test_data):
    try:
        for data in test_data:
            data['meta_dict']['guids'] = botnee.process.text.create_guid_indices(data['docs'])

        result = True
    except Exception, e:
        print e
        result = False
        botnee.debug.debug_here()

    return (result, test_data)


def test_get_tokens_lists_by_guid(test_data):
    try:
        for data in test_data:
            data['meta_dict']['tokens_lists_by_guid'] = botnee.process.text.get_tokens_lists_by_guid(data['docs'])

        result = True
    except Exception, e:
        print e
        result = False
        botnee.debug.debug_here()

    return (result, test_data)


def test_create_dictionary(test_data):
    try:
        for data in test_data:
            assert len(data['meta_dict']['tokens_lists_by_guid']) > 0
            (data['meta_dict']['dictionary'], data['meta_dict']['hash_map']) = botnee.process.text.create_dictionary(data['meta_dict']['tokens_lists_by_guid'])

        result = True
    except Exception, e:
        print e
        result = False
        botnee.debug.debug_here()

    return (result, test_data)


def test_tokens_to_hash(test_data):
    try:
        for data in test_data:
            assert len(data['meta_dict']['tokens_lists_by_guid']) > 0
            data['meta_dict']['tokens_hash'] = botnee.process.text.tokens_to_hash(data['meta_dict']['tokens_lists_by_guid'])

        result = True
    except Exception, e:
        print e
        result = False
        botnee.debug.debug_here()

    return (result, test_data)


def test_calculate_tf(test_data):
    try:
        for data in test_data:
            (data['data_dict']['tf'], t) = botnee.process.vector_space_model.calculate_tf(data['meta_dict'])

        result = True
    except Exception, e:
        print e
        result = False
        botnee.debug.debug_here()

    return (
     result, test_data)


def test_calculate_idf(test_data):
    try:
        for data in test_data:
            (data['data_dict']['idf'], t) = botnee.process.vector_space_model.calculate_idf(data['data_dict']['tf'])

        result = True
    except Exception, e:
        print e
        result = False
        botnee.debug.debug_here()

    return (
     result, test_data)


def test_calculate_tfidf(test_data):
    try:
        for data in test_data:
            (data['data_dict']['tfidf'], t) = botnee.process.vector_space_model.calculate_tfidf(data['data_dict']['tf'], data['data_dict']['idf'])

        result = True
    except Exception, e:
        print e
        result = False
        botnee.debug.debug_here()

    return (result, test_data)


def test_calculate_kernel(test_data):
    try:
        for data in test_data:
            (data['data_dict']['K'], t) = botnee.process.vector_space_model.calculate_kernel(data['data_dict']['tfidf'])

        result = True
    except Exception, e:
        print e
        result = False
        botnee.debug.debug_here()

    return (result, test_data)


def test_merge_dictionaries(test_data):
    try:
        meta_dict0 = test_data[0]['meta_dict']
        meta_dict1 = test_data[1]['meta_dict']
        (meta_dict2, mapping0, mapping1) = botnee.process.text.merge_dictionaries(meta_dict0, meta_dict1)
        test_data[0]['mapping'] = mapping0
        test_data[1]['mapping'] = mapping1
        assert set(test_data[2]['meta_dict']['dictionary'].keys()) == set(meta_dict2['dictionary'].keys())
        assert set(test_data[2]['meta_dict']['dictionary'].values()) == set(meta_dict2['dictionary'].values())
        assert test_data[2]['meta_dict']['dictionary'] == meta_dict2['dictionary']
        assert test_data[2]['meta_dict']['hash_map'] == meta_dict2['hash_map']
        result = True
    except Exception, e:
        print e
        result = False
        botnee.debug.debug_here()

    return (result, test_data)


def test_merge_ids(test_data):
    try:
        ids2 = botnee.process.text.merge_ids(test_data[0]['meta_dict']['guids'], test_data[1]['meta_dict']['guids'])
        assert ids2 == test_data[2]['meta_dict']['guids']
        result = True
    except Exception, e:
        print e
        result = False
        botnee.debug.debug_here()

    return (result, test_data)


def test_merge_tokens(test_data):
    try:
        tokens_hash0 = test_data[0]['meta_dict']['tokens_hash']
        tokens_hash1 = test_data[1]['meta_dict']['tokens_hash']
        tokens_hash2 = botnee.process.text.merge_tokens(tokens_hash0, tokens_hash1)
        for (k, v) in test_data[2]['meta_dict']['tokens_hash'].iteritems():
            assert tokens_hash2.has_key(k)
            assert tokens_hash2[k] == v

        result = True
    except Exception, e:
        print e
        result = False
        botnee.debug.debug_here()

    return (result, test_data)


def test_merge_tf(test_data):
    try:
        tf0 = test_data[0]['data_dict']['tf']
        tf1 = test_data[1]['data_dict']['tf']
        mapping0 = test_data[0]['mapping']
        mapping1 = test_data[1]['mapping']
        tf2 = botnee.process.vector_space_model.merge_tf(tf0, mapping0, tf1, mapping1, len(test_data[2]['meta_dict']['dictionary']))
        tf2_ = test_data[2]['data_dict']['tf'].tocsr()
        assert all(tf2.data == tf2_.data)
        assert all(tf2.indices == tf2_.indices)
        assert all(tf2.indptr == tf2_.indptr)
        assert (tf2 - tf2_).nnz == 0
        result = True
    except Exception, e:
        print e
        result = False
        botnee.debug.debug_here()

    return (result, test_data)


def test_merge_idf(test_data):
    try:
        idf2 = botnee.process.vector_space_model.merge_idf(test_data[0]['data_dict']['idf'], test_data[0]['mapping'], test_data[0]['data_dict']['tf'].shape[0], test_data[1]['data_dict']['idf'], test_data[1]['mapping'], test_data[1]['data_dict']['tf'].shape[0], len(test_data[2]['meta_dict']['dictionary']))
        assert max(idf2 - test_data[2]['data_dict']['idf']) < 1e-10
        result = True
    except Exception, e:
        print e
        result = False
        botnee.debug.debug_here()

    return (result, test_data)


def test_merge_meta_dict(test_data):
    try:
        (test_data[2]['meta_dict'], test_data[0]['mapping'], test_data[1]['mapping']) = botnee.process.text.merge_meta_dict(test_data[0]['meta_dict'], test_data[1]['meta_dict'])
        result = True
    except Exception, e:
        print e
        result = False
        botnee.debug.debug_here()

    return (result, test_data)


def test_merge_data_dict(test_data):
    try:
        test_data[2]['data_dict'] = botnee.process.vector_space_model.merge_data_dict(test_data[0]['data_dict'], test_data[1]['data_dict'], test_data[0]['mapping'], test_data[1]['mapping'], test_data[2]['meta_dict'], verbose=True)
        result = True
    except Exception, e:
        print e
        result = False
        botnee.debug.debug_here()

    return (result, test_data)