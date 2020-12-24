# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/haplugin/sql/driver.py
# Compiled at: 2015-05-19 02:58:44
# Size of source mod 2**32: 1096 bytes
from sqlalchemy.orm.exc import NoResultFound

class Driver(object):

    def __init__(self, db):
        self.db = db

    def add_group(self, group):
        setattr(self, group.name, group)
        group.init(self.db)


class DriverGroup(object):

    def init(self, db):
        self.db = db
        self.query = db.query


class SqlDriver(DriverGroup):

    def upsert(self, **kwargs):
        try:
            return self.query(self.model).filter_by(**kwargs).one()
        except NoResultFound:
            return self.create(**kwargs)

    def get_by_id(self, id):
        return self.find_all().filter_by(id=id).one()

    def find_all(self):
        return self.query(self.model)

    def find_by(self, **kwargs):
        return self.query(self.model).filter_by(**kwargs)

    def create(self, **kwargs):
        obj = self.model()
        for key, value in kwargs.items():
            setattr(obj, key, value)

        self.db.add(obj)
        return obj

    def delete_by_id(self, id_):
        self.delete(self.get_by_id(id_))

    def delete(self, obj):
        self.db.delete(obj)