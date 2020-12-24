# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bauble/meta.py
# Compiled at: 2016-10-03 09:39:22
from sqlalchemy import Unicode, UnicodeText, Column
import bauble.db as db, bauble.utils as utils
VERSION_KEY = 'version'
CREATED_KEY = 'created'
REGISTRY_KEY = 'registry'
DATE_FORMAT_KEY = 'date_format'

def get_default(name, default=None, session=None):
    """
    Get a BaubleMeta object with name.  If the default value is not
    None then a BaubleMeta object is returned with name and the
    default value given.

    If a session instance is passed (session != None) then we
    don't commit the session.
    """
    commit = False
    if not session:
        session = db.Session()
        commit = True
    query = session.query(BaubleMeta)
    meta = query.filter_by(name=name).first()
    if not meta and default is not None:
        meta = BaubleMeta(name=utils.utf8(name), value=default)
        session.add(meta)
        if commit:
            session.commit()
            meta.value
            meta.name
    if commit:
        session.close()
    return meta


class BaubleMeta(db.Base):
    """
    The BaubleMeta class is used to set and retrieve meta information
    based on key/name values from the bauble meta table.

    :Table name: bauble

    :Columns:
      *name*:
        The name of the data.

      *value*:
        The value.

    """
    __tablename__ = 'bauble'
    name = Column(Unicode(64), unique=True)
    value = Column(UnicodeText)