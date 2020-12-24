# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stas/workspace/partners/flask_restframework/flask_restframework/tests/test_mixins.py
# Compiled at: 2017-07-14 09:11:18
# Size of source mod 2**32: 858 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest
from flask_restframework.model_resource import ModelResource
from flask_restframework.serializer.model_serializer import ModelSerializer
import mongoengine as m
from flask_restframework.tests.compat import mock

class SimpleModel(m.Document):
    value = m.StringField()


@pytest.fixture()
def simple_model(db):
    return SimpleModel.objects.create(value='1')


@pytest.mark.test_delete_mixin
def test_delete_mixin(simple_model):

    class S(ModelSerializer):

        class Meta:
            model = SimpleModel

    class R(ModelResource):
        serializer_class = S

        def get_queryset(self):
            return SimpleModel.objects.all()

    request = mock.Mock()
    resp = R(request).delete_object(request, simple_model.id)
    @py_assert1 = resp.status_code
    @py_assert4 = 200
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status_code\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1),  'py5': @pytest_ar._saferepr(@py_assert4),  'py0': @pytest_ar._saferepr(resp) if 'resp' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(resp) else 'resp'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = resp.json
    @py_assert4 = {'id': str(simple_model.id)}
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.json\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1),  'py5': @pytest_ar._saferepr(@py_assert4),  'py0': @pytest_ar._saferepr(resp) if 'resp' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(resp) else 'resp'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None