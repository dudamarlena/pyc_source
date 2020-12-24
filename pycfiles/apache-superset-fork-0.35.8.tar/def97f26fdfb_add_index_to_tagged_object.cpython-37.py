# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/def97f26fdfb_add_index_to_tagged_object.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1266 bytes
"""Add index to tagged_object

Revision ID: def97f26fdfb
Revises: d6ffdf31bdd4
Create Date: 2019-07-11 19:02:38.768324

"""
revision = 'def97f26fdfb'
down_revision = '190188938582'
from alembic import op

def upgrade():
    op.create_index((op.f('ix_tagged_object_object_id')),
      'tagged_object', ['object_id'], unique=False)


def downgrade():
    op.drop_index((op.f('ix_tagged_object_object_id')), table_name='tagged_object')