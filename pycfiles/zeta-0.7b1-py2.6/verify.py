# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/zeta/model/verify.py
# Compiled at: 2010-01-24 10:23:30
"""Verify the Tables, columns, primary keys, foreign keys, unique attribute,
index"""
from sqlalchemy import MetaData, Table, Column, ForeignKey, ForeignKeyConstraint, PrimaryKeyConstraint, Index
from zeta.model import meta, schema
from zeta.model.utils import get_permnames, get_permgroups, get_users, get_userinfos
__all__ = [
 'get_sqltables', 'get_dbtables', 'table_comparator',
 'column_comparator', 'verify_tables']
_metadata = MetaData()
column_attrs = lambda c: (
 c.name, c.type, c.primary_key, c.nullable)

def _compare_attr(a1, a2):
    """Compare two column attributes"""
    if ('String' in repr(a1) or 'Unicode' in repr(a1)) and ('String' in repr(a2) or 'Unicode' in repr(a2)):
        return a1.length == a2.length
    else:
        if 'Integer' in repr(a1) and 'Integer' in repr(a2):
            return True
        if 'Boolean' in repr(a1) and 'Boolean' in repr(a2):
            return True
        if 'DateTime' in repr(a1) and 'DateTime' in repr(a2):
            return True
        if 'Unicode' in repr(a1) and 'Text' in repr(a2):
            return True
        if 'Pickle' in repr(a1) and 'Blob' in repr(a2):
            return True
        if 'Binary' in repr(a1) and 'Blob' in repr(a2):
            return True
        return a1 == a2


def _compare_column(sqlcolumn, dbcolumn):
    """Compare two Column() objects

    sqlcolumn and dbcolumn should be a Column() instance
    Returns status, result
    where, if status == True,  both Columns are same and result == ''
    else,  if status == False, both Columns are different and result specifies
                               the result message string.
    """
    status = True
    sqlc_props = column_attrs(sqlcolumn)
    dbc_props = column_attrs(dbcolumn)
    result = ''
    if False in map(_compare_attr, sqlc_props, dbc_props):
        status = False
        result = '    sqlcolumn : %s  !=  dbcolumn : %s \n' % (sqlc_props, dbc_props)
    return (status, result)


def column_comparator(sqlcolumns, dbcolumns):
    """Generator function to compare a dictionary to Columns of two tables.

    sqlcolumns and dbcolumns should be dictionaries of type,
        { 'columnname' : Column() object }
    """
    for cname in sqlcolumns.keys():
        sqlcolumn = sqlcolumns[cname]
        dbcolumn = dbcolumns[cname]
        yield _compare_column(sqlcolumn, dbcolumn)


def _compare_table(sqltable, dbtable):
    """Compare two Table() objects

    sqltable and dbtable should be a Table() instance
    Returns status, result
    where, if status == True,  both Tables are same and result == ''
    else,  if status == False, both Tables are different and result specifies
                               the result message string.
    """
    status = True
    sqlt_props = (sqltable.name,)
    dbt_props = (dbtable.name,)
    result = ''
    if sqltable.name != dbtable.name:
        status = False
        result = 'sqltable : %s  !=  dbtable : %s \n' % (sqlt_props, dbt_props)
    else:
        sqlcolumns = dict([ (c.name, c) for c in sqltable.c ])
        dbcolumns = dict([ (c.name, c) for c in dbtable.c ])
        for (st, msg) in column_comparator(sqlcolumns, dbcolumns):
            if st == False:
                result += msg
            if status:
                status = st

        if status == False:
            result = 'For Table %s : %s \n' % (sqltable.name, dbtable.name) + result
    return (
     status, result)


def table_comparator(sqltables, dbtables):
    """Generator function to compare a dictionary to 2 tables

    sqltables and dbtables should be dictionaries of type,
        { 'tablename' : Tabe() object }
    """
    for tname in sqltables.keys():
        sqltable = sqltables[tname]
        dbtable = dbtables[tname]
        yield _compare_table(sqltable, dbtable)


def get_sqltables():
    """Return a dictionary of tables defined by `zeta.model`.
    Skip Dynamic table definitions, which are callables defined in
    zeta.model.schema"""
    sqltables = {}
    sqltables.update([ (g[2:], schema.__dict__[g]) for g in dir(schema) if g[:2] == 't_' if callable(schema.__dict__[g]) == False
                     ] + [ (g[3:], schema.__dict__[g]) for g in dir(schema) if g[:3] == 'at_' ])
    return sqltables


def get_dbtables():
    """Return a dictionary of tables already available in the database"""
    dbtables = {}
    dbtables.update([ (t, Table(t, _metadata, autoload=True, autoload_with=meta.engine)) for t in meta.engine.table_names() if callable(schema.__dict__.get('t_' + t, None)) == False
                    ])
    return dbtables


def verify_tables():
    """Verify Tables as defined by `zeta.model.schema` and as found in the 
    database. The verification can be done only for static tables and not for
    dynamic tables. So, it is better to call this API, before creating dynamic
    tables in the database.
    
    Since the table verification can be a complex job, verify tables returns a
    tuple
        (status, result)
    where,
        if status is True,  result can be ignored.
        if status is False, result contains the message string.
    """
    sqltables = get_sqltables()
    dbtables = get_dbtables()
    status = True
    result = ''
    dbtnames = dbtables.keys()
    for tname in dbtnames:
        if tname[:8] == 'wikipage':
            dbtables.pop(tname)

    if set(sqltables.keys()) != set(dbtables.keys()):
        status = False
        result = 'Mismatch in tablenames : \n(%s) ' % set(sqltables).symmetric_difference(set(dbtables))
    for (st, msg) in table_comparator(sqltables, dbtables):
        if st == False:
            result += msg
        if status:
            status = st

    return (
     status, result)


def verify_permnames():
    """Check for permission names that are not mapped with defgrp_<perm_name>
    group. And permission names that has more than one defgrp_* mapping.
    
    Return ( status, result ), where,
        if status is True,  result can be ignored.
        if status is False, result contains the message string.
    """
    gnames = [ g.perm_group for g in get_permgroups() ]
    orphanperms = [ p for p in get_permnames() if 'defgrp_' + p.perm_name.lower() not in gnames
                  ]
    if orphanperms:
        return (False, 'Permission names without group mapping %s ' % orphanperms)
    else:
        return (
         True, '')


def verify_permgroups():
    """Check for permission groups that are not mapped to any permission names.

    Return ( status, result ), where,
        if status is True,  result can be ignored.
        if status is False, result contains the message string.
    """
    emptygroups = [ g for g in get_permgroups() if not g.perm_names ]
    if emptygroups:
        return (False, 'Permission Groups without grouping permission names %s' % emptygroups)
    else:
        return (
         True, '')


def verify_user():
    """Check whether every entry in user table have 1:1 relationship with
    user_info table.

    Return ( status, result ), where,
        if status is True,  result can be ignored.
        if status is False, result contains the message string.
    """
    userinfos = get_userinfos()
    partialusers = []
    for u in get_users():
        if u.user_info not in userinfos:
            partialusers.append(u)
        userinfos.remove(u.user_info)

    if partialusers:
        return (False, 'User without User info %s' % partialusers)
    else:
        return (
         True, '')


def verify_attachments():
    """Check whether the resource_url attribute for each attachment is
    pointing to a valid attachment file under 'envpath'."""
    pass