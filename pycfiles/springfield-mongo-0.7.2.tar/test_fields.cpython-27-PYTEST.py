# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/msthornton/Dropbox/Projects/springfield-mongo/tests/test_fields.py
# Compiled at: 2012-07-06 04:15:51
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from springfield_mongo import fields
from springfield import Entity
import pytest
from bson.objectid import ObjectId
from bson.objectid import InvalidId

def test_objectid():

    class MongoEntity(Entity):
        _id = fields.ObjectIdField()

    e = MongoEntity()
    @py_assert1 = e._id
    @py_assert3 = @py_assert1 is None
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('is',), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s._id\n} is %(py4)s',), (@py_assert1, None)) % {'py0': @pytest_ar._saferepr(e) if 'e' in @py_builtins.locals() is not @py_builtins.globals() else 'e', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(None) if 'None' in @py_builtins.locals() is not @py_builtins.globals() else 'None'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    with pytest.raises(InvalidId):
        e._id = '1234'
    object_id = ObjectId()
    e._id = object_id
    @py_assert0 = e.jsonify()['_id']
    @py_assert5 = str(object_id)
    @py_assert2 = @py_assert0 == @py_assert5
    if not @py_assert2:
        @py_format7 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py6)s\n{%(py6)s = %(py3)s(%(py4)s)\n}',), (@py_assert0, @py_assert5)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() is not @py_builtins.globals() else 'str', 'py4': @pytest_ar._saferepr(object_id) if 'object_id' in @py_builtins.locals() is not @py_builtins.globals() else 'object_id', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert5 = None
    e._id = '4ff69dacc3e3f882f3000000'
    @py_assert1 = e._id
    @py_assert5 = '4ff69dacc3e3f882f3000000'
    @py_assert7 = ObjectId(@py_assert5)
    @py_assert3 = @py_assert1 == @py_assert7
    if not @py_assert3:
        @py_format9 = @pytest_ar._call_reprcompare(('==',), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s._id\n} == %(py8)s\n{%(py8)s = %(py4)s(%(py6)s)\n}',), (@py_assert1, @py_assert7)) % {'py0': @pytest_ar._saferepr(e) if 'e' in @py_builtins.locals() is not @py_builtins.globals() else 'e', 'py8': @pytest_ar._saferepr(@py_assert7), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(ObjectId) if 'ObjectId' in @py_builtins.locals() is not @py_builtins.globals() else 'ObjectId', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    @py_assert2 = e.jsonify
    @py_assert4 = @py_assert2()
    @py_assert6 = MongoEntity(**@py_assert4)
    @py_assert8 = @py_assert6._id
    @py_assert12 = '4ff69dacc3e3f882f3000000'
    @py_assert14 = ObjectId(@py_assert12)
    @py_assert10 = @py_assert8 == @py_assert14
    if not @py_assert10:
        @py_format16 = @pytest_ar._call_reprcompare(('==',), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py7)s\n{%(py7)s = %(py0)s(**%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.jsonify\n}()\n})\n}._id\n} == %(py15)s\n{%(py15)s = %(py11)s(%(py13)s)\n}',), (@py_assert8, @py_assert14)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py11': @pytest_ar._saferepr(ObjectId) if 'ObjectId' in @py_builtins.locals() is not @py_builtins.globals() else 'ObjectId', 'py0': @pytest_ar._saferepr(MongoEntity) if 'MongoEntity' in @py_builtins.locals() is not @py_builtins.globals() else 'MongoEntity', 'py1': @pytest_ar._saferepr(e) if 'e' in @py_builtins.locals() is not @py_builtins.globals() else 'e', 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6), 'py13': @pytest_ar._saferepr(@py_assert12), 'py15': @pytest_ar._saferepr(@py_assert14)}
        @py_format18 = 'assert %(py17)s' % {'py17': @py_format16}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = None
    return