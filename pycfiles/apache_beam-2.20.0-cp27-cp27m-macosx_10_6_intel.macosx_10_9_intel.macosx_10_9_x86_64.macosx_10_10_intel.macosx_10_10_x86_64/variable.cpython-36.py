# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/models/variable.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 5103 bytes
import json
from builtins import bytes
from typing import Any
from sqlalchemy import Column, Integer, String, Text, Boolean
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import synonym
from airflow.models.base import Base, ID_LEN
from airflow.models.crypto import get_fernet, InvalidFernetToken
from airflow.utils.db import provide_session
from airflow.utils.log.logging_mixin import LoggingMixin

class Variable(Base, LoggingMixin):
    __tablename__ = 'variable'
    _Variable__NO_DEFAULT_SENTINEL = object()
    id = Column(Integer, primary_key=True)
    key = Column((String(ID_LEN)), unique=True)
    _val = Column('val', Text)
    is_encrypted = Column(Boolean, unique=False, default=False)

    def __repr__(self):
        return '{} : {}'.format(self.key, self._val)

    def get_val(self):
        log = LoggingMixin().log
        if self._val:
            if self.is_encrypted:
                try:
                    fernet = get_fernet()
                    return fernet.decrypt(bytes(self._val, 'utf-8')).decode()
                except InvalidFernetToken:
                    log.error("Can't decrypt _val for key={}, invalid token or value".format(self.key))
                    return
                except Exception:
                    log.error("Can't decrypt _val for key={}, FERNET_KEY configuration missing".format(self.key))
                    return

        else:
            return self._val

    def set_val(self, value):
        if value:
            fernet = get_fernet()
            self._val = fernet.encrypt(bytes(value, 'utf-8')).decode()
            self.is_encrypted = fernet.is_encrypted

    @declared_attr
    def val(cls):
        return synonym('_val', descriptor=(property(cls.get_val, cls.set_val)))

    @classmethod
    def setdefault(cls, key, default, deserialize_json=False):
        """
        Like a Python builtin dict object, setdefault returns the current value
        for a key, and if it isn't there, stores the default value and returns it.

        :param key: Dict key for this Variable
        :type key: str
        :param default: Default value to set and return if the variable
            isn't already in the DB
        :type default: Mixed
        :param deserialize_json: Store this as a JSON encoded value in the DB
            and un-encode it when retrieving a value
        :return: Mixed
        """
        obj = Variable.get(key, default_var=None, deserialize_json=deserialize_json)
        if obj is None:
            if default is not None:
                Variable.set(key, default, serialize_json=deserialize_json)
                return default
            raise ValueError('Default Value must be set')
        else:
            return obj

    @classmethod
    @provide_session
    def get(cls, key, default_var=_Variable__NO_DEFAULT_SENTINEL, deserialize_json=False, session=None):
        obj = session.query(cls).filter(cls.key == key).first()
        if obj is None:
            if default_var is not cls._Variable__NO_DEFAULT_SENTINEL:
                return default_var
            raise KeyError('Variable {} does not exist'.format(key))
        else:
            if deserialize_json:
                return json.loads(obj.val)
            else:
                return obj.val

    @classmethod
    @provide_session
    def set(cls, key, value, serialize_json=False, session=None):
        if serialize_json:
            stored_value = json.dumps(value, indent=2, separators=(',', ': '))
        else:
            stored_value = str(value)
        Variable.delete(key)
        session.add(Variable(key=key, val=stored_value))
        session.flush()

    @classmethod
    @provide_session
    def delete(cls, key, session=None):
        session.query(cls).filter(cls.key == key).delete()

    def rotate_fernet_key(self):
        fernet = get_fernet()
        if self._val:
            if self.is_encrypted:
                self._val = fernet.rotate(self._val.encode('utf-8')).decode()