# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stas/workspace/partners/flask_restframework/flask_restframework/tests/test_model_serializers.py
# Compiled at: 2017-07-04 05:46:51
# Size of source mod 2**32: 3320 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest
from flask.app import Flask
from flask_mongoengine import MongoEngine
from mongoengine import fields as mfields
from pymongo.database import Database
from flask.ext.restframework.queryset_wrapper import QuerysetWrapper
from flask_restframework import fields
from flask_restframework.serializer.model_serializer import ModelSerializer

class Related(mfields.Document):
    value = mfields.StringField()


class Embedded(mfields.EmbeddedDocument):
    value1 = mfields.StringField()
    value2 = mfields.StringField()


class Main(mfields.Document):
    embedded_inner = mfields.EmbeddedDocumentField(Embedded)
    embedded_list_inner = mfields.EmbeddedDocumentListField(Embedded)
    related_inner = mfields.ReferenceField(Related)
    related_list_inner = mfields.ListField(mfields.ReferenceField(Related))


@pytest.fixture()
def main_record(db):
    rel1 = Related.objects.create(value='1')
    rel2 = Related.objects.create(value='2')
    return Main.objects.create(embedded_inner={'value1': '1', 
     'value2': '2'}, embedded_list_inner=[
     {'value1': '3', 
      'value2': '4'}], related_inner=rel1, related_list_inner=[
     rel1, rel2])


class E1(mfields.EmbeddedDocument):
    value = mfields.StringField()


class E2(mfields.EmbeddedDocument):
    e1 = mfields.EmbeddedDocumentField(E1)


class Doc(mfields.Document):
    e2 = mfields.EmbeddedDocumentField(E2)


@pytest.fixture()
def nested(db):
    return Doc.objects.create(e2=E2(e1=E1(value='test')))


@pytest.mark.test_not_full_fk_serialization
def test_not_full_fk_serialization(nested):

    class S(ModelSerializer):
        field = fields.ForeignKeyField('e2__e1')

        class Meta:
            model = Doc
            fields = ('field', )

    out = S(QuerysetWrapper.from_queryset(Doc.objects.all())).serialize()
    @py_assert2 = [{'field': {'value': 'test'}}]
    @py_assert1 = out == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (out, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(out) if 'out' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(out) else 'out'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


@pytest.mark.test_embedded_inner_serialization
def test_embedded_inner_serialization(main_record):

    class InnerSerializer(ModelSerializer):

        class Meta:
            model = Embedded
            fields = ('value1', )

    class Serializer(ModelSerializer):
        embedded_inner = fields.EmbeddedField(InnerSerializer)
        embedded_list_inner = fields.ListField(fields.EmbeddedField(InnerSerializer))

        class Meta:
            model = Main
            fields = ('embedded_inner', 'embedded_list_inner')

    data = Serializer(QuerysetWrapper.from_queryset(Main.objects.all())).serialize()
    @py_assert2 = len(data)
    @py_assert5 = 1
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py6': @pytest_ar._saferepr(@py_assert5), 'py1': @pytest_ar._saferepr(data) if 'data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(data) else 'data', 'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert0 = data[0]
    @py_assert4 = {'value1': '1'}
    @py_assert6 = [
     {'value1': '3'}]
    @py_assert8 = dict(embedded_inner=@py_assert4, embedded_list_inner=@py_assert6)
    @py_assert2 = @py_assert0 == @py_assert8
    if not @py_assert2:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py9)s\n{%(py9)s = %(py3)s(embedded_inner=%(py5)s, embedded_list_inner=%(py7)s)\n}', ), (@py_assert0, @py_assert8)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py7': @pytest_ar._saferepr(@py_assert6), 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4), 'py3': @pytest_ar._saferepr(dict) if 'dict' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dict) else 'dict'}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = None


@pytest.mark.test_reference_serialization
def test_reference_serialization(main_record):

    class Serializer(ModelSerializer):

        class Meta:
            model = Main

    d = Serializer.from_queryset(Main.objects.all()).serialize()
    @py_assert0 = d[0]['related_inner']
    @py_assert5 = main_record.related_inner
    @py_assert7 = @py_assert5.id
    @py_assert9 = str(@py_assert7)
    @py_assert2 = @py_assert0 == @py_assert9
    if not @py_assert2:
        @py_format11 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py10)s\n{%(py10)s = %(py3)s(%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s.related_inner\n}.id\n})\n}',), (@py_assert0, @py_assert9)) % {'py8': @pytest_ar._saferepr(@py_assert7), 'py4': @pytest_ar._saferepr(main_record) if 'main_record' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(main_record) else 'main_record', 'py10': @pytest_ar._saferepr(@py_assert9), 'py6': @pytest_ar._saferepr(@py_assert5), 'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str'}
        @py_format13 = ('' + 'assert %(py12)s') % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert0 = @py_assert2 = @py_assert5 = @py_assert7 = @py_assert9 = None
    @py_assert0 = d[0]['related_list_inner']
    @py_assert5 = lambda i: str(i.id)
    @py_assert8 = main_record.related_list_inner
    @py_assert10 = map(@py_assert5, @py_assert8)
    @py_assert12 = list(@py_assert10)
    @py_assert2 = @py_assert0 == @py_assert12
    if not @py_assert2:
        @py_format14 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py13)s\n{%(py13)s = %(py3)s(%(py11)s\n{%(py11)s = %(py4)s(%(py6)s, %(py9)s\n{%(py9)s = %(py7)s.related_list_inner\n})\n})\n}',), (@py_assert0, @py_assert12)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py13': @pytest_ar._saferepr(@py_assert12), 'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(map) if 'map' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(map) else 'map', 'py7': @pytest_ar._saferepr(main_record) if 'main_record' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(main_record) else 'main_record', 'py11': @pytest_ar._saferepr(@py_assert10), 'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list'}
        @py_format16 = ('' + 'assert %(py15)s') % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert0 = @py_assert2 = @py_assert5 = @py_assert8 = @py_assert10 = @py_assert12 = None