# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/migrations/versions/bdaa763e6c56_make_xcom_value_column_a_large_binary.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 1607 bytes
__doc__ = 'Make xcom value column a large binary\n\nRevision ID: bdaa763e6c56\nRevises: cc1e65623dc7\nCreate Date: 2017-08-14 16:06:31.568971\n\n'
from alembic import op
import dill, sqlalchemy as sa
revision = 'bdaa763e6c56'
down_revision = 'cc1e65623dc7'
branch_labels = None
depends_on = None

def upgrade():
    with op.batch_alter_table('xcom') as (batch_op):
        batch_op.alter_column('value', type_=(sa.LargeBinary()))


def downgrade():
    with op.batch_alter_table('xcom') as (batch_op):
        batch_op.alter_column('value', type_=sa.PickleType(pickler=dill))