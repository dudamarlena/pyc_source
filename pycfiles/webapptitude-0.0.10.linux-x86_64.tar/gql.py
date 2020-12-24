# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/webapptitude/gql.py
# Compiled at: 2016-08-31 16:32:16
import webapp2
from handlers import adapt_request_params
GQL_OPERATOR_MAP = {'$gt': '>', 
   '$gte': '>=', 
   '$lt': '<', 
   '$lte': '<=', 
   '$ne': '!=', 
   '$eq': '=', 
   '$in': 'IN', 
   '$or': 'IN'}

def construct_gql_where_parts(params, attrib=None, **kwargs):
    """Produce a series of GQL constraints for WHERE clause."""
    bindings = kwargs.pop('bindings', [])
    statements = kwargs.pop('statements', [])
    if isinstance(params, dict) and attrib is not None:
        for k, v in params.iteritems():
            if str(k) in ('OR', '$or', '$in'):
                bindings.append(v)
                statements.append('%s IN (:%d)' % (attrib, len(bindings)))
            if str(k) in GQL_OPERATOR_MAP:
                operator = GQL_OPERATOR_MAP[k]
                bindings.append(v)
                index = len(bindings)
                statements.append('%s %s :%d' % (attrib, operator, index))

    elif isinstance(params, dict):
        for k, v in params.iteritems():
            if isinstance(v, basestring):
                v = str(v)
            if isinstance(v, dict):
                construct_gql_where_parts(v, attrib=str(k), statements=statements, bindings=bindings)
            else:
                bindings.append(v)
                statements.append('%s = :%d' % (str(k), len(bindings)))

    return (
     bindings, statements)


def construct_gql_where(params):
    bindings, statements = construct_gql_where_parts(params)
    return (bindings, (' AND ').join(statements))


def query(request, model):
    assert isinstance(request, webapp2.Request)
    query = dict(adapt_request_params(request))
    bindings, where = construct_gql_where(query)
    if len(bindings):
        return model.gql(('WHERE %s' % where), *bindings)
    else:
        return model.query()