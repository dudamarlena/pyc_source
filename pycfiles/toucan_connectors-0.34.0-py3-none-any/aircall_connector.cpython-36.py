# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rachelle2/webprojects/toucan-connectors/toucan_connectors/aircall/aircall_connector.py
# Compiled at: 2020-04-23 04:23:41
# Size of source mod 2**32: 5579 bytes
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
               28  SETUP_ASYNC_WITH    206  'to 206'
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
               96  POP_JUMP_IF_FALSE   146  'to 146'

 L. 101        98  SETUP_LOOP          146  'to 146'
              100  LOAD_FAST                'team_data'
              102  GET_ITER         
              104  FOR_ITER            144  'to 144'
              106  STORE_FAST               'data'

 L. 102       108  SETUP_LOOP          142  'to 142'
              110  LOAD_FAST                'data'
              112  LOAD_STR                 'teams'
              114  BINARY_SUBSCR    
              116  GET_ITER         
              118  FOR_ITER            140  'to 140'
              120  STORE_FAST               'team_obj'

 L. 103       122  LOAD_FAST                'team_response_list'
              124  LOAD_GLOBAL              DICTIONARY_OF_FORMATTERS
              126  LOAD_STR                 'teams'
              128  BINARY_SUBSCR    
              130  LOAD_FAST                'team_obj'
              132  CALL_FUNCTION_1       1  '1 positional argument'
              134  INPLACE_ADD      
              136  STORE_FAST               'team_response_list'
              138  JUMP_BACK           118  'to 118'
              140  POP_BLOCK        
            142_0  COME_FROM_LOOP      108  '108'
              142  JUMP_BACK           104  'to 104'
              144  POP_BLOCK        
            146_0  COME_FROM_LOOP       98  '98'
            146_1  COME_FROM            96  '96'

 L. 105       146  LOAD_GLOBAL              len
              148  LOAD_FAST                'variable_data'
              150  CALL_FUNCTION_1       1  '1 positional argument'
              152  LOAD_CONST               0
              154  COMPARE_OP               >
              156  POP_JUMP_IF_FALSE   198  'to 198'

 L. 106       158  SETUP_LOOP          198  'to 198'
              160  LOAD_FAST                'variable_data'
              162  GET_ITER         
              164  FOR_ITER            196  'to 196'
              166  STORE_FAST               'data'

 L. 107       168  LOAD_FAST                'variable_response_list'

 L. 108       170  LOAD_CLOSURE             'dataset'
              172  BUILD_TUPLE_1         1 
              174  LOAD_LISTCOMP            '<code_object <listcomp>>'
              176  LOAD_STR                 'AircallConnector._get_data.<locals>.<listcomp>'
              178  MAKE_FUNCTION_8          'closure'
              180  LOAD_FAST                'data'
              182  LOAD_DEREF               'dataset'
              184  BINARY_SUBSCR    
              186  GET_ITER         
              188  CALL_FUNCTION_1       1  '1 positional argument'
              190  INPLACE_ADD      
              192  STORE_FAST               'variable_response_list'
              194  JUMP_BACK           164  'to 164'
              196  POP_BLOCK        
            198_0  COME_FROM_LOOP      158  '158'
            198_1  COME_FROM           156  '156'

 L. 110       198  LOAD_FAST                'team_response_list'
              200  LOAD_FAST                'variable_response_list'
              202  BUILD_TUPLE_2         2 
              204  RETURN_VALUE     
            206_0  COME_FROM_ASYNC_WITH    28  '28'
              206  WITH_CLEANUP_START
              208  GET_AWAITABLE    
              210  LOAD_CONST               None
              212  YIELD_FROM       
              214  WITH_CLEANUP_FINISH
              216  END_FINALLY      

Parse error at or near `COME_FROM_ASYNC_WITH' instruction at offset 206_0

    async def _get_tags--- This code section failed: ---

 L. 114         0  LOAD_GLOBAL              BEARER_API_KEY
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                bearer_auth_id
                6  LOAD_CONST               ('Authorization', 'Bearer-Auth-Id')
                8  BUILD_CONST_KEY_MAP_2     2 
               10  STORE_FAST               'headers'

 L. 115        12  LOAD_GLOBAL              ClientSession
               14  LOAD_FAST                'headers'
               16  LOAD_CONST               ('headers',)
               18  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               20  BEFORE_ASYNC_WITH
               22  GET_AWAITABLE    
               24  LOAD_CONST               None
               26  YIELD_FROM       
               28  SETUP_ASYNC_WITH     88  'to 88'
               30  STORE_FAST               'session'

 L. 116        32  LOAD_GLOBAL              fetch_page
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

 L. 117        54  BUILD_LIST_0          0 
               56  STORE_FAST               'tags_data_list'

 L. 118        58  SETUP_LOOP           84  'to 84'
               60  LOAD_FAST                'raw_data'
               62  GET_ITER         
               64  FOR_ITER             82  'to 82'
               66  STORE_FAST               'data'

 L. 119        68  LOAD_FAST                'tags_data_list'
               70  LOAD_FAST                'data'
               72  LOAD_STR                 'tags'
               74  BINARY_SUBSCR    
               76  INPLACE_ADD      
               78  STORE_FAST               'tags_data_list'
               80  JUMP_BACK            64  'to 64'
               82  POP_BLOCK        
             84_0  COME_FROM_LOOP       58  '58'

 L. 120        84  LOAD_FAST                'tags_data_list'
               86  RETURN_VALUE     
             88_0  COME_FROM_ASYNC_WITH    28  '28'
               88  WITH_CLEANUP_START
               90  GET_AWAITABLE    
               92  LOAD_CONST               None
               94  YIELD_FROM       
               96  WITH_CLEANUP_FINISH
               98  END_FINALLY      

Parse error at or near `COME_FROM_ASYNC_WITH' instruction at offset 88_0

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