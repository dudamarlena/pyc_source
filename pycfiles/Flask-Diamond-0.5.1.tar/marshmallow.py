# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/idm/Work/flask-diamond/flask_diamond/mixins/marshmallow.py
# Compiled at: 2016-12-30 20:14:37
from ..facets.database import db

class MarshmallowMixin:

    def dump(self):
        """serialize the Model object as a python object"""
        return self.__schema__().dump(self).data

    def dumps(self):
        """serialize the Model object as a JSON string"""
        return self.__schema__().dumps(self).data

    def dumpf(self, file_handle):
        """write a Model object to file_handle as a JSON string"""
        file_handle.write(self.dumps())

    @classmethod
    def load(cls, python_obj):
        """create a Model object from a python object"""
        obj = cls.__schema__().load(python_obj)
        return cls.create(**obj.data)

    @classmethod
    def loads(cls, buf):
        """create a Model object from a JSON-encoded string"""
        obj = cls.__schema__().loads(buf)
        return cls.create(**obj.data)

    @classmethod
    def loadf(cls, file_handle):
        """create a Model object from a file_handle pointing to a JSON file"""
        return cls.loads(file_handle.read())

    @classmethod
    def dump_all(cls):
        """write all objects of Model class to an array of python objects"""
        return cls.__schema__().dump(cls.query.all(), many=True).data

    @classmethod
    def dumps_all(cls):
        """write all objects of Model class to a JSON-encoded array"""
        return cls.__schema__().dumps(cls.query.all(), many=True).data

    @classmethod
    def dumpf_all(cls, file_handle):
        """write all objects of Model class to file_handle as JSON"""
        file_handle.write(cls.dumps_all())

    @classmethod
    def load_all(cls, python_objects):
        """create objects of Model class from an array of python objects"""
        objs = cls.__schema__().load(python_objects, many=True)
        for obj in objs.data:
            cls.create(_commit=False, **obj)

        db.session.commit()
        db.session.flush()

    @classmethod
    def loads_all(cls, buf):
        """create objects of Model class from a string containing an array of JSON-encoded objects"""
        objs = cls.__schema__().loads(buf, many=True)
        for obj in objs.data:
            cls.create(_commit=False, **obj)

        db.session.commit()
        db.session.flush()

    @classmethod
    def loadf_all(cls, file_handle):
        """create objects of Model class from a file containing an array of JSON-encoded objects"""
        cls.loads_all(file_handle.read())