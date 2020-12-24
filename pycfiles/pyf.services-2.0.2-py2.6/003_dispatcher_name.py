# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyf/services/migration/versions/003_dispatcher_name.py
# Compiled at: 2010-10-05 09:06:46
from sqlalchemy import *
from migrate import *
import migrate.changeset
from pyf.services.model import DBSession, Dispatch
import unicodedata
metadata = MetaData(migrate_engine)
dispatchs_table = Table('dispatchs', metadata, autoload=True)

def upgrade():
    name_col = Column('name', Unicode(50), unique=True)
    name_col.create(dispatchs_table)
    connection = migrate_engine.connect()
    results = connection.execute(dispatchs_table.select())
    for row in results:
        display_name = unicode(row.display_name, 'utf-8')
        name = display_name.lower().replace(' ', '_')
        nkfd_form = unicodedata.normalize('NFKD', name)
        name = ('').join([ c for c in nkfd_form if not unicodedata.combining(c) ])
        connection.execute("update dispatchs set name='%s' where display_name='%s'" % (name, display_name))

    name_col.alter(nullable=False)


def downgrade():
    name_col = dispatchs_table.columns['name']
    name_col.drop()