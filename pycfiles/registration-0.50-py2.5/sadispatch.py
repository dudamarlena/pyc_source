# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/registration/ormmanager/sadispatch.py
# Compiled at: 2008-07-04 10:34:30
from api import create, retrieve, retrieve_one, update, delete, count
import sqlalchemy as sa
from turbogears.database import session
class_test = 'isSqlAlchemyClass(class_)'
obj_test = 'isSqlAlchemyObject(obj)'

def isSqlAlchemyClass(class_):
    try:
        mapper = sa.orm.class_mapper(class_)
    except sa.exceptions.InvalidRequestError:
        return False

    return True


def isSqlAlchemyObject(obj):
    try:
        mapper = sa.orm.object_mapper(obj)
    except sa.exceptions.InvalidRequestError:
        return False

    return True


def sa_create(class_, **kw):
    try:
        obj = class_(**kw)
    except TypeError:
        obj = class_()

    sa_update(obj, **kw)
    return obj


sa_create = create.when(class_test)(sa_create)

def sa_retrieve(class_, **kw):
    return session.query(class_).filter_by(**kw).all()


sa_retrieve = retrieve.when(class_test)(sa_retrieve)

def sa_retrieve_one(class_, **kw):
    query = session.query(class_).filter_by(**kw)
    count = query.count()
    if count == 0:
        return
    elif count == 1:
        return query[0]
    else:
        raise LookupError, 'Received %d results.' % count
    return


sa_retreive_one = retrieve_one.when(class_test)(sa_retrieve_one)

def sa_update(obj, **kw):
    [ setattr(obj, key, value) for (key, value) in kw.iteritems() ]
    push_to_db(obj)


sa_update = update.when(obj_test)(sa_update)

def sa_delete(obj):
    session = session_for_obj(obj)
    session.delete(obj)
    session.flush()


sa_delete = delete.when(obj_test)(sa_delete)

def sa_count(class_, **kw):
    return session.query(class_).filter_by(**kw).count()


sa_count = count.when(class_test)(sa_count)

def push_to_db(obj):
    session = session_for_obj(obj)
    session.save_or_update(obj)
    session.flush((obj,))


def session_for_obj(obj):
    s = sa.orm.object_session(obj)
    if not s:
        s = session
    return s