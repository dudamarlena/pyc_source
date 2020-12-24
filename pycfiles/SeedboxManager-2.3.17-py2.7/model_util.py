# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.cygwin-1.7.35-i686/egg/seedbox/db/sqlalchemy/model_util.py
# Compiled at: 2015-06-14 13:30:57
"""
Provides utilities for managing models
"""
import logging
from seedbox.db import models as api_model
from seedbox.db.sqlalchemy import models as db_model
LOG = logging.getLogger(__name__)

def from_db(db_item):
    """Database to Model

    Handles the conversion from the database model object to the
    corresponding public facing api model object. If an item has
    a reference to another model object then the call is recursive.

    :param db_item: an instance of a database model object
    :returns: an instance of an api model object
    """
    if db_item is None:
        return db_item
    else:
        _model = getattr(api_model, db_item.__class__.__name__)
        instance = _model.make_empty()
        for k in instance:
            if k == instance.PK_NAME:
                instance[k] = db_item.get('id')
            else:
                _attr = db_item.get(k)
                if isinstance(_attr, db_model.Base):
                    instance[k] = from_db(_attr)
                elif isinstance(_attr, list) and _attr and isinstance(_attr[0], db_model.Base):
                    instance[k] = [ from_db(v) for v in _attr ]
                else:
                    instance[k] = _attr

        return instance


def to_db(api_item, db_item=None):
    """Model to database

    Handles the conversion from the api model object to the
    corresponding database model object. If an item has
    a reference to another model object then the call is recursive.

    :param api_item: an instance of a api model object
    :param db_item: an instance of a database model object that
                    is to be updated. (optional)
    :returns: an instance of an database model object
    """
    if api_item is None:
        return api_item
    else:
        row = db_item
        if row is None:
            _model = getattr(db_model, api_item.__class__.__name__)
            row = _model(id=getattr(api_item, api_item.PK_NAME))
        for k, v in api_item.items():
            if isinstance(v, api_model.Model):
                v = to_db(v)
            elif isinstance(v, list) and v and isinstance(v[0], api_model.Model):
                v = [ to_db(elm) for elm in v ]
            row[k] = v

        return row