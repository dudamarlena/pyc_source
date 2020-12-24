# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stas/workspace/partners/flask_restframework/flask_restframework/tests/test_flask_api.py
# Compiled at: 2017-06-30 11:16:28
# Size of source mod 2**32: 1261 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, datetime, json, mongoengine as m, pytest
from flask.app import Flask
from flask.ext.restframework.model_resource import ModelResource
from flask.ext.restframework.router import DefaultRouter
from flask.ext.restframework.serializer.model_serializer import ModelSerializer

class Model(m.Document):
    created = m.DateTimeField(default=datetime.datetime.now)
    value = m.StringField()


@pytest.mark.test_ignore_created_fields
def test_ignore_excluded_fields():

    class S(ModelSerializer):

        class Meta:
            model = Model
            excluded = ('created', )

    @py_assert2 = []
    @py_assert4 = S(@py_assert2)
    @py_assert6 = @py_assert4.get_fields
    @py_assert8 = @py_assert6()
    @py_assert10 = @py_assert8.keys
    @py_assert12 = @py_assert10()
    @py_assert14 = sorted(@py_assert12)
    @py_assert17 = [
     'id', 'value']
    @py_assert16 = @py_assert14 == @py_assert17
    if not @py_assert16:
        @py_format19 = @pytest_ar._call_reprcompare(('==',), (@py_assert16,), ('%(py15)s\n{%(py15)s = %(py0)s(%(py13)s\n{%(py13)s = %(py11)s\n{%(py11)s = %(py9)s\n{%(py9)s = %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py1)s(%(py3)s)\n}.get_fields\n}()\n}.keys\n}()\n})\n} == %(py18)s',), (@py_assert14, @py_assert17)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py13': @pytest_ar._saferepr(@py_assert12), 'py15': @pytest_ar._saferepr(@py_assert14), 'py0': @pytest_ar._saferepr(sorted) if 'sorted' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sorted) else 'sorted', 'py7': @pytest_ar._saferepr(@py_assert6), 'py11': @pytest_ar._saferepr(@py_assert10), 'py18': @pytest_ar._saferepr(@py_assert17), 'py1': @pytest_ar._saferepr(S) if 'S' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(S) else 'S', 'py5': @pytest_ar._saferepr(@py_assert4), 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format21 = ('' + 'assert %(py20)s') % {'py20': @py_format19}
        raise AssertionError(@pytest_ar._format_explanation(@py_format21))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert16 = @py_assert17 = None


def test_ignore_created_fields(app, db):

    class S(ModelSerializer):

        class Meta:
            model = Model
            excluded = ('created', )

    class R(ModelResource):
        serializer_class = S

        def get_queryset(self):
            return Model.objects.all()

    router = DefaultRouter(app)
    router.register('/test', R, 'test')
    @py_assert3 = isinstance(app, Flask)
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n}') % {'py2': @pytest_ar._saferepr(Flask) if 'Flask' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Flask) else 'Flask', 'py1': @pytest_ar._saferepr(app) if 'app' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(app) else 'app', 'py0': @pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance', 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert3 = None
    resp = app.test_client().post('/test', data=json.dumps({'value': '1'}), headers={'Content-Type': 'application/json'})
    @py_assert1 = resp.status_code
    @py_assert4 = 200
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status_code\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(resp) if 'resp' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(resp) else 'resp'}
        @py_format8 = (@pytest_ar._format_assertmsg(resp.data.decode('utf-8')) + '\n>assert %(py7)s') % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None