# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rachelle2/webprojects/toucan-connectors/toucan_connectors/mysql/mysql_connector.py
# Compiled at: 2020-04-08 11:34:17
# Size of source mod 2**32: 15815 bytes
import re
from typing import Optional
import numpy as np, pandas as pd, pymysql
from pydantic import Field, SecretStr, constr, create_model
from pymysql.constants import CR, ER
from toucan_connectors.toucan_connector import ToucanConnector, ToucanDataSource, strlist_to_enum

class MySQLDataSource(ToucanDataSource):
    __doc__ = '\n    Either `query` or `table` are required, both at the same time are not supported.\n    '
    database = Field(..., description='The name of the database you want to query')
    database: str
    table = Field(None,
      description='The name of the data table that you want to get (equivalent to "SELECT * FROM your_table")')
    table: constr(min_length=1)
    query = Field(None,
      description='You can write a custom query against your database here. It will take precedence over the "table" parameter above',
      widget='sql')
    query: constr(min_length=1)
    follow_relations = Field(False,
      description='Whether you want to perform automatic inner joins of related tables based on every foreign key found in the queried table (left table of the join). As a general rule, you should not need to activate this parameter')
    follow_relations: bool

    def __init__(self, **data):
        (super().__init__)(**data)
        query = data.get('query')
        table = data.get('table')
        if query is None and table is None:
            raise ValueError("'query' or 'table' must be set")
        else:
            if query is not None and table is not None:
                raise ValueError("Only one of 'query' or 'table' must be set")

    @classmethod
    def get_form(cls, connector: 'MySQLConnector', current_config):
        """
        Method to retrieve the form with a current config
        For example, once the connector is set,
        - we are able to give suggestions for the `database` field
        - if `database` is set, we are able to give suggestions for the `table` field
        """
        connection = (pymysql.connect)(**connector.get_connection_params(cursorclass=None,
          database=(current_config.get('database'))))
        constraints = {}
        with connection.cursor() as (cursor):
            cursor.execute('SHOW DATABASES;')
            res = cursor.fetchall()
            available_dbs = [db_name for db_name, in res]
            constraints['database'] = strlist_to_enum('database', available_dbs)
            if 'database' in current_config:
                cursor.execute('SHOW TABLES;')
                res = cursor.fetchall()
                available_tables = [table_name for table_name, in res]
                constraints['table'] = strlist_to_enum('table', available_tables)
        return create_model('FormSchema', **constraints, **{'__base__': cls}).schema()


