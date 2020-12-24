# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/snmpsim_control_plane/metrics/utils.py
# Compiled at: 2020-01-30 12:14:23
from sqlalchemy import func
from snmpsim_control_plane.metrics import db

def autoincrement(obj, model):
    """Add unique ID to model.

    Sqlalchemy's merge requires unique fields being primary keys. On top of
    that, autoincrement does not always work with Sqlalchemy. Thus this
    hack to generate unique row ID. %-(
    """
    if obj.id is None:
        max_id = db.session.query(func.max(model.id)).first()
        max_id = max_id[0]
        max_id = max_id + 1 if max_id else 1
        obj.id = max_id
        db.session.commit()
    return