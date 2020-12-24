# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pagingish/tests/test_couchdbpager.py
# Compiled at: 2009-05-05 06:00:17
import uuid
from unittest import TestCase
from createdata import create_items
import couchdb
from couchdb.design import ViewDefinition
from pagingish.couchdbpager import Pager
dbname = 'test-paging'
model_type = 'test'

def create_view(db, design_doc, name, map_fun, reduce_fun=None):
    view = ViewDefinition(design_doc, name, map_fun, reduce_fun)
    view.get_doc(db)
    view.sync(db)


def sequence_generator(num):
    for n in xrange(num):
        data = {'_id': 'id-%s' % n, 'model_type': model_type, 
           'num': n}
        yield data


def assert_page(page, prev, rows, next, stats, expecteds):
    if page > len(expecteds):
        expected = expecteds[(-1)]
    else:
        expected = expecteds[(page - 1)]
    actual = [ r.key for r in rows ]
    assert expected == actual
    if page >= len(expecteds) or page < len(expecteds) and len(expecteds) == 1:
        assert next is None
    else:
        assert next is not None
    if page <= 1 or page > len(expecteds) and len(expecteds) == 1:
        assert prev is None
    else:
        assert prev is not None
    return


e5pp_10t = [
 [
  0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]
e4pp_10t = [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9]]

def t(d):
    return (
     d['prev'], d['items'], d['next'], d['stats'])


class TestCouchDBPager_10items(TestCase):

    def setUp(self):
        self.db = create_items(dbname, force_create=True, model_type=model_type, items=sequence_generator(10))
        map_fun = 'function(doc) { if (doc.model_type == "%s") { emit(doc.num, 1); } }' % model_type
        reduce_fun = 'function(keys, values) { return sum(values) }'
        create_view(self.db, model_type, 'all', map_fun)
        create_view(self.db, model_type, 'count', map_fun, reduce_fun)

    def test_roundtrip_5pp(self):
        p = Pager(self.db.view, '%s/all' % model_type)
        (prev, rows, next, stats) = t(p.get(5, None))
        assert_page(1, prev, rows, next, stats, e5pp_10t)
        (prev, rows, next, stats) = t(p.get(5, next))
        assert_page(2, prev, rows, next, stats, e5pp_10t)
        (prev, rows, next, stats) = t(p.get(5, prev))
        assert_page(1, prev, rows, next, stats, e5pp_10t)
        return

    def test_roundtrip_4pp(self):
        p = Pager(self.db.view, '%s/all' % model_type)
        (prev, rows, next, stats) = t(p.get(4, None))
        assert_page(1, prev, rows, next, stats, e4pp_10t)
        (prev, rows, next, stats) = t(p.get(4, next))
        assert_page(2, prev, rows, next, stats, e4pp_10t)
        (prev, rows, next, stats) = t(p.get(4, next))
        assert_page(3, prev, rows, next, stats, e4pp_10t)
        (prev, rows, next, stats) = t(p.get(4, prev))
        assert_page(2, prev, rows, next, stats, e4pp_10t)
        (prev, rows, next, stats) = t(p.get(4, prev))
        assert_page(1, prev, rows, next, stats, e4pp_10t)
        return

    def test_upone_downone_4pp(self):
        p = Pager(self.db.view, '%s/all' % model_type)
        (prev, rows, next, stats) = t(p.get(4, None))
        assert_page(1, prev, rows, next, stats, e4pp_10t)
        (prev, rows, next, stats) = t(p.get(4, next))
        assert_page(2, prev, rows, next, stats, e4pp_10t)
        (prev, rows, next, stats) = t(p.get(4, prev))
        assert_page(1, prev, rows, next, stats, e4pp_10t)
        return

    def test_prev_at_start_4pp(self):
        p = Pager(self.db.view, '%s/all' % model_type)
        (prev, rows, next, stats) = t(p.get(4, None))
        assert_page(1, prev, rows, next, stats, e4pp_10t)
        (prev, rows, next, stats) = t(p.get(4, next))
        assert_page(2, prev, rows, next, stats, e4pp_10t)
        (prev, rows, next, stats) = t(p.get(4, prev))
        assert_page(1, prev, rows, next, stats, e4pp_10t)
        (prev, rows, next, stats) = t(p.get(4, prev))
        assert_page(1, prev, rows, next, stats, e4pp_10t)
        return


