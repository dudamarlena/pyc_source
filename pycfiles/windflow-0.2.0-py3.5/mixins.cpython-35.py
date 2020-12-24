# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/windflow/models/mixins.py
# Compiled at: 2018-04-18 11:33:58
# Size of source mod 2**32: 1047 bytes
from sqlalchemy import Column, DateTime, Integer, String, func
from sqlalchemy.ext.declarative import declared_attr
from windflow.models.utils import Filter, Getter
from windflow.utils import generate_repr_method, generate_str_method

class TimestampableMixin:
    created_at = Column('created_at', DateTime, default=func.now())
    updated_at = Column('updated_at', DateTime, default=func.now(), onupdate=func.now())


class TextDimensionMixin:
    __doc__ = '\n    Generic model mixin used to build text dimension models.\n    '
    id = Column(Integer, primary_key=True)
    value = Column(String, unique=True)

    @declared_attr
    def __tablename__(cls):
        return 'dim_' + cls.__name__.lower()

    @Getter(Filter('value', str))
    def get(cls, session, filters):
        return session.query(cls).filter_by(**filters).first()

    __str__ = generate_str_method('value')
    __repr__ = generate_repr_method('value')