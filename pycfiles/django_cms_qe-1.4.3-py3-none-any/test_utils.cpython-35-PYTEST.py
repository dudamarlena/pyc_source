# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tomas/git/euroix/django-cms-qe/cms_qe_table/tests/test_utils.py
# Compiled at: 2019-02-04 04:18:45
# Size of source mod 2**32: 2805 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q
import pytest
from ..exceptions import TableDoesNotExists
from ..utils import get_model_by_table, get_models_choices, get_table_choices, get_field_type, get_filter_params

def test_get_model_by_table():
    User = get_user_model()
    model = get_model_by_table('auth_user')
    @py_assert1 = model is User
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('is', ), (@py_assert1,), ('%(py0)s is %(py2)s', ), (model, User)) % {'py2': @pytest_ar._saferepr(User) if 'User' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(User) else 'User', 'py0': @pytest_ar._saferepr(model) if 'model' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(model) else 'model'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_get_model_by_table_not_found():
    with pytest.raises(TableDoesNotExists):
        get_model_by_table('table_does_not_exist')


def test_get_all_models():
    choices = get_models_choices()
    choices_admin_group = [item[1] for item in choices if item[0] == 'admin'][0]
    @py_assert2 = (('django_admin_log', 'LogEntry'), )
    @py_assert1 = choices_admin_group == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (choices_admin_group, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(choices_admin_group) if 'choices_admin_group' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(choices_admin_group) else 'choices_admin_group'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_get_table_choices():
    choices = get_table_choices('auth_user')
    @py_assert0 = 'columns'
    @py_assert2 = @py_assert0 in choices
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, choices)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(choices) if 'choices' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(choices) else 'choices'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = ('username', 'username', 'string')
    @py_assert3 = choices['columns']
    @py_assert2 = @py_assert0 in @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None


@pytest.mark.parametrize('field, expected_type', [
 (
  models.AutoField(), 'integer'),
 (
  models.BigAutoField(), 'integer'),
 (
  models.BigIntegerField(), 'integer'),
 (
  models.BooleanField(), 'boolean'),
 (
  models.CharField(), 'string'),
 (
  models.DateField(), 'string'),
 (
  models.DateTimeField(), 'string'),
 (
  models.DecimalField(), 'float'),
 (
  models.EmailField(), 'string'),
 (
  models.FloatField(), 'float'),
 (
  models.ForeignKey('LogEntry'), 'string'),
 (
  models.IntegerField(), 'integer'),
 (
  models.GenericIPAddressField(), 'string'),
 (
  models.NullBooleanField(), 'boolean'),
 (
  models.PositiveIntegerField(), 'integer'),
 (
  models.PositiveSmallIntegerField(), 'integer'),
 (
  models.SlugField(), 'string'),
 (
  models.SmallIntegerField(), 'integer'),
 (
  models.TextField(), 'string'),
 (
  models.TimeField(), 'string'),
 (
  models.URLField(), 'string'),
 (
  models.UUIDField(), 'string')])
def test_get_field_type(field, expected_type):
    @py_assert2 = get_field_type(field)
    @py_assert4 = @py_assert2 == expected_type
    if not @py_assert4:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, expected_type)) % {'py1': @pytest_ar._saferepr(field) if 'field' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(field) else 'field', 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(expected_type) if 'expected_type' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_type) else 'expected_type', 'py0': @pytest_ar._saferepr(get_field_type) if 'get_field_type' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get_field_type) else 'get_field_type'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert2 = @py_assert4 = None


def test_get_filter_params():

    class ForeignModel(models.Model):
        text1 = models.CharField()
        text2 = models.CharField()
        flag = models.BooleanField()
        number = models.IntegerField()

    class Model(models.Model):
        other = models.ForeignKey(ForeignModel)
        name = models.CharField()
        active = models.BooleanField()
        age = models.IntegerField()

    args, kwds = get_filter_params(Model, {'other': 'abc', 
     'name': 'name', 
     'active': True, 
     'age': 123, 
     'non-existent-field': 'blah'})
    @py_assert2 = str(args)
    @py_assert6 = [
     Q() | Q(other__text1__icontains='abc') | Q(other__text2__icontains='abc')]
    @py_assert8 = str(@py_assert6)
    @py_assert4 = @py_assert2 == @py_assert8
    if not @py_assert4:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py9)s\n{%(py9)s = %(py5)s(%(py7)s)\n}', ), (@py_assert2, @py_assert8)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py9': @pytest_ar._saferepr(@py_assert8), 'py1': @pytest_ar._saferepr(args) if 'args' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(args) else 'args', 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str', 'py0': @pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str'}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = None
    @py_assert2 = {'name__icontains': 'name', 'active': True, 'age': 123}
    @py_assert1 = kwds == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (kwds, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(kwds) if 'kwds' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(kwds) else 'kwds'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None