e5pp_5t = [
 [
  0, 1, 2, 3, 4]]
e4pp_5t = [[0, 1, 2, 3], [4]]
e6pp_5t = [[0, 1, 2, 3, 4]]

class TestCouchDBPager_5items(TestCase):

    def setUp(self):
        self.db = create_items(dbname, force_create=True, model_type=model_type, items=sequence_generator(5))
        map_fun = 'function(doc) { if (doc.model_type == "%s") { emit(doc.num, 1); } }' % model_type
        reduce_fun = 'function(keys, values) { return sum(values) }'
        create_view(self.db, model_type, 'all', map_fun)
        create_view(self.db, model_type, 'count', map_fun, reduce_fun)

    def test_roundtrip_5pp(self):
        p = Pager(self.db.view, '%s/all' % model_type)
        (prev, rows, next, stats) = t(p.get(5, None))
        assert_page(1, prev, rows, next, stats, e5pp_5t)
        return

    def test_roundtrip_4pp(self):
        p = Pager(self.db.view, '%s/all' % model_type)
        (prev, rows, next, stats) = t(p.get(4, None))
        assert_page(1, prev, rows, next, stats, e4pp_5t)
        (prev, rows, next, stats) = t(p.get(4, next))
        assert_page(2, prev, rows, next, stats, e4pp_5t)
        (prev, rows, next, stats) = t(p.get(4, prev))
        assert_page(1, prev, rows, next, stats, e4pp_5t)
        return

    def test_prev_at_start_4pp(self):
        p = Pager(self.db.view, '%s/all' % model_type)
        (prev, rows, next, stats) = t(p.get(4, None))
        (prev, rows, next, stats) = t(p.get(4, next))
        (prev, rows, next, stats) = t(p.get(4, prev))
        (prev, rows, next, stats) = t(p.get(4, prev))
        assert_page(1, prev, rows, next, stats, e4pp_5t)
        return

    def test_next_at_end_4pp(self):
        p = Pager(self.db.view, '%s/all' % model_type)
        (prev, rows, next, stats) = t(p.get(4, None))
        (prev, rows, next, stats) = t(p.get(4, next))
        (prev, rows, next, stats) = t(p.get(4, next))
        assert_page(1, prev, rows, next, stats, e4pp_5t)
        return

    def test_roundtrip_6pp(self):
        p = Pager(self.db.view, '%s/all' % model_type)
        (prev, rows, next, stats) = t(p.get(6, None))
        assert_page(1, prev, rows, next, stats, e6pp_5t)
        (prev, rows, next, stats) = t(p.get(6, next))
        assert_page(1, prev, rows, next, stats, e6pp_5t)
        (prev, rows, next, stats) = t(p.get(6, prev))
        assert_page(1, prev, rows, next, stats, e6pp_5t)
        return

    def test_prev_at_start_6pp(self):
        p = Pager(self.db.view, '%s/all' % model_type)
        (prev, rows, next, stats) = t(p.get(6, None))
        assert_page(1, prev, rows, next, stats, e6pp_5t)
        (prev, rows, next, stats) = t(p.get(6, prev))
        assert_page(1, prev, rows, next, stats, e6pp_5t)
        return

    def test_next_at_end_6pp(self):
        p = Pager(self.db.view, '%s/all' % model_type)
        (prev, rows, next, stats) = t(p.get(6, None))
        assert_page(1, prev, rows, next, stats, e6pp_5t)
        (prev, rows, next, stats) = t(p.get(6, next))
        assert_page(1, prev, rows, next, stats, e6pp_5t)
        return


e5pp_1t = [
 [
  0]]

