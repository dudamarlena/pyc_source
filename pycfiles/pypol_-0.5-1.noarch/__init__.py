# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pp_sqlalchemy/__init__.py
# Compiled at: 2011-11-24 13:47:49
import pypoly
from pypoly.component import Component
__version__ = '0.2'

class Main(Component):

    def init(self):
        pypoly.config.add('database', '')
        pypoly.config.add('debug', False)
        pypoly.config.add('hostname', 'localhost')
        pypoly.config.add('password', '')
        pypoly.config.add('pool.max_size', 10)
        pypoly.config.add('pool.recycle', 3600)
        pypoly.config.add('pool.size', 5)
        pypoly.config.add('port', 5432)
        pypoly.config.add('type', 'postgres')
        pypoly.config.add('user', 'postgres')

    def start(self):
        pypoly.tool.register('db_sa', DB())


class DB(object):
    """
    This class handles the gloabl db connection.
    """

    def __init__(self):
        """
        initalize all values
        """
        self._connection_args = dict()
        self._connection_string = ''
        self.engine = None
        self.meta = None
        import sqlalchemy.pool as pool, sqlalchemy as sa
        db_type = pypoly.config.get('type')
        db_type = db_type.lower()
        if db_type == 'sqlite':
            self._connection_args = dict()
            self._connection_string = 'sqlite:///' + pypoly.config.get('database').strip()
            self.engine = sa.create_engine(self._connection_string, connect_args=self._connection_args, poolclass=pool.NullPool, echo=pypoly.config.get('debug'))
            self.meta = sa.MetaData(bind=self.engine)
            self.meta.reflect()
        elif db_type == 'mysql':
            self._connection_args = dict(host=pypoly.config.get('hostname'), port=pypoly.config.get('port'), database=pypoly.config.get('database'), user=pypoly.config.get('user'), password=pypoly.config.get('password'))
            self._connection_string = 'mysql+mysqldb://'
            self.engine = sa.create_engine(self._connection_string, connect_args=self._connection_args, poolclass=pool.QueuePool, max_overflow=pypoly.config.get('pool.max_size'), pool_size=pypoly.config.get('pool.size'), pool_recycle=pypoly.config.get('pool.recycle'), echo=pypoly.config.get('debug'))
            self.meta = sa.MetaData(bind=self.engine)
            self.meta.reflect()
        elif db_type == 'postgres':
            self._connection_args = dict(host=pypoly.config.get('hostname'), port=pypoly.config.get('port'), database=pypoly.config.get('database'), user=pypoly.config.get('user'), password=pypoly.config.get('password'))
            self._connection_string = 'postgres://'
            self.engine = sa.create_engine(self._connection_string, connect_args=self._connection_args, poolclass=pool.QueuePool, max_overflow=pypoly.config.get('pool.max_size'), pool_size=pypoly.config.get('pool.size'), echo=pypoly.config.get('debug'))
            self.meta = sa.MetaData(bind=self.engine)
            self.meta.reflect()
        else:
            pypoly.log.error('Unknown DB Type')
        return

    def connect(self):
        return self.engine.connect()