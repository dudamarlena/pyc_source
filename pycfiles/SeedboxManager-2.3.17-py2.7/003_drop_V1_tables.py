# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.cygwin-1.7.35-i686/egg/seedbox/db/sqlalchemy/migrate_repo/versions/003_drop_V1_tables.py
# Compiled at: 2015-06-14 13:30:57
"""Provides removing the initial version of the database tables.

Used for clean up purposes.
"""
import sqlalchemy as sa

def upgrade(migrate_engine):
    """Drops the initial version of the tables.

    :param migrate_engine: an instance of database connection engine
    """
    meta = sa.MetaData(bind=migrate_engine)
    appstates = sa.Table('app_state', meta)
    appstates.drop(checkfirst=True)
    torrents = sa.Table('torrent', meta)
    torrents.drop(checkfirst=True)
    medias = sa.Table('media_file', meta)
    medias.drop(checkfirst=True)


def downgrade(migrate_engine):
    """Does nothing.

    Since the ability to go version 1 from 3 is not supported directly.

    :param migrate_engine: an instance of database connection engine
    """
    pass