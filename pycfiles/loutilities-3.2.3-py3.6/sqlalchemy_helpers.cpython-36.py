# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\loutilities\sqlalchemy_helpers.py
# Compiled at: 2019-11-20 14:41:28
# Size of source mod 2**32: 4057 bytes
"""
sqlalchemy_helpers  -- helper functions for sqlalchemy access
===================================================

"""
from sqlalchemy.orm import object_mapper

class dbConsistencyError(Exception):
    pass


class parameterError(Exception):
    pass


def getunique(session, model, **kwargs):
    """
    retrieve a row from the database, raising exception of more than one row exists for query criteria
    
    :param session: session within which update occurs
    :param model: table model
    :param kwargs: query criteria
    
    :rtype: single instance of the row, or None
    """
    instances = (session.query(model).filter_by)(**kwargs).all()
    if len(instances) > 1:
        raise dbConsistencyError('found multiple rows in {0} for {1}'.format(model, kwargs))
    if len(instances) == 0:
        return
    else:
        return instances[0]


def update(session, model, oldinstance, newinstance, skipcolumns=[]):
    """
    update an existing element based on kwargs query
    
    :param session: session within which update occurs
    :param model: table model
    :param oldinstance: instance of table model which was found in the db
    :param newinstance: instance of table model with updated fields
    :param skipcolumns: list of column names to update
    :rtype: boolean indicates whether any fields have changed
    """
    updated = False
    for col in object_mapper(newinstance).columns:
        if col.key in skipcolumns:
            pass
        else:
            if getattr(oldinstance, col.key) != getattr(newinstance, col.key):
                setattr(oldinstance, col.key, getattr(newinstance, col.key))
                updated = True

    return updated


def insert_or_update(session, model, newinstance, skipcolumns=[], **kwargs):
    """
    insert a new element or update an existing element based on kwargs query
    
    :param session: session within which update occurs
    :param model: table model
    :param newinstance: instance of table model which is to become representation in the db
    :param skipcolumns: list of column names to skip checking for any changes
    :param kwargs: query criteria
    """
    instance = getunique(session, model, **kwargs)
    updated = False
    if instance is not None:
        updated = update(session, model, instance, newinstance, skipcolumns)
    else:
        session.add(newinstance)
        updated = True
    if updated:
        session.flush()
    return updated