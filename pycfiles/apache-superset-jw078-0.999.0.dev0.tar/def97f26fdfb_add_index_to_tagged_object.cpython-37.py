# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/def97f26fdfb_add_index_to_tagged_object.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1266 bytes
__doc__ = 'Add index to tagged_object\n\nRevision ID: def97f26fdfb\nRevises: d6ffdf31bdd4\nCreate Date: 2019-07-11 19:02:38.768324\n\n'
revision = 'def97f26fdfb'
down_revision = '190188938582'
from alembic import op

def upgrade():
    op.create_index((op.f('ix_tagged_object_object_id')),
      'tagged_object', ['object_id'], unique=False)


def downgrade():
    op.drop_index((op.f('ix_tagged_object_object_id')), table_name='tagged_object')