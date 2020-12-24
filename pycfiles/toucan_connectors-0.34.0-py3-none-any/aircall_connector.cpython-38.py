# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rachelle2/webprojects/toucan-connectors/toucan_connectors/aircall/aircall_connector.py
# Compiled at: 2020-04-22 11:33:02
# Size of source mod 2**32: 5533 bytes
import asyncio, os
from enum import Enum
from typing import List, Optional, Tuple
import pandas as pd
from aiohttp import ClientSession
from pydantic import Field
from toucan_connectors.common import get_loop
from toucan_connectors.toucan_connector import ToucanConnector, ToucanDataSource
from .constants import MAX_RUNS, PER_PAGE
from .helpers import DICTIONARY_OF_FORMATTERS, build_df, build_empty_df
BASE_ROUTE = 'https://proxy.bearer.sh/aircall_oauth'
BEARER_API_KEY = os.environ.get('BEARER_API_KEY')

async def fetch_page(dataset: str, data_list: List[dict], session: ClientSession, limit, current_pass: int, new_page=1) -> List[dict]:
    """
    Fetches data from AirCall API

    dependent on existence of other pages and call limit
    """
    endpoint = f"{BASE_ROUTE}/{dataset}?per_page={PER_PAGE}&page={new_page}"
    data = await fetch(endpoint, session)
    data_list.append(data)
    next_page_link = None
    meta_data = data.get('meta')
    if meta_data is not None:
        next_page_link = meta_data.get('next_page_link')
    elif limit > -1:
        current_pass += 1
        if next_page_link is not None and current_pass < limit:
            next_page = meta_data['current_page'] + 1
            data_list = await fetch_page(dataset, data_list, session, limit, current_pass, next_page)
    elif next_page_link is not None:
        next_page = meta_data['current_page'] + 1
        data_list = await fetch_page(dataset, data_list, session, limit, current_pass, next_page)
    return data_list


async def fetch--- This code section failed: ---

 L.  64         0  LOAD_FAST                'session'
                2  LOAD_METHOD              get
                4  LOAD_FAST                'new_endpoint'
                6  CALL_METHOD_1         1  ''
                8  BEFORE_ASYNC_WITH
               10  GET_AWAITABLE    
               12  LOAD_CONST               None
               14  YIELD_FROM       
               16  SETUP_ASYNC_WITH     52  'to 52'
               18  STORE_FAST               'res'

 L.  65        20  LOAD_FAST                'res'
               22  LOAD_METHOD              json
               24  CALL_METHOD_0         0  ''
               26  GET_AWAITABLE    
               28  LOAD_CONST               None
               30  YIELD_FROM       
               32  POP_BLOCK        
               34  ROT_TWO          
               36  BEGIN_FINALLY    
               38  WITH_CLEANUP_START
               40  GET_AWAITABLE    
               42  LOAD_CONST               None
               44  YIELD_FROM       
               46  WITH_CLEANUP_FINISH
               48  POP_FINALLY           0  ''
               50  RETURN_VALUE     
             52_0  COME_FROM_ASYNC_WITH    16  '16'
               52  WITH_CLEANUP_START
               54  GET_AWAITABLE    
               56  LOAD_CONST               None
               58  YIELD_FROM       
               60  WITH_CLEANUP_FINISH
               62  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 34


class AircallDataset(str, Enum):
    calls = 'calls'
    tags = 'tags'
    users = 'users'


class AircallDataSource(ToucanDataSource):
    limit = Field(MAX_RUNS, description='Limit of entries (default is 1 run)', ge=(-1))
    limit: int
    dataset = 'calls'
    dataset: AircallDataset


