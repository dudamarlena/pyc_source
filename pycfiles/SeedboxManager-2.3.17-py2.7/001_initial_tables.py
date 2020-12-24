# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.cygwin-1.7.35-i686/egg/seedbox/db/sqlalchemy/migrate_repo/versions/001_initial_tables.py
# Compiled at: 2015-06-14 13:30:57
"""Initial version of the database model;

maintained to support anyone upgrading from a previous version.
"""
from datetime import datetime
import sqlalchemy as sa
STATES = [
 'init', 'ready', 'active', 'done', 'cancelled']

def upgrade(migrate_engine):
    """Creates the initial version of the database tables.

    :param migrate_engine: an instance of database connection engine
    """
    meta = sa.MetaData(bind=migrate_engine)
    appstate = sa.Table('app_state', meta, sa.Column('id', sa.Integer, primary_key=True), sa.Column('name', sa.String(255), unique=True), sa.Column('val_str', sa.String(255), nullable=True, default=None), sa.Column('val_int', sa.Integer, nullable=True, default=None), sa.Column('val_list', sa.String(1000), default=None), sa.Column('val_flag', sa.Boolean, nullable=True, default=None), sa.Column('val_date', sa.DateTime, nullable=True, default=None))
    appstate.create(checkfirst=True)
    torrent = sa.Table('torrent', meta, sa.Column('id', sa.Integer, primary_key=True), sa.Column('name', sa.String(255), unique=True), sa.Column('create_date', sa.DateTime, default=datetime.utcnow), sa.Column('state', sa.Enum(*STATES), default='init'), sa.Column('retry_count', sa.Integer, default=0), sa.Column('failed', sa.Boolean, default=False), sa.Column('error_msg', sa.String(1000), default=None), sa.Column('invalid', sa.Boolean, default=False), sa.Column('purged', sa.Boolean, default=False))
    torrent.create(checkfirst=True)
    media = sa.Table('media_file', meta, sa.Column('id', sa.Integer, primary_key=True), sa.Column('filename', sa.String(255)), sa.Column('file_ext', sa.String(30)), sa.Column('file_path', sa.String(1000), default=None), sa.Column('size', sa.Integer, default=0), sa.Column('compressed', sa.Boolean, default=False), sa.Column('synced', sa.Boolean, default=False), sa.Column('missing', sa.Boolean, default=False), sa.Column('skipped', sa.Boolean, default=False), sa.Column('torrent_id', sa.Integer, sa.ForeignKey('torrent.id')))
    media.create(checkfirst=True)
    return


def downgrade(migrate_engine):
    """Not implemented because this is associated with initial version.

    :param migrate_engine: an instance of database connection engine
    :raise NotImplementedError: if method executed
    """
    raise NotImplementedError('Downgrade from initial version is unsupported.')