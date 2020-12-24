# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/phouse/phouse.py
# Compiled at: 2019-10-15 11:31:38
# Size of source mod 2**32: 11668 bytes
import pandas as pd
from clickhouse_driver import Client
import sys, time

@pd.api.extensions.register_dataframe_accessor('clickhouse')
class Clickhouse:
    ENGINE_CODE = None
    CREATE_SQL = None
    DATE_COLUMN = None
    COLUMN_LIST = None
    DATA_FRAME = None
    MAPPING = {'int8':"Int8 default CAST(0, 'Int8')", 
     'int16':"Int16 default CAST(0, 'Int16')", 
     'int32':"Int32 default CAST(0, 'Int32')", 
     'int64':"Int64 default CAST(0, 'Int64')", 
     'float32':"Float32 default CAST(0, 'Float32')", 
     'float64':"Float64 default CAST(0, 'Float64')", 
     'object':'String', 
     'datetime64[ns]':'DateTime default today()'}

    def __init__(self, pandas_obj):
        self._validate(pandas_obj)
        self._obj = pandas_obj

    def MergeTree(self, PARTITION=None, ORDER_BY=None, INDEX_GRANULARITY=None):
        if PARTITION is None:
            raise Exception('Не определена партиция')
        else:
            if ORDER_BY is None:
                raise Exception('Не определена сортировка')
            if INDEX_GRANULARITY is None:
                raise Exception('Не определен тип интекса')
        engine_code = ('  \n            engine = MergeTree() \n            PARTITION BY {PARTITION} \n            ORDER BY {ORDER_BY} \n            SETTINGS index_granularity = {INDEX_GRANULARITY};  \n            '.format)(PARTITION=PARTITION, 
         ORDER_BY=ORDER_BY, 
         INDEX_GRANULARITY=INDEX_GRANULARITY)
        self.ENGINE_CODE = engine_code

    def ReplacingMergeTree(self, PARTITION=None, ORDER_BY=None, INDEX_GRANULARITY=None, VER=None):
        if PARTITION is None:
            raise Exception('Не определена партиция')
        else:
            if ORDER_BY is None:
                raise Exception('Не определена сортировка')
            if INDEX_GRANULARITY is None:
                raise Exception('Не определен тип интекса')
        engine_code = ('  \n            engine = ReplacingMergeTree({VER}) \n            PARTITION BY {PARTITION} \n            ORDER BY {ORDER_BY} \n            SETTINGS index_granularity = {INDEX_GRANULARITY};  \n            '.format)(PARTITION=PARTITION, 
         ORDER_BY=ORDER_BY, 
         INDEX_GRANULARITY=INDEX_GRANULARITY, 
         VER=self.NoneToStr(VER))
        self.ENGINE_CODE = engine_code

    def SummingMergeTree(self, PARTITION=None, ORDER_BY=None, INDEX_GRANULARITY=None, COLUMNS=None):
        if PARTITION is None:
            raise Exception('Не определена партиция')
        elif ORDER_BY is None:
            raise Exception('Не определена сортировка')
        else:
            if INDEX_GRANULARITY is None:
                raise Exception('Не определен тип интекса')
            if COLUMNS is None or COLUMNS == []:
                raise Exception('Необходимо указать коллонки суммирования')
            elif not isinstance(COLUMNS, list):
                raise Exception('Тип переменной COLUMNS должна быть списком')
        engine_code = ('  \n            engine = SummingMergeTree(COLUMNS)  \n            PARTITION BY {PARTITION} \n            ORDER BY {ORDER_BY} \n            SETTINGS index_granularity = {INDEX_GRANULARITY};  \n            '.format)(PARTITION=PARTITION, 
         ORDER_BY=ORDER_BY, 
         INDEX_GRANULARITY=INDEX_GRANULARITY, 
         COLUMNS=COLUMNS)
        self.ENGINE_CODE = engine_code

    def AggregatingMergeTree(self, PARTITION=None, ORDER_BY=None, INDEX_GRANULARITY=None):
        if PARTITION is None:
            raise Exception('Не определена партиция')
        else:
            if ORDER_BY is None:
                raise Exception('Не определена сортировка')
            if INDEX_GRANULARITY is None:
                raise Exception('Не определен тип интекса')
        engine_code = ('  \n            engine = AggregatingMergeTree() \n            PARTITION BY {PARTITION} \n            ORDER BY {ORDER_BY}  \n            SETTINGS index_granularity = {INDEX_GRANULARITY};  \n            '.format)(PARTITION=PARTITION, 
         ORDER_BY=ORDER_BY, 
         INDEX_GRANULARITY=INDEX_GRANULARITY)
        self.ENGINE_CODE = engine_code

    def CollapsingMergeTree(self, SIGN=None, PARTITION=None, ORDER_BY=None, INDEX_GRANULARITY=None):
        if PARTITION is None:
            raise Exception('Не определена партиция')
        else:
            if ORDER_BY is None:
                raise Exception('Не определена сортировка')
            if INDEX_GRANULARITY is None:
                raise Exception('Не определен тип интекса')
        self.COLUMN_LIST.update({SIGN: ' "{}" Int8 default 1  '.format(SIGN)})
        engine_code = ('  \n            engine = CollapsingMergeTree({SIGN})  \n            PARTITION BY {PARTITION} \n            ORDER BY {ORDER_BY} \n            SETTINGS index_granularity = {INDEX_GRANULARITY};  \n            '.format)(PARTITION=PARTITION, 
         ORDER_BY=ORDER_BY, 
         INDEX_GRANULARITY=INDEX_GRANULARITY, 
         SIGN=SIGN)
        self.ENGINE_CODE = engine_code

    def VersionedCollapsingMergeTree(self, SIGN=None, VERSION=None, PARTITION=None, ORDER_BY=None, INDEX_GRANULARITY=None):
        if PARTITION is None:
            raise Exception('Не определена партиция')
        else:
            if ORDER_BY is None:
                raise Exception('Не определена сортировка')
            if INDEX_GRANULARITY is None:
                raise Exception('Не определен тип интекса')
        self.COLUMN_LIST.update({SIGN: ' "{}" Int8 default 1  '.format(SIGN)})
        self.COLUMN_LIST.update({VERSION: ' "{}" UInt64  '.format(VERSION)})
        engine_code = ('  \n            engine = VersionedCollapsingMergeTree({SIGN}, {VERSION}) \n            PARTITION BY {PARTITION} \n            ORDER BY {ORDER_BY} \n            SETTINGS index_granularity = {INDEX_GRANULARITY};  \n            '.format)(PARTITION=PARTITION, 
         ORDER_BY=ORDER_BY, 
         INDEX_GRANULARITY=INDEX_GRANULARITY, 
         SIGN=SIGN, 
         VERSION=VERSION)
        self.ENGINE_CODE = engine_code

    @classmethod
    def _validate(cls, obj):
        cls.DATA_FRAME = obj
        cls.COLUMN_LIST = {}
        for c in obj.columns:
            if str(obj[c].dtype) == 'datetime64[ns]':
                cls.DATE_COLUMN = c
            cls.COLUMN_LIST[c] = '"{0}" {1}'.format(c, cls.MAPPING[str(obj[c].dtype)])

    def createTable(self, table):
        if self.ENGINE_CODE is None:
            CREATE_SQL = ('\n                create table {table_name}\n                (\n                   {columns} \n                )\n                  engine = MergeTree() PARTITION BY toYYYYMM({date_column}) \n                  ORDER BY {date_column} SETTINGS index_granularity = 8192; \n            '.format)(table_name=table, 
             columns=',\n'.join(list(self.COLUMN_LIST.values())), 
             date_column=self.DATE_COLUMN)
        else:
            CREATE_SQL = ('\n                            create table {table_name}\n                            (\n                               {columns} \n                            )\n                            {engine_code}\n            '.format)(table_name=table, 
             columns=',\n'.join(list(self.COLUMN_LIST.values())), 
             engine_code=self.ENGINE_CODE)
        self.CREATE_SQL = CREATE_SQL
        try:
            pd.clickhouse_client.execute(CREATE_SQL, with_column_types=True)
        except Exception as e:
            print(e)

    def write(self, table):
        while True:
            try:
                self.createTable(table)
                self.truncate(table=table)
                pd.clickhouse_client.execute('INSERT INTO {0} ({1}) VALUES'.format(table, ','.join(['"{}"'.format(x) for x in Clickhouse.DATA_FRAME.columns])), self.DATA_FRAME.to_dict('records'))
                break
            except:
                print('error query {0} . try again after {1} second'.format(sys.exc_info()[0], 60))
                time.sleep(60)

    def append(self, table):
        while True:
            try:
                self.createTable(table)
                pd.clickhouse_client.execute('INSERT INTO {0} ({1}) VALUES'.format(table, ','.join(['"{}"'.format(x) for x in self.DATA_FRAME.columns])), self.DATA_FRAME.to_dict('records'))
                break
            except:
                print('error query {0} . try again after {1} second'.format(sys.exc_info()[0], 60))
                time.sleep(60)

    def drop(self, table):
        try:
            pd.clickhouse_client.execute('DROP TABLE {}'.format(table))
        except:
            print(' не удалено! возможно таблицы c таким именем не существует ')

    def truncate(self, table):
        try:
            pd.clickhouse_client.execute('TRUNCATE TABLE {}'.format(table))
        except:
            print(' Не удалось почистить таблицу возможно она была удалена или вовсе не создана ')

    def NoneToStr(self, x):
        if x is None:
            return ''
        else:
            return x


class Phouse:

    @classmethod
    def getConnection(cls, options):
        import pandas as pd
        pd.clickhouse_client = Client((options['host']), user=(options['user']),
          password=(options['password']),
          port=(options['port']),
          secure=False,
          verify=False,
          database=(options['database']),
          connect_timeout=1200)

        def clickhouse_query(sql, repeat_interval=60):
            while True:
                try:
                    data = pd.clickhouse_client.execute(sql, with_column_types=True)
                    break
                except:
                    print('error query {0} . try again after {1} second'.format(sys.exc_info()[0], repeat_interval))
                    time.sleep(repeat_interval)

            return pd.DataFrame((data[0]), columns=[c[0] for c in data[1]])

        pd.clickhouse_query = clickhouse_query
        return pd