class AircallConnector(ToucanConnector):
    __doc__ = '\n    This is a connector for [Aircall](https://developer.aircall.io/api-references/#endpoints)\n    using [Bearer.sh](https://app.bearer.sh/)\n    '
    data_source_model: AircallDataSource
    bearer_integration = 'aircall_oauth'
    bearer_auth_id: str

    async def _get_data--- This code section failed: ---

 L.  91         0  LOAD_GLOBAL              BEARER_API_KEY
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                bearer_auth_id
                6  LOAD_CONST               ('Authorization', 'Bearer-Auth-Id')
                8  BUILD_CONST_KEY_MAP_2     2 
               10  STORE_FAST               'headers'

 L.  92        12  LOAD_GLOBAL              ClientSession
               14  LOAD_FAST                'headers'
               16  LOAD_CONST               ('headers',)
               18  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               20  BEFORE_ASYNC_WITH
               22  GET_AWAITABLE    
               24  LOAD_CONST               None
               26  YIELD_FROM       
               28  SETUP_ASYNC_WITH    212  'to 212'
               30  STORE_FAST               'session'

 L.  93        32  LOAD_GLOBAL              asyncio
               34  LOAD_METHOD              gather

 L.  94        36  LOAD_GLOBAL              fetch_page
               38  LOAD_STR                 'teams'
               40  BUILD_LIST_0          0 
               42  LOAD_FAST                'session'
               44  LOAD_FAST                'limit'
               46  LOAD_CONST               0
               48  CALL_FUNCTION_5       5  ''

 L.  95        50  LOAD_GLOBAL              fetch_page
               52  LOAD_DEREF               'dataset'
               54  BUILD_LIST_0          0 
               56  LOAD_FAST                'session'
               58  LOAD_FAST                'limit'
               60  LOAD_CONST               0
               62  CALL_FUNCTION_5       5  ''

 L.  93        64  CALL_METHOD_2         2  ''
               66  GET_AWAITABLE    
               68  LOAD_CONST               None
               70  YIELD_FROM       
               72  UNPACK_SEQUENCE_2     2 
               74  STORE_FAST               'team_data'
               76  STORE_FAST               'variable_data'

 L.  98        78  BUILD_LIST_0          0 
               80  STORE_FAST               'team_response_list'

 L.  99        82  BUILD_LIST_0          0 
               84  STORE_FAST               'variable_response_list'

 L. 100        86  LOAD_GLOBAL              len
               88  LOAD_FAST                'team_data'
               90  CALL_FUNCTION_1       1  ''
               92  LOAD_CONST               0
               94  COMPARE_OP               >
               96  POP_JUMP_IF_FALSE   138  'to 138'

 L. 101        98  LOAD_FAST                'team_data'
              100  GET_ITER         
              102  FOR_ITER            138  'to 138'
              104  STORE_FAST               'data'

 L. 102       106  LOAD_FAST                'data'
              108  LOAD_STR                 'teams'
              110  BINARY_SUBSCR    
              112  GET_ITER         
              114  FOR_ITER            136  'to 136'
              116  STORE_FAST               'team_obj'

 L. 103       118  LOAD_FAST                'team_response_list'
              120  LOAD_GLOBAL              DICTIONARY_OF_FORMATTERS
              122  LOAD_STR                 'teams'
              124  BINARY_SUBSCR    
              126  LOAD_FAST                'team_obj'
              128  CALL_FUNCTION_1       1  ''
              130  INPLACE_ADD      
              132  STORE_FAST               'team_response_list'
              134  JUMP_BACK           114  'to 114'
              136  JUMP_BACK           102  'to 102'
            138_0  COME_FROM            96  '96'

 L. 105       138  LOAD_GLOBAL              len
              140  LOAD_FAST                'variable_data'
              142  CALL_FUNCTION_1       1  ''
              144  LOAD_CONST               0
              146  COMPARE_OP               >
              148  POP_JUMP_IF_FALSE   186  'to 186'

 L. 106       150  LOAD_FAST                'variable_data'
              152  GET_ITER         
              154  FOR_ITER            186  'to 186'
              156  STORE_FAST               'data'

 L. 107       158  LOAD_FAST                'variable_response_list'
              160  LOAD_CLOSURE             'dataset'
              162  BUILD_TUPLE_1         1 
              164  LOAD_LISTCOMP            '<code_object <listcomp>>'
              166  LOAD_STR                 'AircallConnector._get_data.<locals>.<listcomp>'
              168  MAKE_FUNCTION_8          'closure'
              170  LOAD_FAST                'data'
              172  LOAD_DEREF               'dataset'
              174  BINARY_SUBSCR    
              176  GET_ITER         
              178  CALL_FUNCTION_1       1  ''
              180  INPLACE_ADD      
              182  STORE_FAST               'variable_response_list'
              184  JUMP_BACK           154  'to 154'
            186_0  COME_FROM           148  '148'

 L. 108       186  LOAD_FAST                'team_response_list'
              188  LOAD_FAST                'variable_response_list'
              190  BUILD_TUPLE_2         2 
              192  POP_BLOCK        
              194  ROT_TWO          
              196  BEGIN_FINALLY    
              198  WITH_CLEANUP_START
              200  GET_AWAITABLE    
              202  LOAD_CONST               None
              204  YIELD_FROM       
              206  WITH_CLEANUP_FINISH
              208  POP_FINALLY           0  ''
              210  RETURN_VALUE     
            212_0  COME_FROM_ASYNC_WITH    28  '28'
              212  WITH_CLEANUP_START
              214  GET_AWAITABLE    
              216  LOAD_CONST               None
              218  YIELD_FROM       
              220  WITH_CLEANUP_FINISH
              222  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 194

    async def _get_tags--- This code section failed: ---

 L. 112         0  LOAD_GLOBAL              BEARER_API_KEY
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                bearer_auth_id
                6  LOAD_CONST               ('Authorization', 'Bearer-Auth-Id')
                8  BUILD_CONST_KEY_MAP_2     2 
               10  STORE_FAST               'headers'

 L. 113        12  LOAD_GLOBAL              ClientSession
               14  LOAD_FAST                'headers'
               16  LOAD_CONST               ('headers',)
               18  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               20  BEFORE_ASYNC_WITH
               22  GET_AWAITABLE    
               24  LOAD_CONST               None
               26  YIELD_FROM       
               28  SETUP_ASYNC_WITH    102  'to 102'
               30  STORE_FAST               'session'

 L. 114        32  LOAD_GLOBAL              fetch_page
               34  LOAD_FAST                'dataset'
               36  BUILD_LIST_0          0 
               38  LOAD_FAST                'session'
               40  LOAD_FAST                'limit'
               42  LOAD_CONST               1
               44  CALL_FUNCTION_5       5  ''
               46  GET_AWAITABLE    
               48  LOAD_CONST               None
               50  YIELD_FROM       
               52  STORE_FAST               'raw_data'

 L. 115        54  BUILD_LIST_0          0 
               56  STORE_FAST               'tags_data_list'

 L. 116        58  LOAD_FAST                'raw_data'
               60  GET_ITER         
               62  FOR_ITER             80  'to 80'
               64  STORE_FAST               'data'

 L. 117        66  LOAD_FAST                'tags_data_list'
               68  LOAD_FAST                'data'
               70  LOAD_STR                 'tags'
               72  BINARY_SUBSCR    
               74  INPLACE_ADD      
               76  STORE_FAST               'tags_data_list'
               78  JUMP_BACK            62  'to 62'

 L. 118        80  LOAD_FAST                'tags_data_list'
               82  POP_BLOCK        
               84  ROT_TWO          
               86  BEGIN_FINALLY    
               88  WITH_CLEANUP_START
               90  GET_AWAITABLE    
               92  LOAD_CONST               None
               94  YIELD_FROM       
               96  WITH_CLEANUP_FINISH
               98  POP_FINALLY           0  ''
              100  RETURN_VALUE     
            102_0  COME_FROM_ASYNC_WITH    28  '28'
              102  WITH_CLEANUP_START
              104  GET_AWAITABLE    
              106  LOAD_CONST               None
              108  YIELD_FROM       
              110  WITH_CLEANUP_FINISH
              112  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 84

    def run_fetches(self, dataset, limit) -> Tuple[(List[dict], List[dict])]:
        """sets up event loop and fetches for 'calls' and 'users' datasets"""
        loop = get_loop()
        future = asyncio.ensure_future(self._get_datadatasetlimit)
        return loop.run_until_complete(future)

    def run_fetches_for_tags(self, dataset, limit):
        """sets up event loop and fetches for 'tags' dataset"""
        loop = get_loop()
        future = asyncio.ensure_future(self._get_tagsdatasetlimit)
        return loop.run_until_complete(future)

    def _retrieve_data(self, data_source: AircallDataSource) -> pd.DataFrame:
        """retrieves data from AirCall API"""
        dataset = data_source.dataset
        empty_df = build_empty_df(dataset)
        limit = data_source.limit
        if dataset == 'tags':
            non_empty_df = pd.DataFrame([])
            if limit != 0:
                res = self.run_fetches_for_tagsdatasetlimit
                non_empty_df = pd.DataFrame(res)
            return pd.concat([empty_df, non_empty_df])
        team_data = pd.DataFrame([])
        variable_data = pd.DataFrame([])
        if limit != 0:
            team_data, variable_data = self.run_fetchesdatasetlimit
        return build_df(dataset, [empty_df, pd.DataFrame(team_data), pd.DataFrame(variable_data)])