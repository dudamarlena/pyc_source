# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/projects_base/base/models.py
# Compiled at: 2020-04-25 05:24:47
# Size of source mod 2**32: 4485 bytes
import shelve, uuid, fnmatch, fcntl, operator
from projects_base.base import config

class ShelveObject:

    def __init__(self):
        self._id = str(uuid.uuid4())
        self._type = str(type(self))

    def serialize(self):
        return self.__dict__

    def items(self):
        return self.__dict__.items()

    def save(self):
        with open(config.get('BASE', 'db_lock'), 'wb') as (lock):
            fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
            with shelve.open(config.get('BASE', 'db_path')) as (db):
                db[self._id] = {key:self.__dict__[key] for key in self.__dict__.keys()}
            fcntl.flock(lock.fileno(), fcntl.LOCK_UN)
        return self._id

    @classmethod
    def get(cls, instance_id):
        _object = None
        try:
            with shelve.open(config.get('BASE', 'db_path')) as (db):
                _object = cls(**db[instance_id])
        except KeyError:
            pass

        return _object

    @classmethod
    def get_all(cls):
        ids = []
        with shelve.open(config.get('BASE', 'db_path')) as (db):
            ids = [key for key in db.keys() if db[key]['_type'] == str(cls)]
        return [cls.get(instance_id) for instance_id in ids]

    @classmethod
    def remove(cls, shelve_id):
        with open(config.get('BASE', 'db_lock'), 'wb') as (lock):
            fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
            with shelve.open(config.get('BASE', 'db_path')) as (db):
                db.pop(shelve_id)
            fcntl.flock(lock.fileno(), fcntl.LOCK_UN)

    @classmethod
    def clear(cls):
        for instance in cls.get_all():
            cls.remove(instance._id)

    @classmethod
    def get_with_attr(cls, attr, value, collection=None):
        result = []
        if not collection:
            collection = cls.get_all()
        for obj in collection:
            if hasattr(obj, attr):
                obj_attr = getattr(obj, attr)
                if isinstance(obj_attr, type(value)):
                    if obj_attr == value:
                        result.append(obj)
                if isinstance(obj_attr, (list, set, tuple, dict)) and value in obj_attr:
                    result.append(obj)

        return result

    @classmethod
    def get_with_search(cls, key, value, collection=None):
        result = []
        search = '*' + value + '*'
        if not collection:
            collection = cls.get_all()
        for obj in collection:
            if hasattr(obj, key) and len(fnmatch.filter([obj.__dict__[key].lower()], search.lower())) > 0:
                result.append(obj)

        return result

    @classmethod
    def get_with_first(cls, key, value, collection=None):
        if not collection:
            collection = cls.get_all()
        for obj in collection:
            if hasattr(obj, key):
                if obj.__dict__[key] == value:
                    return obj

    @classmethod
    def get_top_with(cls, key, collection=None, num=10):
        if not collection:
            collection = cls.get_all()
        distinct_count = {}
        for obj in collection:
            if hasattr(obj, key):
                struct = obj.__dict__[key]
                distinct_count.update(count_distinct_in(struct, distinct_count))

        top_num = dict(sorted((distinct_count.items()), key=(operator.itemgetter(1)), reverse=True)[:num])
        return top_num


def count_distinct_in(struct, current_count=None):
    if not current_count:
        current_count = {}
    else:
        if isinstance(struct, str):
            if struct not in current_count:
                current_count[struct] = 1
            else:
                current_count[struct] += 1
        if isinstance(struct, list):
            for i in struct:
                return count_distinct_in(i, current_count)

        if isinstance(struct, dict):
            for k, v in struct.items():
                return count_distinct_in(k, current_count)

    return current_count