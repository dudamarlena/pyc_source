# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/botnee/test/test_corpus.py
# Compiled at: 2012-08-16 08:19:42
"""
Testing of the Corpus class functions
"""
from time import time
import sys, hashlib, os, glob, botnee, botnee_config

def test_read_json(test_data):
    try:
        test_data = []
        prefix = botnee_config.DATA_DIRECTORY + 'test/json/'
        fnames = ['gutjnl-small-test.txt',
         'jnnp-small-test.txt',
         'combined-small-test.txt']
        for fname in fnames:
            fname = prefix + fname
            test_data.append({'jobjs': botnee.corpus.read_json(fname), 'fname': fname})

        for data in test_data:
            data['meta_dict']['guids'] = {}
            if isinstance(data['jobjs'], dict):
                sys.stdout.write(str(data['jobjs']['id']) + '...')
                data['meta_dict']['guids'][data['jobjs']['id']] = 0
            else:
                for (i, jobj) in enumerate(data['jobjs']):
                    sys.stdout.write('\n' + str(i) + ':' + str(jobj['id']) + '...')
                    data['meta_dict']['guids'][jobj['id']] = i

                assert len(set(data['meta_dict']['guids'].values())) == len(data['meta_dict']['guids'])
                assert len(set(data['meta_dict']['guids'].keys())) == len(data['meta_dict']['guids'])

        result = len(test_data) == 3
    except Exception, e:
        print e
        test_data = None
        result = False
        botnee.debug.debug_here()

    return (
     result, test_data)


def test_get_all_text(test_data):
    try:
        for data in test_data:
            data['tokens_list'] = []
            for jobj in data['jobjs']:
                text = botnee.corpus.get_all_text(jobj)
                (text, data_dict) = botnee.process.text.process_text(text)
                data['meta_dict']['tokens_list'].append(data_dict['meta_dict']['tokens'])

        result = True
    except Exception, e:
        print e
        result = False
        botnee.debug.debug_here()

    return (
     result, test_data)


def test_update(test_data):
    try:
        result = True
    except Exception, e:
        print e
        result = False
        botnee.debug.debug_here()

    return (
     result, test_data)


def test_Corpus(test_data):
    try:
        for data in test_data:
            fname = 'test/hdf5/' + hashlib.md5(str(time())).hexdigest()
            data['corpus'] = botnee.corpus.Corpus(fname)
            data['corpus'].update(data['meta_dict'], data['data_dict'], reindex=True, verbose=True)
            dtmp = data['corpus'].get_dictionary(as_bidict=True)
            assert dtmp == data['meta_dict']['dictionary']

        result = True
    except Exception, e:
        print e
        result = False
        botnee.debug.debug_here()

    return (
     result, test_data)


def test_merge_corpora(test_data):
    try:
        assert len(test_data) == 3
        fname = hashlib.md5(str(time())).hexdigest()
        corpus2 = botnee.corpus.Corpus('test/hdf5/' + fname)
        test_data[0]['corpus'].merge(test_data[1]['corpus'], corpus2)
        corpus2_ = test_data[2]['corpus']
        assert corpus2.get_dictionary(as_bidict=True) == corpus2_.get_dictionary(as_bidict=True)
        tokens_hash2 = corpus2.get_tokens()
        tokens_hash2_ = corpus2_.get_tokens()
        assert tokens_hash2 == tokens_hash2_
        ids2 = corpus2.get_guids()
        ids2_ = corpus2_.get_guids()
        assert ids2 == ids2_
        assert [ len(x) for x in tokens_hash2 ] == [ len(x) for x in tokens_hash2_ ]
        assert [ token for tokens in tokens_hash2 for token in tokens ] == [ token for tokens in tokens_hash2_ for token in tokens ]
        tf2 = corpus2.get_sparse_matrix('tf')
        tf2_ = corpus2_.get_sparse_matrix('tf')
        assert all(tf2.data == tf2_.data)
        assert all(tf2.indices == tf2_.indices)
        assert all(tf2.indptr == tf2_.indptr)
        idf2 = corpus2.get_idf()
        idf2_ = corpus2_.get_idf()
        assert max(idf2[:] - idf2_[:]) < 1e-10
        result = True
    except Exception, e:
        print e
        result = False
        botnee.debug.debug_here()

    return (
     result, test_data)


def test_stress(test_data):
    """ Stress test of system by merging corpora many times """
    [ os.remove(f) for f in glob.glob(botnee_config.DATA_DIRECTORY + 'test/hdf5/*.h5') ]
    print ''
    print ''
    print 'Running stress test with 10 random documents per iteration.'
    print 'Please indicate how many merge operations to complete: '
    x = -1
    while x == -1:
        try:
            x = int(raw_input())
        except ValueError:
            print 'Invalid Number'

    if x < 1:
        return (True, test_data)
    import nltk
    text_generator = nltk.Text(nltk.corpus.brown.words())
    text_generator.generate()
    verbose = True
    parallel = False
    try:
        try:
            corpus_list = []
            corpus_list.append(botnee.corpus.Corpus('test/hdf5/Merged_corpus_test_0'))
            test_data[0]['corpus'].merge(test_data[1]['corpus'], corpus_list[0])
            for i in range(x):
                fname = 'test/hdf5/Merged_corpus_test_' + str(i + 1)
                corpus_list.append(botnee.corpus.Corpus(fname))
                corpus_random = botnee.corpus.Corpus('test/hdf5/Merged_corpus_test_random_data')
                docs = []
                for j in range(10):
                    random_string = ('').join([ token + ' ' for token in text_generator._trigram_model.generate(100) ])
                    random_id = hashlib.md5(random_string).hexdigest()
                    docs.append({'body': random_string, 'guid': random_id})

                meta_dict = {}
                data_dict = {}
                botnee.process.text.process_docs(docs, meta_dict, True, verbose, parallel)
                tdict = botnee.process.vector_space_model.vector_space_model(meta_dict, data_dict, True, verbose, parallel)
                corpus_random.update(meta_dict, data_dict, reindex=True, verbose=True)
                corpus_list[0].merge(corpus_random, corpus_list[1])
                corpus_list[0].close()
                del corpus_list[0]
                os.remove(botnee_config.DATA_DIRECTORY + fname + '_corpus_table.h5')
                corpus_random.close()
                del corpus_random
                os.remove(botnee_config.DATA_DIRECTORY + 'test/hdf5/Merged_corpus_test_random_data_corpus_table.h5')

            result = True
        except Exception, e:
            print e
            result = False
            botnee.debug.debug_here()

    finally:
        [ os.remove(f) for f in glob.glob(botnee_config.DATA_DIRECTORY + 'test/hdf5/*.h5') ]

    return (
     result, test_data)