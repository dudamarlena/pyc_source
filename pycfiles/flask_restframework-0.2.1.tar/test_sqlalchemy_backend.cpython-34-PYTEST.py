# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stas/workspace/partners/flask_restframework/flask_restframework/tests/test_sqlalchemy_backend.py
# Compiled at: 2017-07-14 09:11:18
# Size of source mod 2**32: 2518 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, datetime, pytest
from flask.ext.sqlalchemy import SQLAlchemy
import sqlalchemy as sa
from flask_restframework.model_wrapper import SqlAlchemyModelWrapper
from flask_restframework.serializer.model_serializer import ModelSerializer
db = SQLAlchemy()

class SAModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uniq = db.Column(db.String(length=100), nullable=False, unique=True)
    dt = db.Column(db.DateTime(), default=datetime.datetime.now, nullable=False)
    date = db.Column(db.Date(), default=datetime.date.today, nullable=False)
    boolean = db.Column(db.Boolean(), nullable=False)
    un1 = db.Column(db.String(), nullable=False)
    un2 = db.Column(db.String(), nullable=False)
    __table_args__ = (
     db.UniqueConstraint('un1', 'un2'),)


@pytest.fixture()
def sdb(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
    db.init_app(app)
    SqlAlchemyModelWrapper.init(db)
    db.create_all()
    yield db
    db.drop_all()


@pytest.mark.test_model_serializer_creation
def test_model_serializer_creation(sdb):

    class Serializer(ModelSerializer):

        class Meta:
            model = SAModel

    s = Serializer({})
    @py_assert1 = s.validate
    @py_assert3 = @py_assert1()
    @py_assert6 = False
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.validate\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py2': @pytest_ar._saferepr(@py_assert1),  'py0': @pytest_ar._saferepr(s) if 's' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(s) else 's',  'py4': @pytest_ar._saferepr(@py_assert3),  'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    print(s.errors)
    @py_assert1 = s.errors
    @py_assert4 = {'date': ['Field is required'],  'un1': ['Field is required'],  'un2': ['Field is required'],  'boolean': ['Field is required'],  'dt': ['Field is required'],  'uniq': ['Field is required']}
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.errors\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1),  'py5': @pytest_ar._saferepr(@py_assert4),  'py0': @pytest_ar._saferepr(s) if 's' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(s) else 's'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    s = Serializer({'un1': '1', 
     'un2': '2', 
     'uniq': '123', 
     'boolean': 'Olala', 
     'date': 'asdasd', 
     'dt': 'asdasd'})
    @py_assert1 = s.validate
    @py_assert3 = @py_assert1()
    @py_assert6 = False
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.validate\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py2': @pytest_ar._saferepr(@py_assert1),  'py0': @pytest_ar._saferepr(s) if 's' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(s) else 's',  'py4': @pytest_ar._saferepr(@py_assert3),  'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = s.errors
    @py_assert4 = {'boolean': ['Boolean is required'],  'date': ['Incorrect DateTime string for %Y-%m-%d format'],  'dt': ['Incorrect DateTime string for %Y-%m-%d %H:%M:%S format']}
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.errors\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1),  'py5': @pytest_ar._saferepr(@py_assert4),  'py0': @pytest_ar._saferepr(s) if 's' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(s) else 's'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    s = Serializer({'un1': '1', 
     'un2': '2', 
     'uniq': '123', 
     'boolean': True, 
     'date': '2016-01-01', 
     'dt': '2016-01-01 00:00:00'})
    @py_assert1 = s.validate
    @py_assert3 = @py_assert1()
    @py_assert6 = True
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.validate\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py2': @pytest_ar._saferepr(@py_assert1),  'py0': @pytest_ar._saferepr(s) if 's' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(s) else 's',  'py4': @pytest_ar._saferepr(@py_assert3),  'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    instance = s.create(s.cleaned_data).item
    @py_assert3 = isinstance(instance, SAModel)
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n}') % {'py2': @pytest_ar._saferepr(SAModel) if 'SAModel' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SAModel) else 'SAModel',  'py1': @pytest_ar._saferepr(instance) if 'instance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(instance) else 'instance',  'py0': @pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert3 = None
    @py_assert1 = instance.un1
    @py_assert4 = '1'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.un1\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1),  'py5': @pytest_ar._saferepr(@py_assert4),  'py0': @pytest_ar._saferepr(instance) if 'instance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(instance) else 'instance'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = instance.un2
    @py_assert4 = '2'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.un2\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1),  'py5': @pytest_ar._saferepr(@py_assert4),  'py0': @pytest_ar._saferepr(instance) if 'instance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(instance) else 'instance'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = instance.uniq
    @py_assert4 = '123'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.uniq\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1),  'py5': @pytest_ar._saferepr(@py_assert4),  'py0': @pytest_ar._saferepr(instance) if 'instance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(instance) else 'instance'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = instance.boolean
    @py_assert4 = True
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.boolean\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1),  'py5': @pytest_ar._saferepr(@py_assert4),  'py0': @pytest_ar._saferepr(instance) if 'instance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(instance) else 'instance'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = instance.date
    @py_assert5 = datetime.date
    @py_assert7 = 2016
    @py_assert9 = 1
    @py_assert11 = 1
    @py_assert13 = @py_assert5(@py_assert7, @py_assert9, @py_assert11)
    @py_assert3 = @py_assert1 == @py_assert13
    if not @py_assert3:
        @py_format15 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.date\n} == %(py14)s\n{%(py14)s = %(py6)s\n{%(py6)s = %(py4)s.date\n}(%(py8)s, %(py10)s, %(py12)s)\n}', ), (@py_assert1, @py_assert13)) % {'py6': @pytest_ar._saferepr(@py_assert5),  'py8': @pytest_ar._saferepr(@py_assert7),  'py4': @pytest_ar._saferepr(datetime) if 'datetime' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(datetime) else 'datetime',  'py14': @pytest_ar._saferepr(@py_assert13),  'py12': @pytest_ar._saferepr(@py_assert11),  'py2': @pytest_ar._saferepr(@py_assert1),  'py0': @pytest_ar._saferepr(instance) if 'instance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(instance) else 'instance',  'py10': @pytest_ar._saferepr(@py_assert9)}
        @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = None
    @py_assert1 = instance.dt
    @py_assert5 = datetime.datetime
    @py_assert7 = 2016
    @py_assert9 = 1
    @py_assert11 = 1
    @py_assert13 = @py_assert5(@py_assert7, @py_assert9, @py_assert11)
    @py_assert3 = @py_assert1 == @py_assert13
    if not @py_assert3:
        @py_format15 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.dt\n} == %(py14)s\n{%(py14)s = %(py6)s\n{%(py6)s = %(py4)s.datetime\n}(%(py8)s, %(py10)s, %(py12)s)\n}', ), (@py_assert1, @py_assert13)) % {'py6': @pytest_ar._saferepr(@py_assert5),  'py8': @pytest_ar._saferepr(@py_assert7),  'py4': @pytest_ar._saferepr(datetime) if 'datetime' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(datetime) else 'datetime',  'py14': @pytest_ar._saferepr(@py_assert13),  'py12': @pytest_ar._saferepr(@py_assert11),  'py2': @pytest_ar._saferepr(@py_assert1),  'py0': @pytest_ar._saferepr(instance) if 'instance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(instance) else 'instance',  'py10': @pytest_ar._saferepr(@py_assert9)}
        @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = None
    @py_assert1 = instance.id
    @py_assert4 = 1
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.id\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1),  'py5': @pytest_ar._saferepr(@py_assert4),  'py0': @pytest_ar._saferepr(instance) if 'instance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(instance) else 'instance'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None