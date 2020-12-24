# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rachelle2/webprojects/toucan-connectors/toucan_connectors/wootric/wootric_connector.py
# Compiled at: 2020-04-23 04:23:41
# Size of source mod 2**32: 4570 bytes
import asyncio, json
from datetime import datetime, timedelta
from itertools import chain
from typing import List, Optional
import pandas as pd, requests
from aiohttp import ClientSession
from toucan_connectors.common import get_loop
from toucan_connectors.toucan_connector import ToucanConnector, ToucanDataSource
_TOKEN_CACHE = None

async def fetch--- This code section failed: ---

 L.  19         0  LOAD_FAST                'session'
                2  LOAD_ATTR                get
                4  LOAD_FAST                'url'
                6  CALL_FUNCTION_1       1  '1 positional argument'
                8  BEFORE_ASYNC_WITH
               10  GET_AWAITABLE    
               12  LOAD_CONST               None
               14  YIELD_FROM       
               16  SETUP_ASYNC_WITH     40  'to 40'
               18  STORE_FAST               'response'

 L.  20        20  LOAD_GLOBAL              json
               22  LOAD_ATTR                loads
               24  LOAD_FAST                'response'
               26  LOAD_ATTR                read
               28  CALL_FUNCTION_0       0  '0 positional arguments'
               30  GET_AWAITABLE    
               32  LOAD_CONST               None
               34  YIELD_FROM       
               36  CALL_FUNCTION_1       1  '1 positional argument'
               38  RETURN_VALUE     
             40_0  COME_FROM_ASYNC_WITH    16  '16'
               40  WITH_CLEANUP_START
               42  GET_AWAITABLE    
               44  LOAD_CONST               None
               46  YIELD_FROM       
               48  WITH_CLEANUP_FINISH
               50  END_FINALLY      

Parse error at or near `COME_FROM_ASYNC_WITH' instruction at offset 40_0


async def _batch_fetch--- This code section failed: ---

 L.  25         0  LOAD_GLOBAL              ClientSession
                2  CALL_FUNCTION_0       0  '0 positional arguments'
                4  BEFORE_ASYNC_WITH
                6  GET_AWAITABLE    
                8  LOAD_CONST               None
               10  YIELD_FROM       
               12  SETUP_ASYNC_WITH     50  'to 50'
               14  STORE_DEREF              'session'

 L.  26        16  LOAD_CLOSURE             'session'
               18  BUILD_TUPLE_1         1 
               20  LOAD_GENEXPR             '<code_object <genexpr>>'
               22  LOAD_STR                 '_batch_fetch.<locals>.<genexpr>'
               24  MAKE_FUNCTION_8          'closure'
               26  LOAD_FAST                'urls'
               28  GET_ITER         
               30  CALL_FUNCTION_1       1  '1 positional argument'
               32  STORE_FAST               'tasks'

 L.  27        34  LOAD_GLOBAL              asyncio
               36  LOAD_ATTR                gather
               38  LOAD_FAST                'tasks'
               40  CALL_FUNCTION_EX      0  'positional arguments only'
               42  GET_AWAITABLE    
               44  LOAD_CONST               None
               46  YIELD_FROM       
               48  RETURN_VALUE     
             50_0  COME_FROM_ASYNC_WITH    12  '12'
               50  WITH_CLEANUP_START
               52  GET_AWAITABLE    
               54  LOAD_CONST               None
               56  YIELD_FROM       
               58  WITH_CLEANUP_FINISH
               60  END_FINALLY      

Parse error at or near `COME_FROM_ASYNC_WITH' instruction at offset 50_0


def batch_fetch(urls):
    """fetch asyncrhonously `urls` in a single batch"""
    loop = get_loop
    future = asyncio.ensure_future_batch_fetchurls
    return loop.run_until_completefuture


def fetch_wootric_data(query, props_fetched=None, batch_size=5, max_pages=30):
    """call the `query` wootric API endpoint and handle pagination

    Parameters:

    - `query`: the API endpoint, e.g. `'response'`

    - `props_fetched`: if specified, a list of properties to pick in the json documents
      returned by wootric

    - `batch_size`: number of requests to batch together. i.e. if `batch_size=5`, then the
      API will be queried by batches of 5 queries until data is exhausted or `max_pages`
      is reached.

    - `max_pages`: maximum number of pages to crawl.
    """
    all_data = []
    for page in range(1, max_pages + 1, batch_size):
        lastpage = min(page + batch_size, max_pages + 1)
        urls = [f"{query}&page={pagenum}" for pagenum in range(page, lastpage)]
        responses = batch_fetchurls
        data = chain.from_iterableresponses
        if props_fetched is None:
            all_data.extenddata
        else:
            all_data.extend[{prop:d[prop] for prop in props_fetched} for d in data]
        if not responses[(-1)]:
            break

    return all_data


def access_token(connector):
    """return OAUTH access token for connector `connector`

    This function handles a cache internally to avoid re-requesting the token
    if the one is cached is still valid.
    """
    global _TOKEN_CACHE
    if _TOKEN_CACHE is not None:
        token_infos = _TOKEN_CACHE
    else:
        token_infos = {}
    now = datetime.now
    if not token_infos or token_infos.get'expiration-date' < now:
        token_infos = connector.fetch_access_token
        _TOKEN_CACHE = token_infos
    return token_infos['access_token']


def wootric_url(route):
    """helper to build a full wootric API route, handling leading '/'

    >>> wootric_url('v1/responses')
    ''https://api.wootric.com/v1/responses'
    >>> wootric_url('/v1/responses')
    ''https://api.wootric.com/v1/responses'
    """
    route = route.lstrip'/'
    return f"https://api.wootric.com/{route}"


class WootricDataSource(ToucanDataSource):
    query: str
    properties = None
    properties: Optional[List[str]]
    batch_size: int = 5
    max_pages: int = 30


class WootricConnector(ToucanConnector):
    data_source_model: WootricDataSource
    client_id: str
    client_secret: str
    api_version: str = 'v1'

    def fetch_access_token(self):
        """fetch OAUH access token

        cf. https://docs.wootric.com/api/#authentication
        """
        response = requests.post((wootric_url'oauth/token'),
          data={'client_id':self.client_id, 
         'client_secret':self.client_secret, 
         'grant_type':'client_credentials'}).json
        return {'access_token':response['access_token'], 
         'expiration-date':datetime.now + timedelta(seconds=(intresponse['expires_in']))}

    def _retrieve_data(self, data_source: WootricDataSource) -> pd.DataFrame:
        """Return the concatenated data for all pages."""
        baseroute = wootric_urlf"{self.api_version}/{data_source.query}"
        query = f"{baseroute}?access_token={access_tokenself}"
        all_data = fetch_wootric_data(query,
          props_fetched=(data_source.properties),
          batch_size=(data_source.batch_size),
          max_pages=(data_source.max_pages))
        return pd.DataFrameall_data