# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\migration\schema_generator.py
# Compiled at: 2007-03-06 17:59:57
from sqlalchemy import *
from sqlalchemy.databases.mysql import *

def create_schema(table):
    yield '%s = Table("%s", metadata,' % (table.name, table.name)
    for col in table.columns:
        args = []
        kw = dict()
        col_name = col.name
        if col.primary_key:
            kw['primary_key'] = col.primary_key
        if col.nullable is False and not col.primary_key:
            kw['nullable'] = False
        if col.onupdate:
            kw['onupdate'] = col.onupdate
        col_type_name = col.type.__class__.__name__
        col_type = col_type_name
        if isinstance(col.type, MSEnum):
            enums = (', ').join([ '"\'%s\'"' % i for i in col.type.enums ])
            col_type += '(%s)' % enums
        elif isinstance(col.type, MSDouble):
            col_type = '%s(%s, %s)' % (col_type_name, col.type.length, col.type.precision)
        elif hasattr(col.type, 'length') and col.type.length:
            col_type = '%s(%s)' % (col_type_name, col.type.length)
        if col_type == 'SmallInteger':
            col_type = 'Smallinteger'
        if col.foreign_key:
            if col.foreign_key.constraint.name:
                f_key_str = str(col.foreign_key)[:-1]
                f_key_str += ', name="%s")' % col.foreign_key.constraint.name
                args.append(f_key_str)
            else:
                args.append(col.foreign_key)
        if col.default:
            args.append(col.default)
        if col.unique:
            kw['unique'] = col.unique
        if col.index:
            kw['index'] = col.index
        kw_str = args_str = ''
        for (k, v) in kw.iteritems():
            kw_str += ', %s=%s' % (k, v)

        for i in args:
            args_str += ', %s' % i

        yield '\tColumn("%s", %s%s%s),' % (col_name, col_type, args_str, kw_str)

    for constraint in table.constraints:
        if isinstance(constraint, UniqueConstraint) and len(constraint.columns) > 1:
            cons_str = '\tUniqueConstraint('
            for col in constraint.columns:
                cons_str += '"%s", ' % col.name

            cons_str += 'name="%s"),' % constraint.name
            yield cons_str

    for (k, v) in table.kwargs.iteritems():
        yield '\t%s="%s", ' % (k, v)

    yield ')'