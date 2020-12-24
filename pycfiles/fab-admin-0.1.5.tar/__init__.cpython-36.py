# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: e:\opt\private\cw1427\fab-admin\fab_admin\fab_manager_overwrite\flask_appbuilder/models/sqla/__init__.py
# Compiled at: 2019-03-06 02:56:37
# Size of source mod 2**32: 2668 bytes
import logging, re, datetime
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy, DefaultMeta, _QueryProperty
try:
    from sqlalchemy.ext.declarative import as_declarative
except ImportError:
    from sqlalchemy.ext.declarative.api import as_declarative

try:
    from sqlalchemy.orm.util import identity_key
    has_identity_key = True
except ImportError:
    has_identity_key = False

log = logging.getLogger(__name__)
_camelcase_re = re.compile('([A-Z]+)(?=[a-z0-9])')

class SQLA(SQLAlchemy):
    __doc__ = "\n        This is a child class of flask_SQLAlchemy\n        It's purpose is to override the declarative base of the original\n        package. So that it is bound to F.A.B. Model class allowing the dev\n        to be in the same namespace of the security tables (and others)\n        and can use AuditMixin class alike.\n\n        Use it and configure it just like flask_SQLAlchemy\n    "

    def make_declarative_base(self, model, metadata=None):
        base = Model
        base.query = _QueryProperty(self)
        return base

    def get_tables_for_bind(self, bind=None):
        """Returns a list of all tables relevant for a bind."""
        result = []
        tables = Model.metadata.tables
        for key in tables:
            if tables[key].info.get('bind_key') == bind:
                result.append(tables[key])

        return result


class ModelDeclarativeMeta(DefaultMeta):
    __doc__ = '\n        Base Model declarative meta for all Models definitions.\n        Setups bind_keys to support multiple databases.\n        Setup the table name based on the class camelcase name.\n    '


@as_declarative(name='Model', metaclass=ModelDeclarativeMeta)
class Model(object):
    __doc__ = '\n        Use this class has the base for your models, it will define your table names automatically\n        MyModel will be called my_model on the database.\n\n        ::\n\n            from sqlalchemy import Table, Column, Integer, String, Boolean, ForeignKey, Date\n            from flask_appbuilder import Model\n\n            class MyModel(Model):\n                id = Column(Integer, primary_key=True)\n                name = Column(String(50), unique = True, nullable=False)\n\n    '
    __table_args__ = None

    def to_json(self):
        result = dict()
        for key in self.__mapper__.c.keys():
            col = getattr(self, key)
            if isinstance(col, datetime.datetime) or isinstance(col, datetime.date):
                col = col.isoformat()
            result[key] = col

        return result


Base = Model