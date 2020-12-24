# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/commonslib/database.py
# Compiled at: 2015-04-04 05:19:06
__doc__ = '\nCreated on 2014-10-29\nA lightweight wrapper around SQLAlchemy.\nauthor: huwei\n'
from contextlib import contextmanager
import functools, inflection
from app.services.base_service import ServiceException
from sqlalchemy import engine_from_config, func
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy.orm import sessionmaker, scoped_session
from app.commons import dateutil
from decorated.base.dict import Dict
__author__ = 'huwei'

class ModelBase(object):

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, self.fields)

    def __json__(self):
        return self.fields

    @property
    def fields(self):
        d = Dict()
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)

        return d

    @property
    def keys(self):
        columns = self.__table__.primary_key.columns
        return tuple([ getattr(self, c.name) for c in columns ])

    def update(self, fields):
        for column in self.__table__.columns:
            if column.name in fields:
                setattr(self, column.name, fields[column.name])


class AutoTableNameMeta(DeclarativeMeta):

    def __init__(cls, classname, bases, dict_):
        cls.__tablename__ = inflection.pluralize(inflection.underscore(classname))
        DeclarativeMeta.__init__(cls, classname, bases, dict_)


def create_model_base(**options):
    options.setdefault('cls', ModelBase)
    options.setdefault('metaclass', AutoTableNameMeta)
    return declarative_base(**options)


BaseModel = create_model_base()

class DatabaseFactory(object):

    def __init__(self, **kwargs):
        self._engine = engine_from_config(kwargs, prefix='')
        self._session = scoped_session(sessionmaker(bind=self._engine))

    @contextmanager
    def create_session(self):
        """Provide a transactional scope around a series of operations."""
        session = self._session()
        try:
            try:
                yield session
                session.commit()
            except Exception as e:
                if isinstance(e, ServiceException):
                    session.commit()
                    raise e
                else:
                    session.rollback()
                    raise e

        finally:
            session.close()


def model(model_cls):

    def _model(cls):
        orig_init = cls.__init__

        @functools.wraps(cls)
        def __init__(self, *args, **kvargs):
            orig_init(self, *args, **kvargs)
            self.model_cls = model_cls

        cls.__init__ = __init__
        return cls

    return _model


class DatabaseTemplate(object):
    u""" 所有Dao对象需要集成DatabaseTemplate
    """

    def __init__(self, session):
        self.session = session
        self.model_cls = None
        return

    def get(self, identity):
        instance = self.session.query(self.model_cls).get(identity)
        if instance is None or hasattr(instance, 'is_deleted') and instance.is_deleted:
            return
        return instance
        return

    def get_first_by_criterion(self, *criterion):
        return self.session.query(self.model_cls).filter(*criterion).first()

    def gets_by_ids(self, ids):
        no_order_instances = self.session.query(self.model_cls).filter(self.model_cls.id.in_(ids)).all()
        inst_dict = dict()
        for instance in no_order_instances:
            inst_dict[instance.id] = instance

        instances = list()
        for identity in ids:
            instance = inst_dict.get(identity, None)
            if instance is not None:
                instances.append(instance)

        return instances

    def get_dict_by_ids(self, ids):
        instances = self.session.query(self.model_cls).filter(self.model_cls.id.in_(ids)).all()
        inst_dict = dict()
        for instance in instances:
            inst_dict[instance.id] = instance

        return inst_dict

    def count(self, *criterion):
        self.session.query(func.count('*')).select_from(self.model_cls).filter(*criterion).scalar()

    def add(self, instance):
        if hasattr(instance, 'created_at'):
            instance.created_at = dateutil.timestamp()
        if hasattr(instance, 'updated_at'):
            instance.updated_at = dateutil.timestamp()
        self.session.add(instance, _warn=True)
        self.session.flush([instance])
        return instance

    def add_all(self, instances):
        u"""插入所有
        :param instances: 多个实例对象
        """
        if instances is None or len(instances) == 0:
            return
        has_updated_at = hasattr(instances[0], 'updated_at')
        has_created_at = hasattr(instances[0], 'created_at')
        now = dateutil.timestamp() if has_updated_at or has_created_at else None
        for instance in instances:
            if has_updated_at:
                instance.updated_at = now
            if has_created_at:
                instance.created_at = now

        self.session.add_all(instances)
        self.session.flush(instances)
        return instances

    def update(self, instance):
        if hasattr(instance, 'updated_at'):
            instance.updated_at = dateutil.timestamp()
        self.session.merge(instance, load=True)
        self.session.flush([instance])
        return instance

    def update_all(self, instances):
        if instances is None or len(instances) == 0:
            return
        has_updated_at = hasattr(instances[0], 'updated_at')
        now = dateutil.timestamp() if has_updated_at else None
        for instance in instances:
            if has_updated_at:
                instance.updated_at = now
            self.session.merge(instance, load=True)

        self.session.flush(instances)
        return

    def delete_by_id(self, identity):
        instance = self.get(identity)
        if instance is not None:
            self.session.delete(instance)
            self.session.flush([instance])
        return

    def delete(self, instance):
        if instance is None:
            return
        else:
            if hasattr(instance, 'is_deleted'):
                instance.is_deleted = True
                self.session.merge(instance, load=True)
                self.session.flush([instance])
            else:
                self.session.delete(instance)
                self.session.flush([instance])
            return

    def _scalar(self, clause, params=None, mapper=None, bind=None, **kw):
        return self.session.scalar(clause, params=params, mapper=mapper, bind=bind, **kw)

    def _execute(self, clause, params=None, mapper=None, bind=None, **kw):
        return self.session.execute(clause, params=params, mapper=mapper, bind=bind, **kw)

    def _query(self, *entities, **kwargs):
        return self.session.query(*entities, **kwargs)

    def _add(self, instance, _warn=True):
        return self.session.add(instance, _warn=_warn)

    def _add_all(self, instances):
        return self.session.add_all(instances)

    def _delete(self, instance):
        return self.session.delete(instance)

    def _merge(self, instance, load=True):
        return self.session.merge(instance, load)

    def _flush(self, objects):
        return self.session.flush(objects)

    def _refresh(self, instance, attribute_names=None, lockmode=None):
        return self.session.refresh(self, instance, attribute_names=attribute_names, lockmode=lockmode)