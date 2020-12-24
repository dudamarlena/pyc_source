# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ubuntu/anaconda/lib/python2.7/site-packages/sql_query_dict.py
# Compiled at: 2016-01-14 15:31:36
import six, re, types, sys
if sys.version_info > (3, ):
    long = int

def quote_string(string):
    return repr(str(string))


def mysql_list(l):
    return (',').join(map(str, l))


def _escape(x):
    if isinstance(x, six.string_types):
        return quote_string(x)
    else:
        return str(x)


def mysql_list_esc(l):
    return (',').join(map(_escape, l))


def _is_iterable(i):
    try:
        iter(i)
        return True
    except TypeError:
        return False


def is_number(x):
    try:
        float(x)
        return True
    except TypeError:
        return False


def _mysql_is_list(val):
    return _is_iterable(val) and not isinstance(val, six.string_types)


def _mysql_isval(val):
    """ These types should either be ignored or have already been
    inserted into the SQL directly and dont need sqlalchemy to do
    it for us. """
    if _mysql_is_list(val):
        return False
    else:
        if isinstance(val, mysql_col):
            return False
        if val in [None, mysql_now, mysql_ignore]:
            return False
        return True


class mysql_now:
    pass


class mysql_col(str):
    pass


class mysql_ignore(str):
    pass


def _mysql_simple_clause_list(key, compare, val):
    esc = mysql_list_esc(val)
    if esc == 'None':
        return ' (1) '
    if esc == '':
        return ' (0) '
    if compare == '!=':
        compare = 'NOT IN'
    else:
        compare = 'IN'
    return (' ({0} {1} ({2})) ').format(key, compare, esc)


def _mysql_clause_list(key, compare, val):
    if isinstance(val, types.GeneratorType):
        val = list(val)
    if None in val:
        val = filter(lambda x: x is not None, val)
        clause = _mysql_simple_clause_list(key, compare, val)
        if compare == '!=':
            compare = 'IS NOT'
            logic = 'AND'
        else:
            compare = 'IS'
            logic = 'OR'
        return (' (({key} {compare} NULL) {logic} {clause}) ').format(key=key, compare=compare, logic=logic, clause=clause)
    else:
        return _mysql_simple_clause_list(key, compare, val)
        return


def _mysql_simple_clause(key, compare, val, param_style):
    if compare == '><':
        return (' (({0} > {1}) AND ({0} < {1})) ').format(key, param_style)
    if compare == '~':
        compare = 'LIKE'
    elif compare == '!~':
        compare = 'NOT LIKE'
    if val == mysql_now:
        val = 'NOW()'
    elif isinstance(val, mysql_col):
        val = val
    else:
        val = param_style
    return (' ({0} {1} {2}) ').format(key, compare, val)


def _split_key_compare(key):
    key, compare = re.match('([^<>=~!|]*)([<>=~!|]*)', key).groups()
    if compare == '':
        compare = '='
    return (
     key, compare)


def _mysql_clause(key, val, param_style):
    key, compare = _split_key_compare(key)
    if _mysql_is_list(val) and compare != '><':
        return _mysql_clause_list(key, compare, val)
    else:
        if val is None:
            if compare == '!=':
                return (' ({0} IS NOT NULL) ').format(key)
            else:
                return (' ({0} IS NULL) ').format(key)

        else:
            return _mysql_simple_clause(key, compare, val, param_style)
        return


def _flatten_between(keys, vals):
    new_vals = []
    for key, val in zip(keys, vals):
        if key[-2:] == '><':
            new_vals.extend(val)
        else:
            new_vals.append(val)

    return new_vals


def _mysql_other_fields(extra=None, order_by=None, limit=None, offset=None):
    ret = ''
    if order_by is not None:
        ret += ' ORDER BY %s ' % order_by
    if limit is not None:
        ret += ' LIMIT %d ' % limit
    if offset is not None:
        ret += ' OFFSET %d ' % offset
    if extra is not None:
        ret += ' ' + extra
    return ret


def _parse_tablename(tablename):
    if isinstance(tablename, six.string_types):
        return tablename
    if _is_iterable(tablename):
        return (',').join(map(str, tablename))
    raise TypeError('tablename expecting string or iterable')


def select(tablename, cols, o=None, j=None, extra=None, order_by=None, limit=None, offset=None, param_style='%s'):
    o = o or {}
    j = j or {}
    if not _is_iterable(o) or isinstance(o, six.string_types):
        o = {'id': long(o)}
    tablename = _parse_tablename(tablename)
    keys = o.keys()
    vals = [ o[key] for key in keys ]
    SQL = ('SELECT {0} FROM {1} WHERE ').format(mysql_list(cols), tablename)
    SQL += (' AND ').join(_mysql_clause(key, val, param_style) for key, val in zip(keys, vals) if val is not mysql_ignore) or '1'
    if j:
        SQL += ('').join((' AND ({0} = {1}) ').format(k, v) for k, v in j.iteritems())
    vals = _flatten_between(keys, vals)
    vals = list(filter(_mysql_isval, vals))
    SQL += _mysql_other_fields(extra=extra, order_by=order_by, limit=limit, offset=offset)
    return (
     SQL, vals)


def update(tablename, where, properties, param_style='%s'):
    set_keys = properties.keys()
    set_vals = [ properties[key] for key in set_keys if properties[key] != mysql_now
               ]
    properties = (', ').join((' {0} = {1} ').format(key, val == mysql_now and 'NOW()' or '%s') for key, val in zip(set_keys, set_vals))
    if is_number(where) or isinstance(where, (list, tuple)):
        where = {'id': where}
    elif not isinstance(where, dict):
        raise ValueError('where should be a number, list, tuple or dict')
    where_items = where.items()
    where_sql = (' AND ').join(_mysql_clause(k, v, param_style) for k, v in where_items if v is not mysql_ignore)
    where_vals = [ v for k, v in where_items if _mysql_isval(v) ]
    vals = set_vals + where_vals
    SQL = ('UPDATE {tablename} SET {properties} WHERE {where_sql}').format(**locals())
    return (
     SQL, vals)


def delete(tablename, properties, param_style='%s'):
    if isinstance(properties, list):
        properties = {'id': properties}
    elif isinstance(properties, six.string_types):
        properties = {'id': long(properties)}
    elif not _is_iterable(properties):
        properties = {'id': long(properties)}
    keys = properties.keys()
    vals = [ properties[key] for key in keys if properties[key] != mysql_now
           ]
    where = (' AND ').join(_mysql_clause(key, val, param_style) for key, val in zip(keys, vals) if val is not mysql_ignore)
    SQL = ('DELETE FROM {tablename} WHERE {where}').format(**locals())
    vals = [ val for val in vals if not _mysql_is_list(val) ]
    return (
     SQL, vals)


def insert(tablename, o, replace_into=False):
    keys = o.keys()
    vals = [ o[key] for key in keys ]
    SQL = '%s INTO %s (%s) VALUES (%s)' % (
     'REPLACE' if replace_into else 'INSERT',
     tablename,
     (', ').join(keys),
     (', ').join(val == mysql_now and 'NOW()' or '%s' for val in vals))
    vals = filter(lambda val: val != mysql_now, vals)
    return (
     SQL, vals)