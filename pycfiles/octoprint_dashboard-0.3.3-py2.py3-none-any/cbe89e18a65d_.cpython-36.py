# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jirimakarius/Projects/OctoPrint-Dashboard/octoprint_dashboard/model/migrations/versions/cbe89e18a65d_.py
# Compiled at: 2017-10-19 04:29:16
# Size of source mod 2**32: 903 bytes
"""empty message

Revision ID: cbe89e18a65d
Revises: 573d726a5860
Create Date: 2017-10-19 10:11:16.624446

"""
import sqlalchemy as sa
from alembic import op
import octoprint_dashboard
revision = 'cbe89e18a65d'
down_revision = '573d726a5860'
branch_labels = None
depends_on = None
OAUTH_CVUT = 'oauth_cvut'
NONE = 'none'
AUTH_CHOICES = (
 (
  OAUTH_CVUT, 'ČVUT - OAuth'),
 (
  NONE, 'None'))

def upgrade():
    op.add_column('config', sa.Column('auth', (octoprint_dashboard.model.utils.ChoiceType(AUTH_CHOICES)), server_default=NONE, nullable=False))


def downgrade():
    op.drop_column('config', 'auth')