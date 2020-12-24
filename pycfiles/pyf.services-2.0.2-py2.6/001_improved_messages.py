# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyf/services/migration/versions/001_improved_messages.py
# Compiled at: 2010-05-21 08:57:50
from sqlalchemy import *
from migrate import *
import migrate.changeset
metadata = MetaData(migrate_engine)
eventhistory_table = Table('eventhistory', metadata, autoload=True)

def upgrade():
    message_type_col = Column('message_type', Unicode(10), server_default='info')
    message_type_col.create(eventhistory_table)


def downgrade():
    message_type_col = eventhistory_table.columns['message_type']
    message_type_col.drop()