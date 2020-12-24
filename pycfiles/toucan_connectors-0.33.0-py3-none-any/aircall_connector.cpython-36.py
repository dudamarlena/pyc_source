# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rachelle2/webprojects/toucan-connectors/toucan_connectors/aircall/aircall_connector.py
# Compiled at: 2020-04-22 11:24:47
# Size of source mod 2**32: 5727 bytes
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
    if limit > -1:
        current_pass += 1
        if next_page_link is not None:
            if current_pass < limit:
                next_page = meta_data['current_page'] + 1
                data_list = await fetch_page(dataset, data_list, session, limit, current_pass, next_page)
    else:
        if next_page_link is not None:
            next_page = meta_data['current_page'] + 1
            data_list = await fetch_page(dataset, data_list, session, limit, current_pass, next_page)
    return data_list


async def fetch--- This code section failed: ---

 L.  64         0  LOAD_FAST                'session'
                2  LOAD_ATTR                get
                4  LOAD_FAST                'new_endpoint'
                6  CALL_FUNCTION_1       1  '1 positional argument'
                8  BEFORE_ASYNC_WITH
               10  GET_AWAITABLE    
               12  LOAD_CONST               None
               14  YIELD_FROM       
               16  SETUP_ASYNC_WITH     34  'to 34'
               18  STORE_FAST               'res'

 L.  65        20  LOAD_FAST                'res'
               22  LOAD_ATTR                json
               24  CALL_FUNCTION_0       0  '0 positional arguments'
               26  GET_AWAITABLE    
               28  LOAD_CONST               None
               30  YIELD_FROM       
               32  RETURN_VALUE     
             34_0  COME_FROM_ASYNC_WITH    16  '16'
               34  WITH_CLEANUP_START
               36  GET_AWAITABLE    
               38  LOAD_CONST               None
               40  YIELD_FROM       
               42  WITH_CLEANUP_FINISH
               44  END_FINALLY      

