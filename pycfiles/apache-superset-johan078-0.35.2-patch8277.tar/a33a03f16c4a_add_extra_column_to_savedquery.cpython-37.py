# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/a33a03f16c4a_add_extra_column_to_savedquery.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 2090 bytes
__doc__ = 'Add extra column to SavedQuery\n\nLicensed to the Apache Software Foundation (ASF) under one or more\ncontributor license agreements.  See the NOTICE file distributed with\nthis work for additional information regarding copyright ownership.\nThe ASF licenses this file to You under the Apache License, Version 2.0\n(the "License"); you may not use this file except in compliance with\nthe License.  You may obtain a copy of the License at\n\n    http://www.apache.org/licenses/LICENSE-2.0\n\nUnless required by applicable law or agreed to in writing, software\ndistributed under the License is distributed on an "AS IS" BASIS,\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\nSee the License for the specific language governing permissions and\nlimitations under the License.\n\nRevision ID: a33a03f16c4a\nRevises: fb13d49b72f9\nCreate Date: 2019-01-14 16:00:26.344439\n\n'
revision = 'a33a03f16c4a'
down_revision = 'fb13d49b72f9'
import sqlalchemy as sa
from alembic import op

def upgrade():
    with op.batch_alter_table('saved_query') as (batch_op):
        batch_op.add_column(sa.Column('extra_json', (sa.Text()), nullable=True))


def downgrade():
    with op.batch_alter_table('saved_query') as (batch_op):
        batch_op.drop_column('extra_json')