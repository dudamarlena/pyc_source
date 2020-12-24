# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dossier/models/tests/test_pairwise.py
# Compiled at: 2015-07-08 07:34:06
"""Exercises the pairwise active learning model.

Note that these tests aren't really machine learning tests. They
are emphatically unit tests. Therefore, when these tests pass, one
should not use that as evidence to conclude that learning is
implemented correctly. The tests only check whether the output of
functions matches this programmer's expectation.
"""
from __future__ import absolute_import, division, print_function
import pytest
from dossier.fc import FeatureCollection, StringCounter
from dossier.label import Label, CorefValue
from dossier.web import Folders
from dossier.models import PairwiseFeatureLearner
import dossier.models.pairwise as mod_pairwise
from dossier.models.tests import kvl, store, label_store

@pytest.fixture
def pairwise(store, label_store):
    store.put([('q', counter_fc({'fubar': 5, 'hi': 1}))])
    return PairwiseFeatureLearner(store, label_store, 'q')


def counter_fc(bow):
    return FeatureCollection({'feature': bow})


def pos_label(id1, id2):
    return Label(id1, id2, '', CorefValue.Positive)


def neg_label(id1, id2):
    return Label(id1, id2, '', CorefValue.Negative)


@pytest.mark.xfail
def test_subtopic_labels(kvl, store, label_store):

    def lab(cid1, sid1, cid2, sid2, neg=False):
        coref_val = CorefValue.Negative if neg else CorefValue.Positive
        return Label(cid1, cid2, 'unknown', coref_val, sid1, sid2)

    nlab = lambda a, b, c, d: lab(a, b, c, d, neg=True)

    def has_label(haystack, needle):
        return any(lab.same_subject_as(needle) and lab.value == needle.value for lab in haystack)

    folders = Folders(kvl)
    folders.add_folder('top')
    folders.add_item('top', 'foo', 'a', 'ax')
    folders.add_item('top', 'foo', 'b', 'bx')
    folders.add_item('top', 'bar', 'c', 'cx')
    folders.add_item('top', 'bar', 'd', 'dx')
    folders.add_folder('other')
    folders.add_item('other', 'baz', 'e', 'ex')
    label_store.put(nlab('a', 'ax', 'r', None))
    label_store.put(nlab('b', 'bx', 'r', None))
    pairwise = PairwiseFeatureLearner(store, label_store, 'a', 'ax')
    labels = pairwise.infer_subtopic_labels()
    print(('\n').join(map(repr, labels)))
    assert has_label(labels, nlab('a', 'ax', 'e', 'ex'))
    assert has_label(labels, nlab('a', 'ax', 'c', 'cx'))
    assert has_label(labels, nlab('a', 'ax', 'd', 'dx'))
    assert has_label(labels, lab('a', 'ax', 'b', 'bx'))
    assert has_label(labels, nlab('a', 'ax', 'r', None))
    assert has_label(labels, nlab('b', 'bx', 'r', None))
    assert len(labels) == 8
    return


def test_canopy(pairwise):
    """Make sure canopies are using indexes correctly."""
    pairwise.store.put([
     (
      'abc', counter_fc({'fubar': 1})),
     (
      'xyz', counter_fc({'foo': 1})),
     (
      'mno', counter_fc({'hi': 10}))])
    pairwise.query_fc = pairwise.store.get(pairwise.query_content_id)
    canopy = pairwise.canopy()
    assert set([ cid for cid, _ in canopy ]) == set(['abc', 'mno'])


def test_canopy_limit(pairwise):
    """Make sure canopies are using indexes correctly."""
    pairwise.store.put([
     (
      'abc', counter_fc({'fubar': 1})),
     (
      'xyz', counter_fc({'foo': 1})),
     (
      'mno', counter_fc({'hi': 10})),
     (
      'def', counter_fc({'hi': 10})),
     (
      'ghi', counter_fc({'hi': 10}))])
    pairwise.query_fc = pairwise.store.get(pairwise.query_content_id)
    canopy = pairwise.canopy()
    assert len(canopy) == 4
    limited = pairwise.canopy(limit=2)
    assert len(limited) == 2


