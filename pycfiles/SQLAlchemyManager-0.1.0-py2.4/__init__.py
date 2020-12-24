# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/sqlalchemymanager/__init__.py
# Compiled at: 2007-11-08 07:34:12
"""SQLAlchemyManager - Provides a sensible way of using SQLAlchemy in WSGI applications 
"""
from sqlalchemy.orm import sessionmaker
from sqlalchemy import engine_from_config, MetaData
from sqlalchemy import Table
from sqlalchemy.orm import mapper

class Model(dict):
    """    A dictionary like object where keys can also be accessed as attributes.
    """
    __module__ = __name__

    def __getattr__(self, key):
        return self.__getitem__(key)

    def __setattr__(self, key, value):
        return self.__setitem__(key, value)


class SQLAlchemyManager(object):
    """    Really simple SQLAlchemy middleware
    which also helps in setting up the model and provides sensible access to 
    key SQLAlchmey objects
    """
    __module__ = __name__

    def __init__(self, app, app_conf, fns=[]):
        self.metadata = MetaData()
        self.model = Model()
        for fn in fns:
            model_dict = fn(self.model, self.metadata)
            if isinstance(model_dict, dict):
                for (k, v) in model_dict:
                    if self.model.has_key(k):
                        raise Exception('The model already has an object named %s' % k)
                    self.model[k] = v

            elif model_dict is not None:
                raise Exception('Function %s returned %s, expected a dictionary or None' % (fn, model_dict))

        self.config = app_conf
        self.engine = engine_from_config(self.config, 'sqlalchemy.')
        self.session_maker = sessionmaker(autoflush=True, transactional=True)
        self.app = app
        return

    def create_all(self):
        """        Create all the required tables
        """
        self.metadata.create_all(bind=self.engine)

    def __call__(self, environ, start_response):
        connection = self.engine.connect()
        session = self.session_maker(bind=connection)
        environ['sqlalchemy.manager'] = self
        environ['sqlalchemy.model'] = self.model
        environ['sqlalchemy.session'] = session
        try:
            return self.app(environ, start_response)
        finally:
            session.close()
            connection.close()


if __name__ == '__main__':
    from sqlalchemy import Table, Column, types
    from sqlalchemy.sql import select

    def setup_model(model, metadata, **p):
        model.table1 = Table('table1', metadata, Column('id', types.Integer, primary_key=True), Column('name', types.String, nullable=False))

        class MyClass(object):
            __module__ = __name__

        model.MyClass = MyClass
        model.table1_mapper = mapper(model.MyClass, model.table1)


    def app(environ, start_response):
        model = environ['sqlalchemy.model']
        session = environ['sqlalchemy.session']
        environ['sqlalchemy.manager'].create_all()
        select_statement = select([model.table1])
        select_result = [ row for row in session.execute(select_statement) ]
        mr_jones = model.MyClass()
        mr_jones.name = 'Mr Jones'
        session.save(mr_jones)
        session.commit()
        multiple_mr_jones = session.query(model.MyClass).filter(model.MyClass.name == 'Mr Jones').order_by(model.table1.c.name).all()
        start_response('200 OK', [('Content-Type', 'text/plain')])
        return ['\n    Select Result: \n    %s\n    \n    Mr Jones Results:\n    %s \n            ' % (select_result, (', ').join([ person.name for person in multiple_mr_jones ]))]


    app_conf = {'sqlalchemy.url': 'sqlite:///test.db', 'sqlalchemy.echo': 'false'}
    app = SQLAlchemyManager(app, app_conf, [setup_model])

    def printing_start_response(status, headers, exc_info=None):
        print 'Status: %s' % status
        print 'Headers: %s' % headers
        print 'Exc_info: %s' % exc_info
        print


    fake_environ = {}
    for output in app(fake_environ, printing_start_response):
        print output