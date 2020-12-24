# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stas/workspace/partners/flask_restframework/flask_restframework/tests/test_custom_querysets.py
# Compiled at: 2017-07-14 09:11:18
# Size of source mod 2**32: 3474 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, json
from flask_restframework.queryset_wrapper import QuerysetWrapper
from flask_restframework.tests.compat import mock
import mongoengine as m, pytest
from flask_restframework.model_cursor_resource import GenericCursorResource
from flask_restframework.model_resource import ModelResource
from flask_restframework.serializer.base_serializer import BaseSerializer
from flask_restframework import fields
from flask_restframework.serializer.model_serializer import ModelSerializer

class Inner(m.EmbeddedDocument):
    value = m.StringField()


class Ref(m.Document):
    value = m.StringField()


class Doc(m.Document):
    ref = m.ReferenceField(Ref)
    ref_list = m.ListField(m.ReferenceField(Ref))
    inner = m.EmbeddedDocumentField(Inner)
    inner_list = m.EmbeddedDocumentListField(Inner)
    value = m.StringField()


@pytest.fixture
def complex_doc(db):
    return Doc.objects.create(ref=Ref.objects.create(value='1'), ref_list=[
     Ref.objects.create(value='1'),
     Ref.objects.create(value='2')], inner=Inner(value='3'), inner_list=[
     Inner(value='4'),
     Inner(value='5')])


class Serializer(ModelSerializer):

    class Meta:
        model = Doc


class Resource(ModelResource):
    serializer_class = Serializer

    def get_queryset(self):
        return Doc._get_collection().find()


@pytest.mark.test_fetch_data_with_cursor
def test_fetch_data_with_cursor(app, complex_doc):
    request = mock.Mock()
    with app.test_request_context():
        resp = Resource(request).get(request)
    @py_assert0 = resp.json[0]['inner_list']
    @py_assert3 = [{'value': '4'}, {'value': '5'}]
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0),  'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert1 = resp.json[0]['ref_list']
    @py_assert3 = len(@py_assert1)
    @py_assert6 = 2
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py2': @pytest_ar._saferepr(@py_assert1),  'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py4': @pytest_ar._saferepr(@py_assert3),  'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert0 = resp.json[0]['inner']
    @py_assert3 = {'value': '3'}
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0),  'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None


@pytest.mark.test_join_data
def test_join_data(app, complex_doc):

    class Nested(BaseSerializer):
        value = fields.StringField()

    class S(ModelSerializer):
        ref = fields.ReferenceField(Nested, queryset=Ref.objects.all)
        nested_list = fields.ListField(fields.ReferenceField(Nested, queryset=Ref.objects.all))

        class Meta:
            model = Doc
            fields = ('id', )

    data = S(QuerysetWrapper.from_queryset(Doc.objects.no_dereference())).serialize()
    @py_assert0 = data[0]['ref']
    @py_assert3 = {'value': '1'}
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py4)s',), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0),  'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = ('' + 'assert %(py6)s') % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert4 = QuerysetWrapper.from_queryset
    @py_assert7 = Doc._get_collection
    @py_assert9 = @py_assert7()
    @py_assert11 = @py_assert9.find
    @py_assert13 = @py_assert11()
    @py_assert15 = @py_assert4(@py_assert13)
    @py_assert17 = S(@py_assert15)
    @py_assert19 = @py_assert17.serialize
    @py_assert21 = @py_assert19()
    @py_assert1 = data == @py_assert21
    if not @py_assert1:
        @py_format23 = @pytest_ar._call_reprcompare(('==',), (@py_assert1,), ('%(py0)s == %(py22)s\n{%(py22)s = %(py20)s\n{%(py20)s = %(py18)s\n{%(py18)s = %(py2)s(%(py16)s\n{%(py16)s = %(py5)s\n{%(py5)s = %(py3)s.from_queryset\n}(%(py14)s\n{%(py14)s = %(py12)s\n{%(py12)s = %(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = %(py6)s._get_collection\n}()\n}.find\n}()\n})\n})\n}.serialize\n}()\n}',), (data, @py_assert21)) % {'py8': @pytest_ar._saferepr(@py_assert7),  'py12': @pytest_ar._saferepr(@py_assert11),  'py5': @pytest_ar._saferepr(@py_assert4),  'py14': @pytest_ar._saferepr(@py_assert13),  'py20': @pytest_ar._saferepr(@py_assert19),  'py2': @pytest_ar._saferepr(S) if 'S' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(S) else 'S',  'py16': @pytest_ar._saferepr(@py_assert15),  'py3': @pytest_ar._saferepr(QuerysetWrapper) if 'QuerysetWrapper' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(QuerysetWrapper) else 'QuerysetWrapper',  'py18': @pytest_ar._saferepr(@py_assert17),  'py6': @pytest_ar._saferepr(Doc) if 'Doc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Doc) else 'Doc',  'py0': @pytest_ar._saferepr(data) if 'data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(data) else 'data',  'py10': @pytest_ar._saferepr(@py_assert9),  'py22': @pytest_ar._saferepr(@py_assert21)}
        @py_format25 = ('' + 'assert %(py24)s') % {'py24': @py_format23}
        raise AssertionError(@pytest_ar._format_explanation(@py_format25))
    @py_assert1 = @py_assert4 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = @py_assert17 = @py_assert19 = @py_assert21 = None

    class S(ModelSerializer):
        ref = fields.ReferenceField(Nested, queryset=lambda : Ref._get_collection().find())
        nested_list = fields.ListField(fields.ReferenceField(Nested, queryset=Ref.objects.all))

        class Meta:
            model = Doc
            fields = ('id', )

    data = S(QuerysetWrapper.from_queryset(Doc.objects.no_dereference())).serialize()
    @py_assert0 = data[0]['ref']
    @py_assert3 = {'value': '1'}
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py4)s',), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0),  'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = ('' + 'assert %(py6)s') % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None


