# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyf/services/migration/versions/002_increase_payload_size.py
# Compiled at: 2010-05-21 08:57:50
from sqlalchemy import *
from migrate import *
import migrate.changeset
metadata = MetaData(migrate_engine)

def upgrade():
    connection = migrate_engine.connect()
    connection.execute('ALTER TABLE tubes ALTER COLUMN payload TYPE character varying(524288)')


def downgrade():
    connection = migrate_engine.connect()
    connection.execute('ALTER TABLE tubes ALTER COLUMN payload TYPE character varying(65536)')