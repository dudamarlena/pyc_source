# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bdgt/storage/gateway.py
# Compiled at: 2014-10-09 13:38:05
import logging
from bdgt.storage.database import session_scope
_log = logging.getLogger(__name__)

def save_object(object_):
    _log.info(("Saving '{}'").format(type(object_)))
    with session_scope() as (session):
        session.add(object_)


def save_objects(objects):
    _log.info(("Saving '{}' object").format(len(objects)))
    with session_scope() as (session):
        session.add_all(objects)


def delete_object(object_):
    _log.info(("Deleting '{}' with id {}").format(type(object_), object_.id))
    with session_scope() as (session):
        session.delete(object_)