class MySQLConnector(ToucanConnector):
    __doc__ = '\n    Import data from MySQL database.\n    '
    data_source_model: MySQLDataSource
    host = Field(...,
      description='The domain name (preferred option as more dynamic) or the hardcoded IP address of your database server')
    host: str
    port = Field(None, description='The listening port of your database server')
    port: int
    user = Field(..., description='Your login username')
    user: str
    password = Field(None, description='Your login password')
    password: SecretStr
    charset = Field('utf8mb4',
      title='Charset',
      description='Character encoding. You should generally let the default "utf8mb4" here.')
    charset: str
    connect_timeout = Field(None,
      title='Connection timeout',
      description='You can set a connection timeout in seconds here, i.e. the maximum length of time you want to wait for the server to respond. None by default')
    connect_timeout: int

    def get_connection_params(self, *, database=None, cursorclass=pymysql.cursors.DictCursor):
        conv = pymysql.converters.conversions.copy()
        conv[246] = float
        con_params = {'host':self.host, 
         'user':self.user, 
         'password':self.password.get_secret_value() if self.password else None, 
         'port':self.port, 
         'database':database, 
         'charset':self.charset, 
         'connect_timeout':self.connect_timeout, 
         'conv':conv, 
         'cursorclass':cursorclass}
        return {v:k for k, v in con_params.items() if v is not None if v is not None}

    @staticmethod
    def _get_details(index: int, status: Optional[bool]):
        checks = ['Hostname resolved', 'Port opened', 'Host connection', 'Authenticated']
        ok_checks = [(c, True) for i, c in enumerate(checks) if i < index]
        new_check = (checks[index], status)
        not_validated_checks = [(c, None) for i, c in enumerate(checks) if i > index]
        return ok_checks + [new_check] + not_validated_checks

    def get_status--- This code section failed: ---

 L. 142         0  SETUP_FINALLY        18  'to 18'

 L. 143         2  LOAD_FAST                'self'
                4  LOAD_METHOD              check_hostname
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                host
               10  CALL_METHOD_1         1  ''
               12  POP_TOP          
               14  POP_BLOCK        
               16  JUMP_FORWARD         80  'to 80'
             18_0  COME_FROM_FINALLY     0  '0'

 L. 144        18  DUP_TOP          
               20  LOAD_GLOBAL              Exception
               22  COMPARE_OP               exception-match
               24  POP_JUMP_IF_FALSE    78  'to 78'
               26  POP_TOP          
               28  STORE_FAST               'e'
               30  POP_TOP          
               32  SETUP_FINALLY        66  'to 66'

 L. 145        34  LOAD_CONST               False
               36  LOAD_FAST                'self'
               38  LOAD_METHOD              _get_details
               40  LOAD_CONST               0
               42  LOAD_CONST               False
               44  CALL_METHOD_2         2  ''
               46  LOAD_GLOBAL              str
               48  LOAD_FAST                'e'
               50  CALL_FUNCTION_1       1  ''
               52  LOAD_CONST               ('status', 'details', 'error')
               54  BUILD_CONST_KEY_MAP_3     3 
               56  ROT_FOUR         
               58  POP_BLOCK        
               60  POP_EXCEPT       
               62  CALL_FINALLY         66  'to 66'
               64  RETURN_VALUE     
             66_0  COME_FROM            62  '62'
             66_1  COME_FROM_FINALLY    32  '32'
               66  LOAD_CONST               None
               68  STORE_FAST               'e'
               70  DELETE_FAST              'e'
               72  END_FINALLY      
               74  POP_EXCEPT       
               76  JUMP_FORWARD         80  'to 80'
             78_0  COME_FROM            24  '24'
               78  END_FINALLY      
             80_0  COME_FROM            76  '76'
             80_1  COME_FROM            16  '16'

 L. 148        80  SETUP_FINALLY       102  'to 102'

 L. 149        82  LOAD_FAST                'self'
               84  LOAD_METHOD              check_port
               86  LOAD_FAST                'self'
               88  LOAD_ATTR                host
               90  LOAD_FAST                'self'
               92  LOAD_ATTR                port
               94  CALL_METHOD_2         2  ''
               96  POP_TOP          
               98  POP_BLOCK        
              100  JUMP_FORWARD        164  'to 164'
            102_0  COME_FROM_FINALLY    80  '80'

 L. 150       102  DUP_TOP          
              104  LOAD_GLOBAL              Exception
              106  COMPARE_OP               exception-match
              108  POP_JUMP_IF_FALSE   162  'to 162'
              110  POP_TOP          
              112  STORE_FAST               'e'
              114  POP_TOP          
              116  SETUP_FINALLY       150  'to 150'

 L. 151       118  LOAD_CONST               False
              120  LOAD_FAST                'self'
              122  LOAD_METHOD              _get_details
              124  LOAD_CONST               1
              126  LOAD_CONST               False
              128  CALL_METHOD_2         2  ''
              130  LOAD_GLOBAL              str
              132  LOAD_FAST                'e'
              134  CALL_FUNCTION_1       1  ''
              136  LOAD_CONST               ('status', 'details', 'error')
              138  BUILD_CONST_KEY_MAP_3     3 
              140  ROT_FOUR         
              142  POP_BLOCK        
              144  POP_EXCEPT       
              146  CALL_FINALLY        150  'to 150'
              148  RETURN_VALUE     
            150_0  COME_FROM           146  '146'
            150_1  COME_FROM_FINALLY   116  '116'
              150  LOAD_CONST               None
              152  STORE_FAST               'e'
              154  DELETE_FAST              'e'
              156  END_FINALLY      
              158  POP_EXCEPT       
              160  JUMP_FORWARD        164  'to 164'
            162_0  COME_FROM           108  '108'
              162  END_FINALLY      
            164_0  COME_FROM           160  '160'
            164_1  COME_FROM           100  '100'

 L. 154       164  SETUP_FINALLY       186  'to 186'

 L. 155       166  LOAD_GLOBAL              pymysql
              168  LOAD_ATTR                connect
              170  BUILD_TUPLE_0         0 
              172  LOAD_FAST                'self'
              174  LOAD_METHOD              get_connection_params
              176  CALL_METHOD_0         0  ''
              178  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              180  POP_TOP          
              182  POP_BLOCK        
              184  JUMP_FORWARD        328  'to 328'
            186_0  COME_FROM_FINALLY   164  '164'

 L. 156       186  DUP_TOP          
              188  LOAD_GLOBAL              pymysql
              190  LOAD_ATTR                err
              192  LOAD_ATTR                OperationalError
              194  COMPARE_OP               exception-match
          196_198  POP_JUMP_IF_FALSE   326  'to 326'
              200  POP_TOP          
              202  STORE_FAST               'e'
              204  POP_TOP          
              206  SETUP_FINALLY       314  'to 314'

 L. 157       208  LOAD_FAST                'e'
              210  LOAD_ATTR                args
              212  LOAD_CONST               0
              214  BINARY_SUBSCR    
              216  STORE_FAST               'error_code'

 L. 160       218  LOAD_FAST                'error_code'
              220  LOAD_GLOBAL              CR
              222  LOAD_ATTR                CR_CONN_HOST_ERROR
              224  COMPARE_OP               ==
          226_228  POP_JUMP_IF_FALSE   264  'to 264'

 L. 161       230  LOAD_CONST               False
              232  LOAD_FAST                'self'
              234  LOAD_METHOD              _get_details
              236  LOAD_CONST               2
              238  LOAD_CONST               False
              240  CALL_METHOD_2         2  ''
              242  LOAD_FAST                'e'
              244  LOAD_ATTR                args
              246  LOAD_CONST               1
              248  BINARY_SUBSCR    
              250  LOAD_CONST               ('status', 'details', 'error')
              252  BUILD_CONST_KEY_MAP_3     3 
              254  ROT_FOUR         
              256  POP_BLOCK        
              258  POP_EXCEPT       
              260  CALL_FINALLY        314  'to 314'
              262  RETURN_VALUE     
            264_0  COME_FROM           226  '226'

 L. 164       264  LOAD_FAST                'error_code'
              266  LOAD_GLOBAL              ER
              268  LOAD_ATTR                ACCESS_DENIED_ERROR
              270  COMPARE_OP               ==
          272_274  POP_JUMP_IF_FALSE   310  'to 310'

 L. 165       276  LOAD_CONST               False
              278  LOAD_FAST                'self'
              280  LOAD_METHOD              _get_details
              282  LOAD_CONST               3
              284  LOAD_CONST               False
              286  CALL_METHOD_2         2  ''
              288  LOAD_FAST                'e'
              290  LOAD_ATTR                args
              292  LOAD_CONST               1
              294  BINARY_SUBSCR    
              296  LOAD_CONST               ('status', 'details', 'error')
              298  BUILD_CONST_KEY_MAP_3     3 
              300  ROT_FOUR         
              302  POP_BLOCK        
              304  POP_EXCEPT       
              306  CALL_FINALLY        314  'to 314'
              308  RETURN_VALUE     
            310_0  COME_FROM           272  '272'
              310  POP_BLOCK        
              312  BEGIN_FINALLY    
            314_0  COME_FROM           306  '306'
            314_1  COME_FROM           260  '260'
            314_2  COME_FROM_FINALLY   206  '206'
              314  LOAD_CONST               None
              316  STORE_FAST               'e'
              318  DELETE_FAST              'e'
              320  END_FINALLY      
              322  POP_EXCEPT       
              324  JUMP_FORWARD        328  'to 328'
            326_0  COME_FROM           196  '196'
              326  END_FINALLY      
            328_0  COME_FROM           324  '324'
            328_1  COME_FROM           184  '184'

 L. 167       328  LOAD_CONST               True
              330  LOAD_FAST                'self'
              332  LOAD_METHOD              _get_details
              334  LOAD_CONST               3
              336  LOAD_CONST               True
              338  CALL_METHOD_2         2  ''
              340  LOAD_CONST               None
              342  LOAD_CONST               ('status', 'details', 'error')
              344  BUILD_CONST_KEY_MAP_3     3 
              346  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 256

    @staticmethod
    def clean_response(response):
        for elt in response:
            for k, v in elt.items():
                if v is None:
                    elt[k] = np.nan
                elif isinstance(v, bytes):
                    elt[k] = v.decode('utf8')
            else:
                return response

    @staticmethod
    def execute_and_fetchall(query, connection):
        cursor = connection.cursor()
        cursor.execute(query)
        return cursor.fetchall()

    @staticmethod
    def _merge_drop(df, f_df, suffixes, f_key, f_table_key):
        """
        Merge two DataFrames and drop unnecessary column.
        Args:
            df: base DataFrame
            f_df: DataFrame from foreign table
            suffixes: suffixes for merge
            f_key: foreign key
            f_table_key: foreign table's key

        Returns: Bigger DataFrame.

        """
        tmp_df = df.merge(f_df, left_on=f_key, right_on=f_table_key, how='outer', suffixes=suffixes)
        MySQLConnector.logger.info('Merged two DataFrames...')
        if f_key != f_table_key:
            if f_table_key not in tmp_df.columns:
                MySQLConnector.logger.info(f" and dropped one column {f_table_key}{suffixes[0]}")
                return tmp_df.drop((f_table_key + suffixes[0]), axis=1)
            MySQLConnector.logger.info(' no column dropped')
            return tmp_df.drop(f_table_key, axis=1)
        return tmp_df

    @staticmethod
    def extract_info(fetch_all):
        """
        Extract the key, table name and key in the foreign table from a
        line. It must be the line that has the 'FOREIGN KEY' string. A
        find must have been done before calling this method.
        Args:
            fetch_all: string to parse

        Returns: list of dicts with 'f_key', 'f_table', 'f_table_key' keys.

        """
        idx = 0
        res = []
        while idx >= 0:
            info = {}
            MySQLConnector.logger.info('start searching for foreign key.')
            info['f_key'], idx = MySQLConnector.extract_info_word(fetch_all, idx, ['FOREIGN', 'KEY'])
            if idx == -1:
                MySQLConnector.logger.info('No (other) foreign key.')
                return res
            info['f_table'], idx = MySQLConnector.extract_info_word(fetch_all, idx, ['REFERENCES'])
            if idx == -1:
                MySQLConnector.logger.error(f"Foreign key {info['f_key']}, found but no REFERENCES found.")
                return res
            info['f_table_key'], idx = MySQLConnector.extract_info_word(fetch_all, idx, [])
            if idx == -1:
                MySQLConnector.logger.error(f"Foreign key {info['_key']} and REFERENCES found but no foreign table key.")
                return res
            res.append(info)

    @staticmethod
    def extract_info_word(line, start, words_to_match):
        """
        Extract an information such as a table or a key name from a string.
        Parse the string word by word and find the wanted information after
         some words to match (eg. find a key after FOREIGN KEY)
        Args:
            line: string to parse
            start: start index
            words_to_match: list of words to match before the wanted information.

        Returns: wanted information as a string

        """
        idx = start
        len_line = len(line)
        curr_idx_to_match = 0
        len_words_to_match = len(words_to_match)
        while idx < len_line:
            word, idx = MySQLConnector._get_wordlineidx
            if curr_idx_to_match == len_words_to_match:
                return (
                 word, idx)
            if word.upper() == words_to_match[curr_idx_to_match]:
                curr_idx_to_match = curr_idx_to_match + 1

        return ('', -1)

    @staticmethod
    def _get_word(line, start):
        """
        Extract the first word found starting from start index
        Args:
            line: line to parse
            start: start index

        Returns: first word found.

        """

        def valid_char(word):
            return word.isalnum() or word == '_'

        idx_start = start
        len_line = len(line)
        if idx_start < len_line:
            if not valid_char(line[idx_start]):
                idx_start = idx_start + 1
        elif idx_start == len_line:
            return (
             '', idx_start)
        else:
            idx_end = idx_start
            while True:
                if idx_end < len_line and valid_char(line[idx_end]):
                    idx_end = idx_end + 1

        if idx_end == 0 or idx_end == len_line:
            return (
             '', idx_end)
        return (
         line[idx_start:idx_end], idx_end)

    @staticmethod
    def get_foreign_key_info(table_name, connection):
        """
        Get the foreign key information from a table: foreign key inside the
        table, foreign table, key inside that table.
        Args:
            table_name: table name...

        Returns: list of dicts ('f_key', 'f_table', 'f_table_key')

        """
        fetch_all_query = f"show create table {table_name}"
        fetch_all_list = MySQLConnector.execute_and_fetchallfetch_all_queryconnection
        keys = list(fetch_all_list[0].keys())
        if 'Create Table' in keys:
            fetch_all = fetch_all_list[0]['Create Table']
        else:
            if 'Create View' in keys:
                fetch_all = fetch_all_list[0]['Create View']
            else:
                raise InvalidQuery(keys)
        return MySQLConnector.extract_info(fetch_all)

    @staticmethod
    def decode_df(df):
        """
        Used to change bytes columns to string columns
        (can be moved to be applied for all connectors if needed)
        It retrieves all the string columns and converts them all together.
        The string columns become nan columns so we remove them from the result,
        we keep the rest and insert it back to the dataframe
        """
        str_df = df.select_dtypes([np.object])
        if str_df.empty:
            return df
        str_df = str_df.stack().str.decode('utf8').unstack().dropna(axis=1, how='all')
        for col in str_df.columns:
            df[col] = str_df[col]
        else:
            return df

    def _retrieve_data--- This code section failed: ---

 L. 363         0  LOAD_GLOBAL              pymysql
                2  LOAD_ATTR                connect
                4  BUILD_TUPLE_0         0 
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                get_connection_params
               10  LOAD_FAST                'datasource'
               12  LOAD_ATTR                database
               14  LOAD_CONST               ('database',)
               16  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               18  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               20  STORE_FAST               'connection'

 L. 366        22  LOAD_FAST                'datasource'
               24  LOAD_ATTR                query
               26  POP_JUMP_IF_FALSE    62  'to 62'

 L. 367        28  LOAD_FAST                'datasource'
               30  LOAD_ATTR                query
               32  STORE_FAST               'query'

 L. 369        34  LOAD_GLOBAL              re
               36  LOAD_METHOD              search

 L. 370        38  LOAD_STR                 'from\\s*(?P<table>[^\\s]+)\\s*(where|order by|group by|limit)?'

 L. 370        40  LOAD_FAST                'query'

 L. 370        42  LOAD_GLOBAL              re
               44  LOAD_ATTR                I

 L. 369        46  CALL_METHOD_3         3  ''
               48  STORE_FAST               'm'

 L. 372        50  LOAD_FAST                'm'
               52  LOAD_METHOD              group
               54  LOAD_STR                 'table'
               56  CALL_METHOD_1         1  ''
               58  STORE_FAST               'table'
               60  JUMP_FORWARD         78  'to 78'
             62_0  COME_FROM            26  '26'

 L. 374        62  LOAD_FAST                'datasource'
               64  LOAD_ATTR                table
               66  STORE_FAST               'table'

 L. 375        68  LOAD_STR                 'select * from '
               70  LOAD_FAST                'table'
               72  FORMAT_VALUE          0  ''
               74  BUILD_STRING_2        2 
               76  STORE_FAST               'query'
             78_0  COME_FROM            60  '60'

 L. 377        78  LOAD_GLOBAL              MySQLConnector
               80  LOAD_ATTR                logger
               82  LOAD_METHOD              debug
               84  LOAD_STR                 'Executing query : '
               86  LOAD_FAST                'query'
               88  FORMAT_VALUE          0  ''
               90  BUILD_STRING_2        2 
               92  CALL_METHOD_1         1  ''
               94  POP_TOP          

 L. 378        96  LOAD_FAST                'datasource'
               98  LOAD_ATTR                parameters
              100  JUMP_IF_TRUE_OR_POP   104  'to 104'
              102  BUILD_MAP_0           0 
            104_0  COME_FROM           100  '100'
              104  STORE_FAST               'query_params'

 L. 380       106  LOAD_FAST                'datasource'
              108  LOAD_ATTR                follow_relations
              110  POP_JUMP_IF_TRUE    150  'to 150'

 L. 381       112  LOAD_GLOBAL              pd
              114  LOAD_ATTR                read_sql
              116  LOAD_FAST                'query'
              118  LOAD_FAST                'connection'
              120  LOAD_FAST                'query_params'
              122  LOAD_CONST               ('con', 'params')
              124  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              126  STORE_FAST               'df'

 L. 382       128  LOAD_FAST                'self'
              130  LOAD_METHOD              decode_df
              132  LOAD_FAST                'df'
              134  CALL_METHOD_1         1  ''
              136  STORE_FAST               'df'

 L. 383       138  LOAD_FAST                'connection'
              140  LOAD_METHOD              close
              142  CALL_METHOD_0         0  ''
              144  POP_TOP          

 L. 384       146  LOAD_FAST                'df'
              148  RETURN_VALUE     
            150_0  COME_FROM           110  '110'

 L. 389       150  LOAD_GLOBAL              pd
              152  LOAD_ATTR                read_sql
              154  LOAD_FAST                'query'
              156  LOAD_FAST                'connection'
              158  LOAD_FAST                'query_params'
              160  LOAD_CONST               ('con', 'params')
              162  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              164  BUILD_LIST_1          1 
              166  STORE_FAST               'lres'

 L. 390       168  LOAD_GLOBAL              MySQLConnector
              170  LOAD_ATTR                logger
              172  LOAD_METHOD              info
              174  LOAD_FAST                'table'
              176  FORMAT_VALUE          0  ''
              178  LOAD_STR                 ' : dumped first DataFrame'
              180  BUILD_STRING_2        2 
              182  CALL_METHOD_1         1  ''
              184  POP_TOP          

 L. 396       186  BUILD_LIST_0          0 
              188  STORE_FAST               'infos'

 L. 397       190  LOAD_FAST                'table'
              192  BUILD_SET_1           1 
              194  STORE_FAST               'has_been_merged'

 L. 398       196  LOAD_FAST                'self'
              198  LOAD_METHOD              get_foreign_key_info
              200  LOAD_FAST                'table'
              202  LOAD_FAST                'connection'
              204  CALL_METHOD_2         2  ''
              206  STORE_FAST               'foreign_keys_append'

 L. 399       208  LOAD_GLOBAL              len
              210  LOAD_FAST                'foreign_keys_append'
              212  CALL_FUNCTION_1       1  ''
              214  LOAD_CONST               0
              216  COMPARE_OP               >
              218  POP_JUMP_IF_FALSE   240  'to 240'

 L. 400       220  LOAD_FAST                'foreign_keys_append'
              222  GET_ITER         
              224  FOR_ITER            240  'to 240'
              226  STORE_FAST               'keys'

 L. 401       228  LOAD_FAST                'infos'
              230  LOAD_METHOD              append
              232  LOAD_FAST                'keys'
              234  CALL_METHOD_1         1  ''
              236  POP_TOP          
              238  JUMP_BACK           224  'to 224'
            240_0  COME_FROM           456  '456'
            240_1  COME_FROM           218  '218'

 L. 402       240  LOAD_FAST                'infos'
          242_244  POP_JUMP_IF_FALSE   482  'to 482'

 L. 403       246  LOAD_FAST                'infos'
              248  LOAD_METHOD              pop
              250  CALL_METHOD_0         0  ''
              252  STORE_FAST               'table_info'

 L. 405       254  LOAD_FAST                'table_info'
              256  LOAD_CONST               None
              258  COMPARE_OP               is
          260_262  POP_JUMP_IF_FALSE   268  'to 268'

 L. 406       264  JUMP_BACK           240  'to 240'
              266  JUMP_FORWARD        284  'to 284'
            268_0  COME_FROM           260  '260'

 L. 407       268  LOAD_FAST                'table_info'
              270  LOAD_STR                 'f_table'
              272  BINARY_SUBSCR    
              274  LOAD_FAST                'has_been_merged'
              276  COMPARE_OP               in
          278_280  POP_JUMP_IF_FALSE   284  'to 284'

 L. 408       282  JUMP_BACK           240  'to 240'
            284_0  COME_FROM           278  '278'
            284_1  COME_FROM           266  '266'

 L. 410       284  LOAD_GLOBAL              MySQLConnector
              286  LOAD_ATTR                logger
              288  LOAD_METHOD              info

 L. 411       290  LOAD_FAST                'table'
              292  FORMAT_VALUE          0  ''
              294  LOAD_STR                 ' <> found foreign key: '
              296  LOAD_FAST                'table_info'
              298  LOAD_STR                 'f_key'
              300  BINARY_SUBSCR    
              302  FORMAT_VALUE          0  ''
              304  LOAD_STR                 ' inside '
              306  LOAD_FAST                'table_info'
              308  LOAD_STR                 'f_table'
              310  BINARY_SUBSCR    
              312  FORMAT_VALUE          0  ''
              314  BUILD_STRING_5        5 

 L. 410       316  CALL_METHOD_1         1  ''
              318  POP_TOP          

 L. 415       320  LOAD_GLOBAL              pd
              322  LOAD_ATTR                read_sql
              324  LOAD_STR                 'select * from '
              326  LOAD_FAST                'table_info'
              328  LOAD_STR                 'f_table'
              330  BINARY_SUBSCR    
              332  FORMAT_VALUE          0  ''
              334  BUILD_STRING_2        2 
              336  LOAD_FAST                'connection'
              338  LOAD_CONST               ('con',)
              340  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              342  STORE_FAST               'f_df'

 L. 416       344  LOAD_STR                 '_'
              346  LOAD_FAST                'table'
              348  BINARY_ADD       
              350  LOAD_STR                 '_'
              352  LOAD_FAST                'table_info'
              354  LOAD_STR                 'f_table'
              356  BINARY_SUBSCR    
              358  BINARY_ADD       
              360  BUILD_TUPLE_2         2 
              362  STORE_FAST               'suffixes'

 L. 417       364  LOAD_FAST                'lres'
              366  LOAD_METHOD              append

 L. 418       368  LOAD_FAST                'self'
              370  LOAD_METHOD              _merge_drop

 L. 419       372  LOAD_FAST                'lres'
              374  LOAD_CONST               0
              376  BINARY_SUBSCR    

 L. 419       378  LOAD_FAST                'f_df'

 L. 419       380  LOAD_FAST                'suffixes'

 L. 419       382  LOAD_FAST                'table_info'
              384  LOAD_STR                 'f_key'
              386  BINARY_SUBSCR    

 L. 419       388  LOAD_FAST                'table_info'
              390  LOAD_STR                 'f_table_key'
              392  BINARY_SUBSCR    

 L. 418       394  CALL_METHOD_5         5  ''

 L. 417       396  CALL_METHOD_1         1  ''
              398  POP_TOP          

 L. 423       400  LOAD_FAST                'lres'
          402_404  POP_JUMP_IF_FALSE   412  'to 412'

 L. 424       406  LOAD_FAST                'lres'
              408  LOAD_CONST               0
              410  DELETE_SUBSCR    
            412_0  COME_FROM           402  '402'

 L. 426       412  LOAD_FAST                'has_been_merged'
              414  LOAD_METHOD              add
              416  LOAD_FAST                'table_info'
              418  LOAD_STR                 'f_table'
              420  BINARY_SUBSCR    
              422  CALL_METHOD_1         1  ''
              424  POP_TOP          

 L. 428       426  LOAD_FAST                'table_info'
              428  LOAD_STR                 'f_table'
              430  BINARY_SUBSCR    
              432  STORE_FAST               'table'

 L. 429       434  LOAD_FAST                'self'
              436  LOAD_METHOD              get_foreign_key_info
              438  LOAD_FAST                'table'
              440  LOAD_FAST                'connection'
              442  CALL_METHOD_2         2  ''
              444  STORE_FAST               'foreign_keys_append'

 L. 430       446  LOAD_GLOBAL              len
              448  LOAD_FAST                'foreign_keys_append'
              450  CALL_FUNCTION_1       1  ''
              452  LOAD_CONST               0
              454  COMPARE_OP               >
              456  POP_JUMP_IF_FALSE   240  'to 240'

 L. 431       458  LOAD_FAST                'foreign_keys_append'
              460  GET_ITER         
              462  FOR_ITER            480  'to 480'
              464  STORE_FAST               'keys'

 L. 432       466  LOAD_FAST                'infos'
              468  LOAD_METHOD              append
              470  LOAD_FAST                'keys'
              472  CALL_METHOD_1         1  ''
              474  POP_TOP          
          476_478  JUMP_BACK           462  'to 462'
              480  JUMP_BACK           240  'to 240'
            482_0  COME_FROM           242  '242'

 L. 434       482  LOAD_FAST                'connection'
              484  LOAD_METHOD              close
              486  CALL_METHOD_0         0  ''
              488  POP_TOP          

 L. 436       490  LOAD_FAST                'lres'
              492  LOAD_METHOD              pop
              494  CALL_METHOD_0         0  ''
              496  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_FORWARD' instruction at offset 266


class InvalidQuery(Exception):
    __doc__ = 'raised when a query is invalid'