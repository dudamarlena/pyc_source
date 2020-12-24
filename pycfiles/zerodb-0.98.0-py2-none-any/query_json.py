# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /zerodb/catalog/query_json.py
# Compiled at: 2016-03-08 18:12:41
from six import iterkeys
from .query import Eq, Lt, Gt, And, Or, Not, InRange, Contains, NotEq, Le, Ge, NotInRange, DoesNotContain, Any, All, NotAny, NotAll
logical_operators = {'$and': And, 
   '$or': Or, 
   '$not': Not}
field_operators = {'$eq': Eq, 
   '$ne': NotEq, 
   '$lt': Lt, 
   '$lte': Le, 
   '$gt': Gt, 
   '$gte': Ge, 
   '$range': InRange, 
   '$nrange': NotInRange, 
   '$text': Contains, 
   '$ntext': DoesNotContain, 
   '$in': Any, 
   '$all': All, 
   '$nany': NotAny, 
   '$nin': NotAll}

def compile(q):
    """
    :param dict q: deserialized json
    :returns: query object
    :rtype: zerodb.catalog.query.Query
    """
    assert len(q) == 1
    key = next(iterkeys(q))
    if key in logical_operators:
        if isinstance(q[key], list):
            return logical_operators[key](*map(compile, q[key]))
        else:
            return logical_operators[key](compile(q[key]))

    else:
        if not isinstance(q[key], dict):
            raise AssertionError
            assert len(q[key]) == 1
            opkey = next(iterkeys(q[key]))
            params = q[key][opkey]
            params = isinstance(params, list) or [
             params]
        return field_operators[opkey](key, *params)