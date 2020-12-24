# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stas/workspace/partners/flask_restframework/flask_restframework/tests/test_filter_backends.py
# Compiled at: 2017-07-04 08:01:30
# Size of source mod 2**32: 1549 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, json, pytest
from mongoengine.queryset.queryset import QuerySet
from flask.ext.restframework.filter_backends import JsonFilterBackend, OrderingBackend
from flask.ext.restframework.queryset_wrapper import MongoDbQuerySet
import mongoengine as m
from flask.ext.restframework.tests.compat import mock

class Doc(m.Document):
    pass


@mock.patch.object(QuerySet, 'filter')
def test_json_filter_backend(m, db):
    qs = Doc.objects.all()
    m.return_value = qs
    jf = JsonFilterBackend(MongoDbQuerySet.from_queryset(qs), mock.Mock(args=dict(json_filters=json.dumps(dict(key='value')))), mock.Mock(spec=[]))
    jf.filter()
    @py_assert3 = mock.Mock
    @py_assert5 = isinstance(m, @py_assert3)
    if not @py_assert5:
        @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py0)s(%(py1)s, %(py4)s\n{%(py4)s = %(py2)s.Mock\n})\n}') % {'py2': @pytest_ar._saferepr(mock) if 'mock' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock) else 'mock', 'py6': @pytest_ar._saferepr(@py_assert5), 'py1': @pytest_ar._saferepr(m) if 'm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(m) else 'm', 'py0': @pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance', 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert3 = @py_assert5 = None
    m.assert_has_calls([
     mock.call(__raw__=dict(key='value'))])


@pytest.mark.test_json_filter_backend
@mock.patch.object(QuerySet, 'order_by')
def test_ordering_backend(m, db):
    qs = Doc.objects.all()
    m.return_value = qs
    ob = OrderingBackend(MongoDbQuerySet.from_queryset(qs), mock.Mock(args=dict(ordering='field,-other')), mock.Mock(spec=[]))
    ob.filter()
    m.assert_has_calls([
     mock.call('field', '-other')])
    ob = OrderingBackend(MongoDbQuerySet.from_queryset(qs), mock.Mock(args=dict()), mock.Mock(spec=['ordering'], ordering=('-field', )))
    ob.filter()
    m.assert_has_calls([
     mock.call('-field')])