Parse error at or near `COME_FROM_ASYNC_WITH' instruction at offset 34_0


class AircallDataset(str, Enum):
    calls = 'calls'
    tags = 'tags'
    users = 'users'


class AircallDataSource(ToucanDataSource):
    limit: int = Field(MAX_RUNS, description='Limit of entries (default is 1 run)', ge=(-1))
    dataset: AircallDataset = 'calls'


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
               28  SETUP_ASYNC_WITH    214  'to 214'
               30  STORE_FAST               'session'

 L.  93        32  LOAD_GLOBAL              asyncio
               34  LOAD_ATTR                gather

 L.  94        36  LOAD_GLOBAL              fetch_page
               38  LOAD_STR                 'teams'
               40  BUILD_LIST_0          0 
               42  LOAD_FAST                'session'
               44  LOAD_FAST                'limit'
               46  LOAD_CONST               0
               48  CALL_FUNCTION_5       5  '5 positional arguments'

 L.  95        50  LOAD_GLOBAL              fetch_page
               52  LOAD_DEREF               'dataset'
               54  BUILD_LIST_0          0 
               56  LOAD_FAST                'session'
               58  LOAD_FAST                'limit'
               60  LOAD_CONST               0
               62  CALL_FUNCTION_5       5  '5 positional arguments'
               64  CALL_FUNCTION_2       2  '2 positional arguments'
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
               90  CALL_FUNCTION_1       1  '1 positional argument'
               92  LOAD_CONST               0
               94  COMPARE_OP               >
               96  POP_JUMP_IF_FALSE   148  'to 148'

 L. 101        98  SETUP_LOOP          148  'to 148'
              100  LOAD_FAST                'team_data'
              102  GET_ITER         
              104  FOR_ITER            146  'to 146'
              106  STORE_FAST               'data'

 L. 102       108  SETUP_LOOP          144  'to 144'
              110  LOAD_FAST                'data'
              112  LOAD_ATTR                get
              114  LOAD_STR                 'teams'
              116  CALL_FUNCTION_1       1  '1 positional argument'
              118  GET_ITER         
              120  FOR_ITER            142  'to 142'
              122  STORE_FAST               'team_obj'

 L. 103       124  LOAD_FAST                'team_response_list'
              126  LOAD_GLOBAL              DICTIONARY_OF_FORMATTERS
              128  LOAD_STR                 'teams'
              130  BINARY_SUBSCR    
              132  LOAD_FAST                'team_obj'
              134  CALL_FUNCTION_1       1  '1 positional argument'
              136  INPLACE_ADD      
              138  STORE_FAST               'team_response_list'
              140  JUMP_BACK           120  'to 120'
              142  POP_BLOCK        
            144_0  COME_FROM_LOOP      108  '108'
              144  JUMP_BACK           104  'to 104'
              146  POP_BLOCK        
            148_0  COME_FROM_LOOP       98  '98'
            148_1  COME_FROM            96  '96'

 L. 105       148  LOAD_GLOBAL              len
              150  LOAD_FAST                'variable_data'
              152  CALL_FUNCTION_1       1  '1 positional argument'
              154  LOAD_CONST               0
              156  COMPARE_OP               >
              158  POP_JUMP_IF_FALSE   206  'to 206'

 L. 106       160  SETUP_LOOP          206  'to 206'
              162  LOAD_FAST                'variable_data'
              164  GET_ITER         
              166  FOR_ITER            204  'to 204'
              168  STORE_FAST               'data'

 L. 107       170  LOAD_FAST                'variable_response_list'
              172  LOAD_GLOBAL              list

 L. 108       174  LOAD_GLOBAL              map

 L. 109       176  LOAD_CLOSURE             'dataset'
              178  BUILD_TUPLE_1         1 
              180  LOAD_LAMBDA              '<code_object <lambda>>'
              182  LOAD_STR                 'AircallConnector._get_data.<locals>.<lambda>'
              184  MAKE_FUNCTION_8          'closure'

 L. 110       186  LOAD_FAST                'data'
              188  LOAD_ATTR                get
              190  LOAD_DEREF               'dataset'
              192  CALL_FUNCTION_1       1  '1 positional argument'
              194  CALL_FUNCTION_2       2  '2 positional arguments'
              196  CALL_FUNCTION_1       1  '1 positional argument'
              198  INPLACE_ADD      
              200  STORE_FAST               'variable_response_list'
              202  JUMP_BACK           166  'to 166'
              204  POP_BLOCK        
            206_0  COME_FROM_LOOP      160  '160'
            206_1  COME_FROM           158  '158'

 L. 113       206  LOAD_FAST                'team_response_list'
              208  LOAD_FAST                'variable_response_list'
              210  BUILD_TUPLE_2         2 
              212  RETURN_VALUE     
            214_0  COME_FROM_ASYNC_WITH    28  '28'
              214  WITH_CLEANUP_START
              216  GET_AWAITABLE    
              218  LOAD_CONST               None
              220  YIELD_FROM       
              222  WITH_CLEANUP_FINISH
              224  END_FINALLY      

Parse error at or near `COME_FROM_ASYNC_WITH' instruction at offset 214_0

    async def _get_tags--- This code section failed: ---

 L. 117         0  LOAD_GLOBAL              BEARER_API_KEY
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                bearer_auth_id
                6  LOAD_CONST               ('Authorization', 'Bearer-Auth-Id')
                8  BUILD_CONST_KEY_MAP_2     2 
               10  STORE_FAST               'headers'

 L. 118        12  LOAD_GLOBAL              ClientSession
               14  LOAD_FAST                'headers'
               16  LOAD_CONST               ('headers',)
               18  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               20  BEFORE_ASYNC_WITH
               22  GET_AWAITABLE    
               24  LOAD_CONST               None
               26  YIELD_FROM       
               28  SETUP_ASYNC_WITH    102  'to 102'
               30  STORE_FAST               'session'

 L. 119        32  LOAD_GLOBAL              fetch_page
               34  LOAD_FAST                'dataset'
               36  BUILD_LIST_0          0 
               38  LOAD_FAST                'session'
               40  LOAD_FAST                'limit'
               42  LOAD_CONST               1
               44  CALL_FUNCTION_5       5  '5 positional arguments'
               46  GET_AWAITABLE    
               48  LOAD_CONST               None
               50  YIELD_FROM       
               52  STORE_FAST               'raw_data'

 L. 120        54  BUILD_LIST_0          0 
               56  STORE_FAST               'tags_data_list'

 L. 121        58  LOAD_GLOBAL              len
               60  LOAD_FAST                'raw_data'
               62  CALL_FUNCTION_1       1  '1 positional argument'
               64  LOAD_CONST               0
               66  COMPARE_OP               >
               68  POP_JUMP_IF_FALSE    98  'to 98'

 L. 122        70  SETUP_LOOP           98  'to 98'
               72  LOAD_FAST                'raw_data'
               74  GET_ITER         
               76  FOR_ITER             96  'to 96'
               78  STORE_FAST               'data'

 L. 123        80  LOAD_FAST                'tags_data_list'
               82  LOAD_FAST                'data'
               84  LOAD_ATTR                get
               86  LOAD_STR                 'tags'
               88  CALL_FUNCTION_1       1  '1 positional argument'
               90  INPLACE_ADD      
               92  STORE_FAST               'tags_data_list'
               94  JUMP_BACK            76  'to 76'
               96  POP_BLOCK        
             98_0  COME_FROM_LOOP       70  '70'
             98_1  COME_FROM            68  '68'

 L. 124        98  LOAD_FAST                'tags_data_list'
              100  RETURN_VALUE     
            102_0  COME_FROM_ASYNC_WITH    28  '28'
              102  WITH_CLEANUP_START
              104  GET_AWAITABLE    
              106  LOAD_CONST               None
              108  YIELD_FROM       
              110  WITH_CLEANUP_FINISH
              112  END_FINALLY      

Parse error at or near `COME_FROM_ASYNC_WITH' instruction at offset 102_0

    def run_fetches(self, dataset, limit) -> Tuple[(List[dict], List[dict])]:
        """sets up event loop and fetches for 'calls' and 'users' datasets"""
        loop = get_loop
        future = asyncio.ensure_future(self._get_data(dataset, limit))
        return loop.run_until_complete(future)

    def run_fetches_for_tags(self, dataset, limit):
        """sets up event loop and fetches for 'tags' dataset"""
        loop = get_loop
        future = asyncio.ensure_future(self._get_tags(dataset, limit))
        return loop.run_until_complete(future)

    def _retrieve_data(self, data_source: AircallDataSource) -> pd.DataFrame:
        """retrieves data from AirCall API"""
        dataset = data_source.dataset
        empty_df = build_empty_df(dataset)
        limit = data_source.limit
        if dataset == 'tags':
            non_empty_df = pd.DataFrame([])
            if limit != 0:
                res = self.run_fetches_for_tags(dataset, limit)
                non_empty_df = pd.DataFrame(res)
            return pd.concat([empty_df, non_empty_df])
        else:
            team_data = pd.DataFrame([])
            variable_data = pd.DataFrame([])
            if limit != 0:
                team_data, variable_data = self.run_fetches(dataset, limit)
            return build_df(dataset, [empty_df, pd.DataFrame(team_data), pd.DataFrame(variable_data)])