def test_labels(pairwise):
    """Make sure we get the right labels.

    The "right" labels means: label expansion on the connected
    component of the query.

    This doesn't test negative label inference.
    """
    pairwise.label_store.put(pos_label('q', 'a'))
    pairwise.label_store.put(pos_label('a', 'b'))
    pairwise.label_store.put(pos_label('y', 'z'))
    fs = lambda *args: frozenset(args)
    got = set([ fs(lab.content_id1, lab.content_id2) for lab in pairwise.labels_from_query()
              ])
    assert got == set([
     fs('q', 'a'), fs('a', 'b'),
     fs('q', 'b')])


def test_label_limit(pairwise):
    """Make sure label limiting works."""
    pairwise.label_store.put(pos_label('q', 'a'))
    pairwise.label_store.put(pos_label('a', 'b'))
    pairwise.label_store.put(neg_label('q', 'y'))
    pairwise.label_store.put(neg_label('y', 'z'))
    fs = lambda *args: frozenset(args)
    got = set([ fs(lab.content_id1, lab.content_id2) for lab in pairwise.labels_from_query(limit=2)
              ])
    assert len(got) <= 4


def test_label_indexing():
    """Make sure labels get converted to indices correctly."""
    content_objs = [
     (
      'a', counter_fc({})),
     (
      'b', counter_fc({})),
     (
      'c', counter_fc({}))]
    labels = [
     pos_label('a', 'c'),
     pos_label('c', 'b'),
     neg_label('b', 'a')]
    indiced = mod_pairwise.labels_to_indexed_coref_values(content_objs, labels)
    assert indiced == [
     (1, 0, 2),
     (1, 1, 2),
     (-1, 0, 1)]


def test_vectorizable_features():
    """Make sure we only do learning on the right features.

    The "right" features means features that can be vectorized
    by sklearn. Translation: they must be instances of
    collections.Mapping.
    """
    fc = FeatureCollection({'yes': {'fubar': 1}, 'no': 'haha'})
    got = mod_pairwise.vectorizable_features([fc])
    assert got == ['yes']


def test_dissimilarities():
    """Make sure computing dissimilarities works like we expect.

    This is probably too rigid.
    """
    from numpy.testing import assert_approx_equal
    from scipy.spatial.distance import cosine
    fcs = [
     counter_fc({'a': 1, 'b': 2}),
     counter_fc({'a': 2, 'b': 3}),
     counter_fc({'a': 20, 'b': 0})]
    dis = mod_pairwise.dissimilarities(['feature'], fcs)['feature']
    got = [
     dis[0][1], dis[0][2], dis[1][2]]
    exp = [
     1 - cosine([1, 2], [2, 3]),
     1 - cosine([1, 2], [20, 0]),
     1 - cosine([2, 3], [20, 0])]
    [ assert_approx_equal(got[i], exp[i]) for i in xrange(len(got)) ]


def interesting_training_data():
    """Returns ([(content_id, FeatureCollection)], [Label])"""
    return (
     [
      (
       'a', counter_fc({'ignored': 1, 'x': 50, 'y': 0})),
      (
       'b', counter_fc({'x': 0, 'y': 100})),
      (
       'c', counter_fc({'x': 0, 'y': 101})),
      (
       'd', counter_fc({'x': 0, 'y': 101})),
      (
       'e', counter_fc({'x': 0, 'y': 101})),
      (
       'f', counter_fc({'x': 0, 'y': 101})),
      (
       'g', counter_fc({'x': 0, 'y': 101}))],
     [
      neg_label('a', 'c'),
      neg_label('a', 'b'),
      pos_label('b', 'c'),
      pos_label('b', 'd'),
      pos_label('b', 'e'),
      pos_label('b', 'f'),
      pos_label('b', 'g')])


def test_training(pairwise):
    """Tests that training does something."""
    from numpy.testing import assert_approx_equal
    content_objs, labels = interesting_training_data()
    indiced = mod_pairwise.labels_to_indexed_coref_values(content_objs, labels)
    names, model, vec = pairwise.train(content_objs, indiced)
    assert names == vec.get_feature_names()
    assert_approx_equal(model.coef_[0][0], 0.61903921)
    assert model.classes_.tolist() == [-1, 1]


