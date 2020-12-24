# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/migrations/versions/f23433877c24_fix_mysql_not_null_constraint.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 1991 bytes
"""fix mysql not null constraint

Revision ID: f23433877c24
Revises: 05f30312d566
Create Date: 2018-06-17 10:16:31.412131

"""
from alembic import op
from sqlalchemy.dialects import mysql
revision = 'f23433877c24'
down_revision = '05f30312d566'
branch_labels = None
depends_on = None

def upgrade():
    conn = op.get_bind()
    if conn.dialect.name == 'mysql':
        conn.execute("SET time_zone = '+00:00'")
        op.alter_column('task_fail', 'execution_date', existing_type=mysql.TIMESTAMP(fsp=6), nullable=False)
        op.alter_column('xcom', 'execution_date', existing_type=mysql.TIMESTAMP(fsp=6), nullable=False)
        op.alter_column('xcom', 'timestamp', existing_type=mysql.TIMESTAMP(fsp=6), nullable=False)


def downgrade():
    conn = op.get_bind()
    if conn.dialect.name == 'mysql':
        conn.execute("SET time_zone = '+00:00'")
        op.alter_column('xcom', 'timestamp', existing_type=mysql.TIMESTAMP(fsp=6), nullable=True)
        op.alter_column('xcom', 'execution_date', existing_type=mysql.TIMESTAMP(fsp=6), nullable=True)
        op.alter_column('task_fail', 'execution_date', existing_type=mysql.TIMESTAMP(fsp=6), nullable=True)