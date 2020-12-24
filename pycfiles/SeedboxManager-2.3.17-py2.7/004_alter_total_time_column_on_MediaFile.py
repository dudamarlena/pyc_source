# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.cygwin-1.7.35-i686/egg/seedbox/db/sqlalchemy/migrate_repo/versions/004_alter_total_time_column_on_MediaFile.py
# Compiled at: 2015-06-14 13:29:33
"""Handles converting MediaFile.total_time from Integer to Float"""
import sqlalchemy as sa

def upgrade(migrate_engine):
    meta = sa.MetaData(bind=migrate_engine)
    table = sa.Table('media_files', meta, autoload=True)
    col_resource = getattr(table.c, 'total_time')
    col_resource.alter(type=sa.Float)


def downgrade(migrate_engine):
    meta = sa.MetaData(bind=migrate_engine)
    table = sa.Table('media_files', meta, autoload=True)
    col_resource = getattr(table.c, 'total_time')
    col_resource.alter(type=sa.Integer)