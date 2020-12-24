# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/db/sqlalchemy/migrate_repo/versions/004_map_recipes_capacity.py
# Compiled at: 2016-06-13 14:11:03
from sqlalchemy import Boolean, Column, DateTime, ForeignKey
from sqlalchemy import Integer, MetaData, String, Table
from sqlalchemy import Table, Text, Float

def upgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    crushmaps = Table('crushmaps', meta, Column('id', Integer, primary_key=True, nullable=False), Column('updated_at', DateTime(timezone=False)), Column('created_at', DateTime(timezone=False)), Column('deleted_at', DateTime(timezone=False)), Column('deleted', Boolean(create_constraint=True, name=None)), Column('content', Text(convert_unicode=False, unicode_error=None, _warn_on_bytestring=False), nullable=False))
    recipes = Table('recipes', meta, Column('id', Integer, primary_key=True, nullable=False), Column('recipe_name', String(length=255), unique=True, nullable=False), Column('updated_at', DateTime(timezone=False)), Column('created_at', DateTime(timezone=False)), Column('deleted_at', DateTime(timezone=False)), Column('deleted', Boolean(create_constraint=True, name=None)), Column('pg_num', Integer, nullable=False), Column('pgp_num', Integer, nullable=False), Column('size', Integer, nullable=False), Column('min_size', Integer), Column('crush_ruleset', Integer, nullable=False), Column('crash_replay_interval', Integer))
    vsm_capacity_manages = Table('vsm_capacity_manages', meta, Column('id', Integer, primary_key=True, nullable=False), Column('name', String(length=255), nullable=False), Column('capacity_quota_mb', Integer), Column('capacity_used_mb', Integer), Column('updated_at', DateTime(timezone=False)), Column('created_at', DateTime(timezone=False)), Column('deleted_at', DateTime(timezone=False)), Column('deleted', Boolean(create_constraint=True, name=None)), Column('testyr', Integer))
    try:
        crushmaps.create()
    except Exception:
        meta.drop_all(tables=[crushmaps])
        raise

    try:
        recipes.create()
    except Exception:
        meta.drop_all(tables=[recipes])
        raise

    try:
        vsm_capacity_manages.create()
    except Exception:
        meta.drop_all(tables=[vsm_capacity_manages])
        raise

    return


def downgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    crushmaps = Table('crushmaps', meta, autoload=True)
    crushmaps.drop()
    recipes = Table('recipes', meta, autoload=True)
    recipes.drop()
    vsm_capacity_manages = Table('vsm_capacity_manages', meta, autoload=True)
    vsm_capacity_manages.drop()