@pytest.mark.xfail
def test_classify(pairwise):
    """Tests the whole kit and kaboodle."""
    content_objs, labels = interesting_training_data()
    pairwise.store.put(content_objs)
    for lab in labels:
        pairwise.label_store.put(lab)

    pairwise.store.put([('q', counter_fc({'x': 5, 'y': 90}))])
    pairwise.label_store.put(neg_label('q', 'a'))
    pairwise.label_store.put(pos_label('q', 'b'))
    candidate_probs = pairwise.probabilities()
    id_to_prob = dict([ (cid, p) for (cid, _), p in candidate_probs ])
    assert all([ id_to_prob['a'] <= id_to_prob[cid] for cid in id_to_prob ])


def test_search_engine(store, label_store):
    """Pretty much the same as classify, but for the search engine."""
    content_objs, labels = interesting_training_data()
    store.put(content_objs)
    for lab in labels:
        label_store.put(lab)

    store.put([('q', counter_fc({'x': 5, 'y': 90}))])
    label_store.put(pos_label('q', 'b'))
    label_store.put(neg_label('q', 'a'))
    label_store.put(neg_label('q', 'b'))
    label_store.put(neg_label('q', 'c'))
    results = mod_pairwise.similar(store, label_store).set_query_id('q').set_query_params({'limit': 1}).recommendations()
    assert results['results'][0][0] != 'a'


def test_search_engine_limit(store, label_store):
    """Pretty much the same as classify, but for the search engine."""
    content_objs, labels = interesting_training_data()
    store.put(content_objs)
    for lab in labels:
        label_store.put(lab)

    store.put([('q', counter_fc({'x': 5, 'y': 90}))])
    label_store.put(neg_label('q', 'a'))
    label_store.put(pos_label('q', 'b'))
    results = mod_pairwise.similar(store, label_store).set_query_id('q').set_query_params({'limit': 2}).recommendations()
    assert len(results['results']) == 2


def test_no_labels(store, label_store):
    """Make sure the learner can handle zero labels."""
    store.put([('q', counter_fc({'x': 5, 'y': 90}))])
    results = mod_pairwise.similar(store, label_store).set_query_id('q').set_query_params({'limit': 1}).recommendations()
    assert len(results['results']) == 0


def test_only_positive_labels(store, label_store):
    """Make sure the learner can handle one class of labels."""
    content_objs, labels = interesting_training_data()
    store.put(content_objs)
    for lab in labels:
        if lab.value == CorefValue.Positive:
            label_store.put(lab)

    store.put([('q', counter_fc({'x': 5, 'y': 90}))])
    label_store.put(pos_label('q', 'b'))
    results = mod_pairwise.similar(store, label_store).set_query_id('q').set_query_params({'limit': 100}).recommendations()
    assert len(results['results']) >= 0


def test_only_negative_labels(store, label_store):
    """Make sure the learner can handle one class of labels."""
    content_objs, labels = interesting_training_data()
    store.put(content_objs)
    for lab in labels:
        if lab.value == CorefValue.Negative:
            label_store.put(lab)

    store.put([('q', counter_fc({'x': 5, 'y': 90}))])
    label_store.put(neg_label('q', 'a'))
    results = mod_pairwise.similar(store, label_store).set_query_id('q').set_query_params({'limit': 100}).recommendations()
    assert len(results['results']) >= 0


def test_add_facets():
    cid1 = 'cid1'
    fc1 = FeatureCollection()
    fc1['bowNP_sip'] = StringCounter(['elephant', 'car'])
    cid2 = 'cid2'
    fc2 = FeatureCollection()
    fc2['bowNP_sip'] = StringCounter(['car', 'green'])
    fake_results = {'results': [(cid1, fc1), (cid2, fc2)]}
    new_results = mod_pairwise.add_facets(fake_results)
    assert 'facets' in new_results
    assert new_results['facets'] == {'elephant': [
                  cid1], 
       'car': [
             cid1, cid2], 
       'green': [
               cid2]}