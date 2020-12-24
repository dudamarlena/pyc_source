# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/stephenmoore/Projects/utility/photons-interactor/photons_interactor/database/connection.py
# Compiled at: 2020-02-25 22:11:59
# Size of source mod 2**32: 8341 bytes
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy import create_engine, orm
from sqlalchemy import Column, Integer
import sqlalchemy, logging
log = logging.getLogger('photons_interactor.database.connection')

class Base(object):
    metadata = None
    __repr_columns__ = None

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)

    def __repr__(self):
        title = self.__tablename__
        cols = dict(((key, getattr(self, key)) for key in self.__repr_columns__))
        columns = ', '.join(('%s:%s' % (key, value) for key, value in cols.items()))
        return '<%s (%s)>' % (title, columns)


Base = declarative_base(cls=Base)

class DatabaseConnection(object):
    __doc__ = '\n    The wrapper to sqlalchemy for interacting with the database. Usage looks like:\n\n    .. code-block:: python\n\n        conn = DatabaseConnection(database_uri)\n        with conn.new_session() as db:\n            try:\n                # Do something with the db\n                db.commit()\n            except:\n                db.rollback()\n\n    The db object has a ``session`` attribute that is an instance of a\n    sqlalchemy session (http://docs.sqlalchemy.org/en/latest/orm/session_basics.html)\n\n    The db object also forwards the following properties to that session:\n    ``query``, ``rollback``, ``commit``, ``merge``, ``add``, ``delete``\n    , ``refresh`` and ``execute``.\n\n    So you can do something like:\n\n    .. code-block:: python\n\n        thing = Thing(luid="asdf", serial="adf")\n        db.add(thing)\n        db.commit()\n\n    As a bonus, we also have an instance of ``photons_interactor.database.connection.QueryHelper`` on\n    ``db.queries`` so you can do the above with:\n\n    .. code-block:: python\n\n        db.add(db.queries.create_thing(luid="adf", serial=\'adf"))\n        db.commit()\n    '

    def __init__(self, database=None, engine=None, **engine_kwargs):
        self.database = database
        self.engine = engine
        self.engine_kwargs = engine_kwargs
        if self.engine is None:
            self.engine = (self.create_engine)(database, **self.engine_kwargs)
        self.queries = QueryHelper(self)

    def create_engine(self, database, **engine_kwargs):
        if not database:
            database = 'sqlite:///:memory:'
        return create_engine(database, **engine_kwargs)

    def new_session(self):
        dc = (self.__class__)(database=self.database, engine=self.engine, **self.engine_kwargs)
        dc.session = dc.make_session()
        return dc

    @property
    def query(self):
        return self.session.query

    @property
    def rollback(self):
        return self.session.rollback

    @property
    def commit(self):
        return self.session.commit

    @property
    def merge(self):
        return self.session.merge

    @property
    def add(self):
        return self.session.add

    @property
    def delete(self):
        return self.session.delete

    @property
    def refresh(self):
        return self.session.refresh

    @property
    def execute(self):
        return self.session.execute

    def make_session(self):
        return orm.sessionmaker(bind=(self.engine))()

    def drop_all(self):
        try:
            Base.metadata.drop_all(self.engine)
        except sqlalchemy.exc.OperationalError as error:
            try:
                log.exception(error)
            finally:
                error = None
                del error

    def create_tables(self):
        self.drop_all()
        Base.metadata.create_all(self.engine)

    def expire_all(self):
        self.session.expire_all()

    def dispose(self):
        if self.engine:
            self.engine.dispose()

    def close(self):
        if self.engine:
            self.dispose()
        if hasattr(self, 'session'):
            self.session.close()


class QueryHelper(object):
    __doc__ = '\n    Object to abstract getting stuff from the database\n\n    Essentially you do stuff via the special __getattr__:\n\n    .. automethod:: photons_interactor.database.connection.QueryHelper.__getattr__\n    '

    def __init__(self, db):
        self.db = db

    @property
    def session(self):
        return self.db.session

    def __getattr__(self, key):
        """
        Custom getattr to get

        get_<ModelName>
            Finds first model with provided keyword attributes

        get_<ModelName>s
            Finds all model with provided keyword attributes

        get_one_<ModelName>
            Find the only model with provided keyword attributes

        create_<ModelName>
            Create this model

        get_or_create_<ModelName>
            Finds first model with provided keyword attributes or creates one.
        """
        if key.startswith('_') or key in self.__dict__:
            return object.__getattribute__(self, key)
        if key.startswith('get_') or key.startswith('create_') or key.startswith('count_'):
            if key.startswith('count_'):
                name = key[6:]
                action = 'count_model'
            else:
                if key.startswith('create_'):
                    name = key[7:]
                    action = 'create_model'
                else:
                    if key.startswith('get_one_'):
                        name = key[7:]
                        action = 'get_one_model'
                    else:
                        if key.startswith('get_or_create_'):
                            name = key[14:]
                            action = 'get_or_create_model'
                        else:
                            name = key[4:]
                            if name.endswith('s'):
                                name = name[:-1]
                                action = 'get_models'
                            else:
                                action = 'get_model'
            model_name = self.clean_name(name)
            if model_name.lower() not in Base.metadata.tables:
                raise AttributeError('No such table as %s' % model_name)

            def getter(**attrs):
                model = Base._decl_class_registry[model_name]
                return object.__getattribute__(self, action)(model, attrs)

            return getter
        return object.__getattribute__(self, key)

    def count_model(self, model, attrs, **kwargs):
        return (self.filtered)(model, attrs, **kwargs).count()

    def get_model(self, model, attrs, **kwargs):
        return (self.filtered)(model, attrs, **kwargs).first()

    def get_models(self, model, attrs, limit=None, **kwargs):
        fltrd = (self.filtered)(model, attrs, **kwargs)
        if limit:
            fltrd = fltrd.limit(limit)
        return fltrd

    def get_one_model(self, model, attrs, **kwargs):
        return (self.filtered)(model, attrs, **kwargs).one()

    def get_or_create_model(self, model, attrs, **kwargs):
        found = (self.get_model)(model, attrs, **kwargs)
        if not found:
            return (
             model(**attrs), True)
        return (found, False)

    def create_model(self, model, attrs):
        return model(**attrs)

    def clean_name(self, name):
        return ''.join((part.capitalize() for part in name.split('_')))

    def make_filters(self, model, attrs):
        filters = []
        for key, val in attrs.items():
            filters.append(getattr(model, key) == val)

        return filters

    def filtered(self, model, attrs, for_update=False, skip_locked=True):
        filters = self.make_filters(model, attrs) if type(attrs) is dict else attrs
        query = self.session.query(model)
        if for_update:
            query = query.with_for_update(skip_locked=skip_locked)
        return (query.filter)(*filters)