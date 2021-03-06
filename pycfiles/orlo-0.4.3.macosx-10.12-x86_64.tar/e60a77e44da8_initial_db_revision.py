# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /vagrant/orlo/orlo/migrations/e60a77e44da8_initial_db_revision.py
# Compiled at: 2017-04-03 12:00:52
"""Initial DB revision

Revision ID: e60a77e44da8
Revises: 
Create Date: 2016-11-24 17:03:25.249133

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy_utils.types.uuid import UUIDType
from sqlalchemy_utils.types.arrow import ArrowType
from orlo.config import config
revision = 'e60a77e44da8'
down_revision = None
branch_labels = ('default', )
depends_on = None

class HackyUUIDType(UUIDType):
    """ Horrible hack for SQLAlchemy-utils' UUID, which doesn't support
    Alembic yet

    For Postgres, we return the UUID dialect, for others CHAR(36)
    See https://github.com/kvesteri/sqlalchemy-utils/issues/129
    """

    def __repr__(self):
        """
        :return:
        """
        uri = config.get('db', 'uri')
        if uri.startswith('postgresql'):
            return 'sa.dialects.postgresql.UUID()'
        else:
            if uri.startswith('mysql'):
                return 'sa.dialects.mysql.CHAR(32)'
            return 'sa.types.CHAR(32)'


def upgrade():
    op.create_table('platform', sa.Column('id', HackyUUIDType(), nullable=False), sa.Column('name', sa.Text(), nullable=False), sa.PrimaryKeyConstraint('id'), sa.UniqueConstraint('id'), sa.UniqueConstraint('name'))
    op.create_table('release', sa.Column('id', HackyUUIDType(), nullable=False), sa.Column('references', sa.String(), nullable=True), sa.Column('stime', ArrowType(), nullable=True), sa.Column('ftime', ArrowType(), nullable=True), sa.Column('duration', sa.Interval(), nullable=True), sa.Column('user', sa.String(), nullable=False), sa.Column('team', sa.String(), nullable=True), sa.PrimaryKeyConstraint('id'), sa.UniqueConstraint('id'))
    op.create_index(op.f('ix_release_stime'), 'release', ['stime'], unique=False)
    op.create_table('package', sa.Column('id', HackyUUIDType(), nullable=False), sa.Column('name', sa.String(length=120), nullable=False), sa.Column('stime', ArrowType(), nullable=True), sa.Column('ftime', ArrowType(), nullable=True), sa.Column('duration', sa.Interval(), nullable=True), sa.Column('status', sa.Enum('NOT_STARTED', 'IN_PROGRESS', 'SUCCESSFUL', 'FAILED', name='status_types'), nullable=True), sa.Column('version', sa.String(length=32), nullable=False), sa.Column('diff_url', sa.String(), nullable=True), sa.Column('rollback', sa.Boolean(), nullable=True), sa.Column('release_id', HackyUUIDType(), nullable=True), sa.ForeignKeyConstraint(['release_id'], ['release.id']), sa.PrimaryKeyConstraint('id'), sa.UniqueConstraint('id'))
    op.create_index(op.f('ix_package_stime'), 'package', ['stime'], unique=False)
    op.create_table('release_metadata', sa.Column('id', HackyUUIDType(), nullable=False), sa.Column('release_id', HackyUUIDType(), nullable=True), sa.Column('key', sa.Text(), nullable=False), sa.Column('value', sa.Text(), nullable=False), sa.ForeignKeyConstraint(['release_id'], ['release.id']), sa.PrimaryKeyConstraint('id'), sa.UniqueConstraint('id'))
    op.create_table('release_note', sa.Column('id', HackyUUIDType(), nullable=False), sa.Column('content', sa.Text(), nullable=False), sa.Column('release_id', HackyUUIDType(), nullable=True), sa.ForeignKeyConstraint(['release_id'], ['release.id']), sa.PrimaryKeyConstraint('id'), sa.UniqueConstraint('id'))
    op.create_table('release_platform', sa.Column('release_id', HackyUUIDType(), nullable=True), sa.Column('platform_id', HackyUUIDType(), nullable=True), sa.ForeignKeyConstraint(['platform_id'], ['platform.id']), sa.ForeignKeyConstraint(['release_id'], ['release.id']))
    op.create_table('package_result', sa.Column('id', HackyUUIDType(), nullable=False), sa.Column('content', sa.Text(), nullable=True), sa.Column('package_id', HackyUUIDType(), nullable=True), sa.ForeignKeyConstraint(['package_id'], ['package.id']), sa.PrimaryKeyConstraint('id'), sa.UniqueConstraint('id'))


def downgrade():
    op.drop_table('package_result')
    op.drop_table('release_platform')
    op.drop_table('release_note')
    op.drop_table('release_metadata')
    op.drop_index(op.f('ix_package_stime'), table_name='package')
    op.drop_table('package')
    op.drop_index(op.f('ix_release_stime'), table_name='release')
    op.drop_table('release')
    op.drop_table('platform')