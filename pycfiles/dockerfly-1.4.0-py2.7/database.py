# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dockerfly/runtime/database.py
# Compiled at: 2016-06-30 23:57:44
import os, json, time, shutil
from dockerfly import settings
from dockerfly.contrib.filelock import FileLock
db_dir = settings.DB_ROOT
dbs = settings.dbs

def get_db_lockfile(db_name):
    db_file = os.path.join(db_dir, db_name)
    return db_file + '.lock'


def init_db(func):

    def init_db_wrapper(*args, **kwargs):
        if not os.path.exists(db_dir):
            os.mkdir(db_dir)
        for db in dbs:
            if not os.path.exists(db):
                with open(db, 'w') as (db_file):
                    json.dump([], db_file, indent=4)

        return func(*args, **kwargs)

    return init_db_wrapper


@init_db
def update_db(content, db_name):
    with FileLock(get_db_lockfile(db_name)).acquire(timeout=settings.LOCK_TIMEOUT):
        db_file = os.path.join(db_dir, db_name)
        with open(db_file, 'w') as (db):
            json.dump(content, db, indent=4)


@init_db
def get_db(db_name):
    with FileLock(get_db_lockfile(db_name)).acquire(timeout=settings.LOCK_TIMEOUT):
        db_file = os.path.join(db_dir, db_name)
        with open(db_file, 'r') as (db):
            return json.load(db)


def del_db(db_name):
    with FileLock(get_db_lockfile(db_name)).acquire(timeout=settings.LOCK_TIMEOUT):
        db_file = os.path.join(db_dir, db_name)
        if os.path.exists(db_file):
            os.remove(db_file)