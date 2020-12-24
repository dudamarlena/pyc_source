# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/msthornton/Dropbox/Projects/springfield-mongo/tests/test_utils.py
# Compiled at: 2014-02-22 00:56:07
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from springfield_mongo import utils
from springfield_mongo.fields import ObjectIdField
from springfield import fields
from springfield import Entity, FlexEntity
from bson.objectid import ObjectId

class FooEntity(Entity):
    id = ObjectIdField()
    foo = fields.StringField()


class FlexFooEntity(FlexEntity):
    foo = fields.StringField()
    bar = fields.EntityField(FlexEntity)


def test_entity_to_mongo():
    i = ObjectId()
    m = FooEntity()
    m.id = i
    m.foo = 'monkey'
    mongo_document = utils.entity_to_mongo(m)
    @py_assert0 = '_id'
    @py_assert2 = @py_assert0 in mongo_document
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, mongo_document)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(mongo_document) if 'mongo_document' in @py_builtins.locals() is not @py_builtins.globals() else 'mongo_document'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = mongo_document['_id']
    @py_assert2 = @py_assert0 == i
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py3)s', ), (@py_assert0, i)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(i) if 'i' in @py_builtins.locals() is not @py_builtins.globals() else 'i'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'foo'
    @py_assert2 = @py_assert0 in mongo_document
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, mongo_document)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(mongo_document) if 'mongo_document' in @py_builtins.locals() is not @py_builtins.globals() else 'mongo_document'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = mongo_document['foo']
    @py_assert3 = 'monkey'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    return


def test_entity_from_mongo():
    i = ObjectId()
    m = FooEntity()
    m.id = i
    m.foo = 'gorilla'
    mongo_document = utils.entity_to_mongo(m)
    entity = utils.entity_from_mongo(FooEntity, mongo_document)
    @py_assert0 = '_id'
    @py_assert2 = @py_assert0 not in entity
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py3)s', ), (@py_assert0, entity)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(entity) if 'entity' in @py_builtins.locals() is not @py_builtins.globals() else 'entity'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'id'
    @py_assert2 = @py_assert0 in entity
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, entity)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(entity) if 'entity' in @py_builtins.locals() is not @py_builtins.globals() else 'entity'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = entity['id']
    @py_assert2 = @py_assert0 == i
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py3)s', ), (@py_assert0, i)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(i) if 'i' in @py_builtins.locals() is not @py_builtins.globals() else 'i'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'foo'
    @py_assert2 = @py_assert0 in entity
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, entity)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(entity) if 'entity' in @py_builtins.locals() is not @py_builtins.globals() else 'entity'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = entity['foo']
    @py_assert3 = 'gorilla'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    return


def test_to_and_from_equality():
    i = ObjectId()
    m = FooEntity()
    m.id = i
    m.foo = 'giraffe'
    mongo_document = utils.entity_to_mongo(m)
    entity = utils.entity_from_mongo(FooEntity, mongo_document)
    @py_assert1 = m == entity
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (m, entity)) % {'py0': @pytest_ar._saferepr(m) if 'm' in @py_builtins.locals() is not @py_builtins.globals() else 'm', 'py2': @pytest_ar._saferepr(entity) if 'entity' in @py_builtins.locals() is not @py_builtins.globals() else 'entity'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    mongo_document2 = utils.entity_to_mongo(entity)
    @py_assert1 = mongo_document2 == mongo_document
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (mongo_document2, mongo_document)) % {'py0': @pytest_ar._saferepr(mongo_document2) if 'mongo_document2' in @py_builtins.locals() is not @py_builtins.globals() else 'mongo_document2', 'py2': @pytest_ar._saferepr(mongo_document) if 'mongo_document' in @py_builtins.locals() is not @py_builtins.globals() else 'mongo_document'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    return


def test_flex_entity_field():
    f = FlexFooEntity()
    f.foo = 'spider'
    f.bar = dict(monkey='gorilla')
    mongo_document = utils.entity_to_mongo(f)
    @py_assert0 = 'foo'
    @py_assert2 = @py_assert0 in mongo_document
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, mongo_document)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(mongo_document) if 'mongo_document' in @py_builtins.locals() is not @py_builtins.globals() else 'mongo_document'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'bar'
    @py_assert2 = @py_assert0 in mongo_document
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, mongo_document)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(mongo_document) if 'mongo_document' in @py_builtins.locals() is not @py_builtins.globals() else 'mongo_document'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert1 = mongo_document['bar']
    @py_assert4 = isinstance(@py_assert1, dict)
    if not @py_assert4:
        @py_format6 = 'assert %(py5)s\n{%(py5)s = %(py0)s(%(py2)s, %(py3)s)\n}' % {'py0': @pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() is not @py_builtins.globals() else 'isinstance', 'py2': @pytest_ar._saferepr(@py_assert1), 'py3': @pytest_ar._saferepr(dict) if 'dict' in @py_builtins.locals() is not @py_builtins.globals() else 'dict', 'py5': @pytest_ar._saferepr(@py_assert4)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert4 = None
    entity = utils.entity_from_mongo(FlexFooEntity, mongo_document)
    @py_assert1 = entity.foo
    @py_assert4 = 'spider'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.foo\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(entity) if 'entity' in @py_builtins.locals() is not @py_builtins.globals() else 'entity', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert2 = entity.bar
    @py_assert4 = 'monkey'
    @py_assert6 = hasattr(@py_assert2, @py_assert4)
    if not @py_assert6:
        @py_format8 = 'assert %(py7)s\n{%(py7)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.bar\n}, %(py5)s)\n}' % {'py0': @pytest_ar._saferepr(hasattr) if 'hasattr' in @py_builtins.locals() is not @py_builtins.globals() else 'hasattr', 'py1': @pytest_ar._saferepr(entity) if 'entity' in @py_builtins.locals() is not @py_builtins.globals() else 'entity', 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert2 = @py_assert4 = @py_assert6 = None
    return