class TestCouchDBPager_1items(TestCase):

    def setUp(self):
        self.db = create_items(dbname, force_create=True, model_type=model_type, items=sequence_generator(1))
        map_fun = 'function(doc) { if (doc.model_type == "%s") { emit(doc.num, 1); } }' % model_type
        reduce_fun = 'function(keys, values) { return sum(values) }'
        create_view(self.db, model_type, 'all', map_fun)
        create_view(self.db, model_type, 'count', map_fun, reduce_fun)

    def test_roundtrip_5pp(self):
        p = Pager(self.db.view, '%s/all' % model_type)
        (prev, rows, next, stats) = t(p.get(5, None))
        assert_page(1, prev, rows, next, stats, e5pp_1t)
        return

    def test_next_at_end_5pp(self):
        p = Pager(self.db.view, '%s/all' % model_type)
        (prev, rows, next, stats) = t(p.get(5, None))
        (prev, rows, next, stats) = t(p.get(5, next))
        assert_page(1, prev, rows, next, stats, e5pp_1t)
        return

    def test_prev_at_start_5pp(self):
        p = Pager(self.db.view, '%s/all' % model_type)
        (prev, rows, next, stats) = t(p.get(5, None))
        (prev, rows, next, stats) = t(p.get(5, prev))
        assert_page(1, prev, rows, next, stats, e5pp_1t)
        return


e5pp_0t = [[]]

class TestCouchDBPager_0items(TestCase):

    def setUp(self):
        self.db = create_items(dbname, force_create=True, model_type=model_type, items=sequence_generator(0))
        map_fun = 'function(doc) { if (doc.model_type == "%s") { emit(doc.num, 1); } }' % model_type
        reduce_fun = 'function(keys, values) { return sum(values) }'
        create_view(self.db, model_type, 'all', map_fun)
        create_view(self.db, model_type, 'count', map_fun, reduce_fun)

    def test_roundtrip_5pp(self):
        p = Pager(self.db.view, '%s/all' % model_type)
        (prev, rows, next, stats) = t(p.get(5, None))
        assert_page(1, prev, rows, next, stats, e5pp_0t)
        return

    def test_next_at_end_5pp(self):
        p = Pager(self.db.view, '%s/all' % model_type)
        (prev, rows, next, stats) = t(p.get(5, None))
        (prev, rows, next, stats) = t(p.get(5, next))
        assert_page(1, prev, rows, next, stats, e5pp_0t)
        return

    def test_prev_at_start_5pp(self):
        p = Pager(self.db.view, '%s/all' % model_type)
        (prev, rows, next, stats) = t(p.get(5, None))
        (prev, rows, next, stats) = t(p.get(5, prev))
        assert_page(1, prev, rows, next, stats, e5pp_0t)
        return


