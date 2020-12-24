# uncompyle6 version 3.6.7
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/maxk/Projects/OpenSource/arango-python/arango/tests/tests_mixins.py
# Compiled at: 2013-03-08 14:06:20
# Size of source mod 2**32: 2585 bytes
import copy
from nose.tools import assert_equal, assert_false, assert_true, raises
from mock import Mock
from .tests_base import TestsBase
from arango.mixins import ComparsionMixin, LazyLoadMixin

class DummyDataType(ComparsionMixin, LazyLoadMixin):
    IGNORE_KEYS = [
     'id', 'rev', 'test']
    LAZY_LOAD_HANDLERS = ['id', 'rev', 'body']

    def __init__(self, id=None, rev=None, body=None, **kwargs):
        self.body = body
        self._id = id
        self._rev = rev
        self.__dict__.update(kwargs)
        self._lazy_loaded = True

    @property
    def id(self):
        return self._id

    @property
    def rev(self):
        return self._rev


class TestComparsion(TestsBase):

    def setUp(self):
        super(TestComparsion, self).setUp()
        self.data = DummyDataType(id=1, rev=2, body={'name': 1}, test=None)
        return

    def test_other_none(self):
        assert_equal(self.data.__eq__(None), False)
        assert_false(self.data is None)
        return

    def test_compare_plain(self):
        data2 = DummyDataType(id=None, rev=2, body={'name': 1}, test=None)
        assert_equal(self.data.__eq__(data2), False)
        return

    def test_ignore_keys(self):
        data = DummyDataType(id=1, rev=2, body={'name': 1}, test=None)
        assert_equal(self.data, data)
        data.__dict__.update(dict(test=1))
        assert_equal(self.data, data)
        return

    def test_compare_body(self):
        data = copy.deepcopy(self.data)
        data.body.update({'name': 2})
        assert_equal(data.__eq__(self.data), False)
        assert_false(data == self.data)


class TestLazyLoad(TestsBase):

    def setUp(self):
        super(TestLazyLoad, self).setUp()
        self.data = DummyDataType(id=1, rev=2, body={'name': 1}, test=None)
        self.data.lazy_loader = Mock()
        self.data._lazy_loaded = False
        return

    def test_lazy_attr(self):
        assert_false(self.data.lazy_loader.called)
        self.data.id
        assert_true(self.data.lazy_loader.called)

    @raises(AttributeError)
    def test_missing_attr(self):
        self.data.check

    def test_nonlazy_attr(self):
        assert_false(self.data.lazy_loader.called)
        self.data.test
        assert_false(self.data.lazy_loader.called)