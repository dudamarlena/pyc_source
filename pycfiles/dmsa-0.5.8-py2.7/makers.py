# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dmsa/makers.py
# Compiled at: 2016-02-12 12:18:44
from __future__ import unicode_literals
from sqlalchemy import Column, Integer, Numeric, Float, String, Date, DateTime, Time, Text, Boolean, LargeBinary, Table
from sqlalchemy.schema import PrimaryKeyConstraint, ForeignKeyConstraint, Index, UniqueConstraint
DATATYPE_MAP = {b'integer': Integer, 
   b'number': Numeric, 
   b'decimal': Numeric, 
   b'float': Float, 
   b'string': String, 
   b'date': Date, 
   b'datetime': DateTime, 
   b'timestamp': DateTime, 
   b'time': Time, 
   b'text': Text, 
   b'clob': Text, 
   b'boolean': Boolean, 
   b'blob': LargeBinary}

def make_index(index_json):
    """Returns a dynamically constructed SQLAlchemy model Index class.

    `index_json` is a declarative style dictionary index object, as defined by
    the chop-dbhi/data-models package.
    """
    idx_name = index_json.get(b'name')
    return Index(idx_name, *index_json[b'fields'])


def make_constraint(constraint_type, constraint_json):
    """Returns a dynamically constructed SQLAlchemy model Constraint class.

    `constraint_type` is a string that maps to the type of constraint to be
    constructed.

    `constraint_json` is a declarative style dictionary constraint object, as
    defined by the chop-dbhi/data-models package.
    """
    constraint_name = constraint_json.get(b'name')
    if constraint_type == b'primary_keys':
        return PrimaryKeyConstraint(name=constraint_name, *constraint_json[b'fields'])
    if constraint_type == b'foreign_keys':
        source_column_list = [constraint_json[b'source_field']]
        target_column_list = [
         (b'.').join([constraint_json[b'target_table'],
          constraint_json[b'target_field']])]
        return ForeignKeyConstraint(source_column_list, target_column_list, constraint_name, use_alter=True)
    if constraint_type == b'uniques':
        return UniqueConstraint(name=constraint_name, *constraint_json[b'fields'])


def make_column(field, not_null_flag=False):
    """Returns a dynamically constructed SQLAlchemy model Column class.

    `field` is a declarative style dictionary field object retrieved from the
    chop-dbhi/data-models service or at least matching the format specified
    there.

    `not_null_flag` signifies that a not null constraint should be included.
    """
    column_kwargs = {}
    column_kwargs[b'name'] = field[b'name']
    type_string = field[b'type']
    type_class = DATATYPE_MAP[type_string]
    type_kwargs = {}
    if field.get(b'description'):
        column_kwargs[b'doc'] = field[b'description']
    if field.get(b'default'):
        column_kwargs[b'default'] = field[b'default']
        column_kwargs[b'server_default'] = field[b'default']
    if not_null_flag:
        column_kwargs[b'nullable'] = False
    if type_class == String:
        type_kwargs[b'length'] = field.get(b'length') or 256
    if type_class == Numeric:
        type_kwargs[b'precision'] = field.get(b'precision') or 20
        type_kwargs[b'scale'] = field.get(b'scale') or 5
    column_kwargs[b'type_'] = type_class(**type_kwargs)
    return Column(**column_kwargs)


def make_table(table_json, metadata, not_nulls):
    """Makes and attaches a SQLAlchemy Table class to the metadata object.

    `table_json` is a declarative style nested table object retrieved from the
    chop-dbhi/data-models service or at least matching the format specified
    there.

    `metadata` is the metadata instance the produced model should attach to.
    This could simply be sqlalchemy.MetaData().

    `not_nulls` is a list of table-relevant not null constraints matching the
    chop-dbhi/data-models specified format.
    """
    table = Table(table_json[b'name'], metadata)
    for field in table_json.get(b'fields', []):
        not_null_flag = False
        for not_null in not_nulls:
            if not_null[b'field'] == field[b'name']:
                not_null_flag = True
                break

        table.append_column(make_column(field, not_null_flag))

    return table


def make_model(data_model, metadata):
    """Makes and attaches a collection of SQLAlchemy classes that describe a
    data model to the metadata object.

    `data_model` is a declarative style nested data model object retrieved from
    the chop-dbhi/data-models service or at least matching the format specified
    there.

    `metadata` is the metadata instance the produced models should attach to.
    This could simply be sqlalchemy.MetaData().
    """
    for table_json in data_model[b'tables']:
        table_not_nulls = []
        for not_null in data_model[b'schema'][b'constraints'][b'not_null'] or []:
            if not_null[b'table'] == table_json[b'name']:
                table_not_nulls.append(not_null)

        make_table(table_json, metadata, table_not_nulls)

    for con_type, con_list in data_model[b'schema'][b'constraints'].iteritems():
        if con_type != b'not_null':
            for con in con_list or []:
                table_name = con.get(b'table') or con.get(b'source_table')
                metadata.tables[table_name].append_constraint(make_constraint(con_type, con))

    for index in data_model[b'schema'][b'indexes']:
        table_name = index[b'table']
        metadata.tables[table_name].append_constraint(make_index(index))

    return metadata


def make_model_from_service(model, model_version, service, metadata):
    from dmsa.utility import get_model_json
    return make_model(get_model_json(model, model_version, service), metadata)