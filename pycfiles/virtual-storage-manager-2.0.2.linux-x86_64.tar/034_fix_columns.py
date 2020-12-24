# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/db/sqlalchemy/migrate_repo/versions/034_fix_columns.py
# Compiled at: 2016-06-13 14:11:03


def upgrade(migrate_engine):
    migrate_engine.execute('alter table devices modify avail_capacity_kb bigint(20) not null')
    migrate_engine.execute('alter table devices modify total_capacity_kb bigint(20) not null')
    migrate_engine.execute('alter table devices modify used_capacity_kb bigint(20) not null')


def downgrade(migrate_engine):
    migrate_engine.execute('alter table devices modify avail_capacity_kb int(11) not null')
    migrate_engine.execute('alter table devices modify total_capacity_kb int(11) not null')
    migrate_engine.execute('alter table devices modify used_capacity_kb int(11) not null')