@pytest.mark.test_serialize_embedded
def test_serialize_embedded(app, complex_doc):

    class S(ModelSerializer):
        field = fields.ForeignKeyField('inner__value')

        class Meta:
            model = Doc
            fields = ('field', )

    @py_assert2 = QuerysetWrapper.from_queryset
    @py_assert5 = Doc._get_collection
    @py_assert7 = @py_assert5()
    @py_assert9 = @py_assert7.find
    @py_assert11 = @py_assert9()
    @py_assert13 = @py_assert2(@py_assert11)
    @py_assert15 = S(@py_assert13)
    @py_assert17 = @py_assert15.serialize
    @py_assert19 = @py_assert17()
    @py_assert22 = [{'field': '3'}]
    @py_assert21 = @py_assert19 == @py_assert22
    if not @py_assert21:
        @py_format24 = @pytest_ar._call_reprcompare(('==',), (@py_assert21,), ('%(py20)s\n{%(py20)s = %(py18)s\n{%(py18)s = %(py16)s\n{%(py16)s = %(py0)s(%(py14)s\n{%(py14)s = %(py3)s\n{%(py3)s = %(py1)s.from_queryset\n}(%(py12)s\n{%(py12)s = %(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s._get_collection\n}()\n}.find\n}()\n})\n})\n}.serialize\n}()\n} == %(py23)s',), (@py_assert19, @py_assert22)) % {'py8': @pytest_ar._saferepr(@py_assert7),  'py4': @pytest_ar._saferepr(Doc) if 'Doc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Doc) else 'Doc',  'py12': @pytest_ar._saferepr(@py_assert11),  'py14': @pytest_ar._saferepr(@py_assert13),  'py20': @pytest_ar._saferepr(@py_assert19),  'py1': @pytest_ar._saferepr(QuerysetWrapper) if 'QuerysetWrapper' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(QuerysetWrapper) else 'QuerysetWrapper',  'py16': @pytest_ar._saferepr(@py_assert15),  'py23': @pytest_ar._saferepr(@py_assert22),  'py3': @pytest_ar._saferepr(@py_assert2),  'py18': @pytest_ar._saferepr(@py_assert17),  'py6': @pytest_ar._saferepr(@py_assert5),  'py0': @pytest_ar._saferepr(S) if 'S' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(S) else 'S',  'py10': @pytest_ar._saferepr(@py_assert9)}
        @py_format26 = ('' + 'assert %(py25)s') % {'py25': @py_format24}
        raise AssertionError(@pytest_ar._format_explanation(@py_format26))
    @py_assert2 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = @py_assert17 = @py_assert19 = @py_assert21 = @py_assert22 = None