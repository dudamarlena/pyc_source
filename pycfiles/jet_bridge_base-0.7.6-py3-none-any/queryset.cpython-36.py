# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/f1nal/Dropbox/python/jet-bridge/src/packages/jet_bridge_base/jet_bridge_base/utils/queryset.py
# Compiled at: 2019-11-15 03:30:19
# Size of source mod 2**32: 2047 bytes
from sqlalchemy import inspect, desc
from sqlalchemy.sql import operators, text
from sqlalchemy.sql.elements import AnnotatedColumnElement, UnaryExpression
from jet_bridge_base import settings
from jet_bridge_base.db import engine

def get_queryset_model(queryset):
    return queryset._primary_entity.entity_zero_or_selectable.entity


def apply_default_ordering(queryset):
    model = get_queryset_model(queryset)
    mapper = inspect(model)
    pk = mapper.primary_key[0].name
    ordering = queryset._order_by if queryset._order_by else []

    def is_pk(x):
        if isinstance(x, AnnotatedColumnElement):
            return x.name == pk
        else:
            if isinstance(x, UnaryExpression):
                return x.element.name == pk and x.modifier == operators.desc_op
            return False

    if ordering is None or not any(map(is_pk, ordering)):
        order_by = list(ordering or []) + [desc(pk)]
        queryset = (queryset.order_by)(*order_by)
    return queryset


def queryset_count_optimized_for_postgresql(db_table):
    with engine.connect() as (connection):
        cursor = connection.execute(text('SELECT reltuples FROM pg_class WHERE relname = :db_table'), {'db_table': db_table})
        row = cursor.fetchone()
        return int(row[0])


def queryset_count_optimized_for_mysql(db_table):
    with engine.connect() as (connection):
        cursor = connection.execute(text('EXPLAIN SELECT COUNT(*) FROM `{}`'.format(db_table)))
        row = cursor.fetchone()
        return int(row[8])


def queryset_count_optimized(queryset):
    result = None
    if queryset.whereclause is None:
        try:
            table = queryset.statement.froms[0].name
            if settings.DATABASE_ENGINE == 'postgresql':
                result = queryset_count_optimized_for_postgresql(table)
            else:
                if settings.DATABASE_ENGINE == 'mysql':
                    result = queryset_count_optimized_for_mysql(table)
        except:
            pass

    if result is not None:
        if result >= 10000:
            return result
    return queryset.count()