class TestCouchDBPager_alterlist_10items(TestCase):

    def setUp(self):
        self.db = create_items(dbname, force_create=True, model_type=model_type, items=sequence_generator(10))
        map_fun = 'function(doc) { if (doc.model_type == "%s") { emit(doc.num, 1); } }' % model_type
        reduce_fun = 'function(keys, values) { return sum(values) }'
        create_view(self.db, model_type, 'all', map_fun)
        create_view(self.db, model_type, 'count', map_fun, reduce_fun)

    def test_remove_prevref(self):
        e5pp_10t_before = [
         [
          0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]
        e5pp_10t_after = [[0, 1, 2, 3], [5, 6, 7, 8, 9]]
        p = Pager(self.db.view, '%s/all' % model_type)
        (prev, rows, next, stats) = t(p.get(5, None))
        assert_page(1, prev, rows, next, stats, e5pp_10t_before)
        del self.db['id-4']
        (prev, rows, next, stats) = t(p.get(5, next))
        assert_page(2, prev, rows, next, stats, e5pp_10t_after)
        return

    def test_remove_prevref_reverse(self):
        e5pp_10t_before = [[9, 8, 7, 6, 5], [4, 3, 2, 1, 0]]
        e5pp_10t_after = [[9, 8, 7, 6], [4, 3, 2, 1, 0]]
        p = Pager(self.db.view, '%s/all' % model_type, dict(descending=True))
        (prev, rows, next, stats) = t(p.get(5, None))
        assert_page(1, prev, rows, next, stats, e5pp_10t_before)
        del self.db['id-5']
        (prev, rows, next, stats) = t(p.get(5, next))
        assert_page(2, prev, rows, next, stats, e5pp_10t_after)
        return

    def test_remove_whole_next_page(self):
        e5pp_10t_before = [[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]
        e5pp_10t_after = [[0, 1, 2, 3, 4], []]
        e5pp_10t_after_secondpass = [[0, 1, 2, 3, 4]]
        p = Pager(self.db.view, '%s/all' % model_type)
        (prev, rows, next, stats) = t(p.get(5, None))
        assert_page(1, prev, rows, next, stats, e5pp_10t_before)
        for i in xrange(5, 10):
            del self.db['id-%s' % i]

        (prev, rows, next, stats) = t(p.get(5, next))
        assert_page(2, prev, rows, next, stats, e5pp_10t_after)
        (prev, rows, next, stats) = t(p.get(5, prev))
        assert_page(1, prev, rows, next, stats, e5pp_10t_after_secondpass)
        return

    def test_remove_whole_next_page_reverse(self):
        e5pp_10t_before = [[9, 8, 7, 6, 5], [4, 3, 2, 1, 0]]
        e5pp_10t_after = [[9, 8, 7, 6, 5], []]
        e5pp_10t_after_secondpass = [[9, 8, 7, 6, 5]]
        p = Pager(self.db.view, '%s/all' % model_type, dict(descending=True))
        (prev, rows, next, stats) = t(p.get(5, None))
        assert_page(1, prev, rows, next, stats, e5pp_10t_before)
        for i in xrange(0, 5):
            del self.db['id-%s' % i]

        (prev, rows, next, stats) = t(p.get(5, next))
        assert_page(2, prev, rows, next, stats, e5pp_10t_after)
        (prev, rows, next, stats) = t(p.get(5, prev))
        assert_page(1, prev, rows, next, stats, e5pp_10t_after_secondpass)
        (prev, rows, next, stats) = t(p.get(5, next))
        assert_page(2, prev, rows, next, stats, e5pp_10t_after_secondpass)
        return

    def test_remove_alldata(self):
        e5pp_10t_before = [
         [
          0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]
        e5pp_10t_after = [[]]
        p = Pager(self.db.view, '%s/all' % model_type)
        (prev, rows, next, stats) = t(p.get(5, None))
        assert_page(1, prev, rows, next, stats, e5pp_10t_before)
        for i in xrange(0, 10):
            del self.db['id-%s' % i]

        (prev, rows, next, stats) = t(p.get(5, next))
        assert_page(2, prev, rows, next, stats, e5pp_10t_after)
        (prev, rows, next, stats) = t(p.get(5, prev))
        assert_page(1, prev, rows, next, stats, e5pp_10t_after)
        return

    def test_remove_alldata_reversed(self):
        e5pp_10t_before = [[9, 8, 7, 6, 5], [4, 3, 2, 1, 0]]
        e5pp_10t_after = [[]]
        p = Pager(self.db.view, '%s/all' % model_type, dict(descending=True))
        (prev, rows, next, stats) = t(p.get(5, None))
        assert_page(1, prev, rows, next, stats, e5pp_10t_before)
        for i in xrange(0, 10):
            del self.db['id-%s' % i]

        (prev, rows, next, stats) = t(p.get(5, next))
        assert_page(2, prev, rows, next, stats, e5pp_10t_after)
        return


class TestCouchDBPager_alterlist_15items(TestCase):

    def setUp(self):
        self.db = create_items(dbname, force_create=True, model_type=model_type, items=sequence_generator(15))
        map_fun = 'function(doc) { if (doc.model_type == "%s") { emit(doc.num, 1); } }' % model_type
        reduce_fun = 'function(keys, values) { return sum(values) }'
        create_view(self.db, model_type, 'all', map_fun)
        create_view(self.db, model_type, 'count', map_fun, reduce_fun)

    def test_remove_prevref(self):
        e5pp_15t_before = [
         [
          0, 1, 2, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14]]
        e5pp_15t_after = [[0, 1, 2, 3], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14]]
        p = Pager(self.db.view, '%s/all' % model_type)
        (prev, rows, next, stats) = t(p.get(5, None))
        assert_page(1, prev, rows, next, stats, e5pp_15t_before)
        del self.db['id-4']
        (prev, rows, next, stats) = t(p.get(5, next))
        assert_page(2, prev, rows, next, stats, e5pp_15t_after)
        return

    def test_remove_prevrefandfirst(self):
        e5pp_15t_before = [
         [
          0, 1, 2, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14]]
        e5pp_15t_after = [[0, 1, 2, 3], [6, 7, 8, 9, 10], [11, 12, 13, 14]]
        p = Pager(self.db.view, '%s/all' % model_type)
        (prev, rows, next, stats) = t(p.get(5, None))
        assert_page(1, prev, rows, next, stats, e5pp_15t_before)
        del self.db['id-4']
        del self.db['id-5']
        (prev, rows, next, stats) = t(p.get(5, next))
        assert_page(2, prev, rows, next, stats, e5pp_15t_after)
        return

    def test_remove_prevrefandfirst_thenprev(self):
        e5pp_15t_before = [[0, 1, 2, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14]]
        e5pp_15t_after = [[0, 1, 2, 3], [6, 7, 8, 9, 10], [11, 12, 13, 14]]
        p = Pager(self.db.view, '%s/all' % model_type)
        (prev, rows, next, stats) = t(p.get(5, None))
        assert_page(1, prev, rows, next, stats, e5pp_15t_before)
        del self.db['id-4']
        del self.db['id-5']
        (prev, rows, next, stats) = t(p.get(5, next))
        assert_page(2, prev, rows, next, stats, e5pp_15t_after)
        (prev, rows, next, stats) = t(p.get(5, prev))
        assert_page(1, prev, rows, next, stats, e5pp_15t_after)
        return


class TestCouchDBPager_10items_withstartend(TestCase):

    def setUp(self):
        self.db = create_items(dbname, force_create=True, model_type=model_type, items=sequence_generator(20))
        map_fun = 'function(doc) { if (doc.model_type == "%s") { emit(doc.num, 1); } }' % model_type
        reduce_fun = 'function(keys, values) { return sum(values) }'
        create_view(self.db, model_type, 'all', map_fun)
        create_view(self.db, model_type, 'count', map_fun, reduce_fun)

    def test_roundtrip_5pp(self):
        p = Pager(self.db.view, '%s/all' % model_type, dict(startkey=5, endkey=14))
        expecteds = [[5, 6, 7, 8, 9], [10, 11, 12, 13, 14]]
        (prev, rows, next, stats) = t(p.get(5, None))
        assert_page(1, prev, rows, next, stats, expecteds)
        (prev, rows, next, stats) = t(p.get(5, next))
        assert_page(2, prev, rows, next, stats, expecteds)
        (prev, rows, next, stats) = t(p.get(5, prev))
        assert_page(1, prev, rows, next, stats, expecteds)
        return

    def test_roundtrip_5pp_reversed(self):
        p = Pager(self.db.view, '%s/all' % model_type, dict(startkey=14, endkey=5, descending=True))
        expecteds = [[14, 13, 12, 11, 10], [9, 8, 7, 6, 5]]
        (prev, rows, next, stats) = t(p.get(5, None))
        assert_page(1, prev, rows, next, stats, expecteds)
        (prev, rows, next, stats) = t(p.get(5, next))
        assert_page(2, prev, rows, next, stats, expecteds)
        (prev, rows, next, stats) = t(p.get(5, prev))
        assert_page(1, prev, rows, next, stats, expecteds)
        return


class TestCouchDBPager_alterlist_15items_withstartend(TestCase):

    def setUp(self):
        self.db = create_items(dbname, force_create=True, model_type=model_type, items=sequence_generator(15))
        map_fun = 'function(doc) { if (doc.model_type == "%s") { emit(doc.num, 1); } }' % model_type
        reduce_fun = 'function(keys, values) { return sum(values) }'
        create_view(self.db, model_type, 'all', map_fun)
        create_view(self.db, model_type, 'count', map_fun, reduce_fun)

    def test_remove_prevref(self):
        e5pp_15t_before = [
         [
          2, 3, 4, 5, 6], [7, 8, 9, 10, 11], [12]]
        e5pp_15t_after = [[2, 3, 4, 5], [7, 8, 9, 10, 11], [12]]
        p = Pager(self.db.view, '%s/all' % model_type, dict(startkey=2, endkey=12))
        (prev, rows, next, stats) = t(p.get(5, None))
        assert_page(1, prev, rows, next, stats, e5pp_15t_before)
        del self.db['id-6']
        (prev, rows, next, stats) = t(p.get(5, next))
        assert_page(2, prev, rows, next, stats, e5pp_15t_after)
        (prev, rows, next, stats) = t(p.get(5, prev))
        assert_page(1, prev, rows, next, stats, e5pp_15t_after)
        (prev, rows, next, stats) = t(p.get(5, next))
        assert_page(2, prev, rows, next, stats, e5pp_15t_after)
        (prev, rows, next, stats) = t(p.get(5, next))
        assert_page(3, prev, rows, next, stats, e5pp_15t_after)
        return

    def test_remove_prevref_reversed(self):
        e5pp_15t_before = [
         [
          12, 11, 10, 9, 8], [7, 6, 5, 4, 3], [2]]
        e5pp_15t_after = [[12, 11, 10, 9], [7, 6, 5, 4, 3], [2]]
        p = Pager(self.db.view, '%s/all' % model_type, dict(startkey=12, endkey=2, descending=True))
        (prev, rows, next, stats) = t(p.get(5, None))
        assert_page(1, prev, rows, next, stats, e5pp_15t_before)
        del self.db['id-8']
        (prev, rows, next, stats) = t(p.get(5, next))
        assert_page(2, prev, rows, next, stats, e5pp_15t_after)
        (prev, rows, next, stats) = t(p.get(5, prev))
        assert_page(1, prev, rows, next, stats, e5pp_15t_after)
        (prev, rows, next, stats) = t(p.get(5, next))
        assert_page(2, prev, rows, next, stats, e5pp_15t_after)
        (prev, rows, next, stats) = t(p.get(5, next))
        assert_page(3, prev, rows, next, stats, e5pp_15t_after)
        return

    def test_remove_lots(self):
        e5pp_15t_before = [[2, 3, 4, 5, 6], [7, 8, 9, 10, 11], [12]]
        e5pp_15t_after = [[2, 3, 4, 5], []]
        e5pp_15t_after_secondpass = [[2, 3, 4, 5]]
        p = Pager(self.db.view, '%s/all' % model_type, dict(startkey=2, endkey=12))
        (prev, rows, next, stats) = t(p.get(5, None))
        assert_page(1, prev, rows, next, stats, e5pp_15t_before)
        for i in xrange(6, 13):
            del self.db['id-%s' % i]

        (prev, rows, next, stats) = t(p.get(5, next))
        assert_page(2, prev, rows, next, stats, e5pp_15t_after)
        (prev, rows, next, stats) = t(p.get(5, prev))
        assert_page(1, prev, rows, next, stats, e5pp_15t_after_secondpass)
        (prev, rows, next, stats) = t(p.get(5, next))
        assert_page(1, prev, rows, next, stats, e5pp_15t_after_secondpass)
        return

    def test_remove_lots_trigger_hack_and_revscan(self):
        e5pp_15t_before = [[2, 3, 4, 5, 6], [7, 8, 9, 10, 11], [12]]
        e5pp_15t_after = [[2, 3, 4, 5, 6], [7, 8, 9, 10], []]
        e5pp_15t_after_secondpass = [[2, 3, 4, 5]]
        e5pp_15t_after_lastpass = [[2, 3, 4, 5]]
        p = Pager(self.db.view, '%s/all' % model_type, dict(startkey=2, endkey=12))
        (prev, rows, next, stats) = t(p.get(5, None))
        assert_page(1, prev, rows, next, stats, e5pp_15t_before)
        (prev, rows, next, stats) = t(p.get(5, next))
        assert_page(2, prev, rows, next, stats, e5pp_15t_before)
        del self.db['id-11']
        del self.db['id-12']
        (prev, rows, next, stats) = t(p.get(5, next))
        assert_page(3, prev, rows, next, stats, e5pp_15t_after)
        del self.db['id-10']
        del self.db['id-9']
        del self.db['id-8']
        del self.db['id-7']
        del self.db['id-6']
        (prev, rows, next, stats) = t(p.get(5, prev))
        assert_page(2, prev, rows, next, stats, e5pp_15t_after_secondpass)
        (prev, rows, next, stats) = t(p.get(5, prev))
        assert_page(1, prev, rows, next, stats, e5pp_15t_after_secondpass)
        return

    def test_remove_lots_trigger_hack_and_revscan2(self):
        e5pp_15t_before = [[2, 3, 4, 5, 6], [7, 8, 9, 10, 11], [12]]
        e5pp_15t_after1 = [[2, 3, 4, 5, 6], [7, 8, 9, 10, 11], []]
        e5pp_15t_after2 = [[2, 3, 4, 5], [7, 8, 9, 10, 11]]
        e5pp_15t_after_secondpass = [[], [7, 8, 9, 10, 11]]
        p = Pager(self.db.view, '%s/all' % model_type, dict(startkey=2, endkey=12))
        (prev, rows, next, stats) = t(p.get(5, None))
        assert_page(1, prev, rows, next, stats, e5pp_15t_before)
        (prev, rows, next, stats) = t(p.get(5, next))
        assert_page(2, prev, rows, next, stats, e5pp_15t_before)
        del self.db['id-12']
        (prev, rows, next, stats) = t(p.get(5, next))
        assert_page(3, prev, rows, next, stats, e5pp_15t_after1)
        del self.db['id-6']
        (prev, rows, next, stats) = t(p.get(5, prev))
        assert_page(2, prev, rows, next, stats, e5pp_15t_after2)
        del self.db['id-5']
        del self.db['id-4']
        del self.db['id-3']
        del self.db['id-2']
        (prev, rows, next, stats) = t(p.get(5, prev))
        assert_page(1, prev, rows, next, stats, e5pp_15t_after_secondpass)
        return


class TestCouchDBPagerJumpRef(TestCase):

    def setUp(self):
        self.db_name = 'pagingish-%s' % uuid.uuid4().hex
        self.db = couchdb.Server().create(self.db_name)

    def tearDown(self):
        del couchdb.Server()[self.db_name]

    def test_jumpref(self):
        self.db['_design/test'] = {'views': {'test': {'map': 'function(doc) {emit(doc.letter+doc.letter, null);}'}}}
        self.db.update([ {'letter': letter} for letter in 'abcdefghijklmnopqrstuvwxyz' ])
        pager = Pager(self.db.view, 'test/test')
        p = pager.get(5)
        assert p['items'][0].key == 'aa'
        p = pager.get(5, Pager.jumpref('k'))
        assert p['items'][0].key == 'kk'
        p = pager.get(5, p['prev'])
        assert p['items'][0].key == 'ff'
        p = pager.get(5, p['prev'])
        assert p['items'][0].key == 'aa'
        assert p['prev'] is None
        return

    def test_jumpref_pageback(self):
        self.db['_design/test'] = {'views': {'test': {'map': 'function(doc) {emit(doc.letter, null);}'}}}
        self.db.update([ {'letter': 'a'} for i in range(100) ])
        self.db.update([ {'letter': 'b'} for i in range(100) ])
        pager = Pager(self.db.view, 'test/test')
        (prev, items, next, stats) = t(pager.get(5, Pager.jumpref('b')))
        assert items[0].key == 'b'

    def test_jumpref_start(self):
        self.db['_design/test'] = {'views': {'test': {'map': 'function(doc) {emit(doc.letter+doc.letter, null);}'}}}
        self.db.update([ {'letter': letter} for letter in 'abcdefghijklmnopqrstuvwxyz' ])
        pager = Pager(self.db.view, 'test/test')
        (prev, items, next, stats) = t(pager.get(5, Pager.jumpref('a')))
        assert items[0].key == 'aa'
        (prev, items, next, stats) = t(pager.get(5, Pager.jumpref('aa')))
        assert items[0].key == 'aa'

    def test_jumpref_exact(self):
        self.db['_design/test'] = {'views': {'test': {'map': 'function(doc) {emit(doc.letter, null);}'}}}
        self.db.update([ {'letter': letter} for letter in 'abcdefghijklmnopqrstuvwxyz' ])
        pager = Pager(self.db.view, 'test/test')
        (prev, items, next, stats) = t(pager.get(5))
        assert items[0].key == 'a'
        (prev, items, next, stats) = t(pager.get(5, Pager.jumpref('k')))
        assert items[0].key == 'k'
        (prev, items, next, stats) = t(pager.get(5, prev))
        assert items[0].key == 'f'
        (prev, items, next, stats) = t(pager.get(5, prev))
        assert items[0].key == 'a'
        assert prev is None
        return