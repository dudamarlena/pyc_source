# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sachowdh/code/fedora-infra/autocloud/alembic/versions/55932e5d6b3f_added_family_arch_fields_in_job_table.py
# Compiled at: 2016-05-27 13:17:50
"""Added family, arch fields in Job table.

Revision ID: 55932e5d6b3f
Revises: 159b60132535
Create Date: 2015-12-05 12:44:33.525292

"""
revision = '55932e5d6b3f'
down_revision = '159b60132535'
branch_labels = None
depends_on = None
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('job_details', sa.Column('arch', sa.String(length=255), nullable=True))
    op.add_column('job_details', sa.Column('family', sa.String(length=255), nullable=True))
    op.add_column('job_details', sa.Column('release', sa.String(length=255), nullable=True))


def downgrade():
    op.drop_column('job_details', 'family')
    op.drop_column('job_details', 'arch')
    op.drop_column('job_details', 'release')