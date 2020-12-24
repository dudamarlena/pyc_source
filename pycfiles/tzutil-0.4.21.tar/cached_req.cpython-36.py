# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n8f5s77x/tzutil/tzutil/cached_req.py
# Compiled at: 2018-12-04 01:36:04
# Size of source mod 2**32: 2047 bytes
import aiohttp, rocksdb
from time import time
import requests
from urllib.parse import urlparse
from os.path import join
from json import loads
from tzutil.req import get
import pathlib, struct

class Req:

    def __init__(self, path, expire=None, valid=lambda html: 1):
        self._path = path
        self.expire = expire
        self.valid = valid
        self._Req__db = {}
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)

    def _db(self, name):
        _db = self._Req__db
        db = _db.get(name)
        if not db:
            db = _db[name] = rocksdb.DB(join(self._path, name), rocksdb.Options(create_if_missing=True))
        return db

    def _cached(self, url):
        db = self._db(urlparse(url).netloc)
        _url = url.encode('utf-8')
        now = int(time())
        r = db.get(_url)
        if r:
            html = r[8:]
            if self.valid(html):
                expire = self.expire
                if expire:
                    cache_time = struct.unpack('Q', r[:8])[0]
                    if now - cache_time < expire:
                        return html
                else:
                    return html

        def put(html):
            db.put(_url, struct.pack('Q', now) + html)

        return put

    def get(self, url, *args, **kwds):
        html = self._cached(url)
        if type(html) is bytes:
            return html
        else:
            _put = html
            html = get(url, *args, **kwds)
            if not html:
                return
            html = html.content
            _put(html)
            return html

    async def async_get--- This code section failed: ---

 L.  67         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _cached
                4  LOAD_FAST                'url'
                6  CALL_FUNCTION_1       1  '1 positional argument'
                8  STORE_FAST               'html'

 L.  69        10  LOAD_GLOBAL              type
               12  LOAD_FAST                'html'
               14  CALL_FUNCTION_1       1  '1 positional argument'
               16  LOAD_GLOBAL              bytes
               18  COMPARE_OP               is
               20  POP_JUMP_IF_FALSE    26  'to 26'

 L.  70        22  LOAD_FAST                'html'
               24  RETURN_END_IF    
             26_0  COME_FROM            20  '20'

 L.  72        26  LOAD_FAST                'html'
               28  STORE_FAST               '_put'

 L.  74        30  LOAD_GLOBAL              aiohttp
               32  LOAD_ATTR                ClientSession
               34  LOAD_FAST                'kwds'
               36  LOAD_ATTR                get
               38  LOAD_STR                 'headers'
               40  CALL_FUNCTION_1       1  '1 positional argument'
               42  LOAD_CONST               ('headers',)
               44  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               46  BEFORE_ASYNC_WITH
               48  GET_AWAITABLE    
               50  LOAD_CONST               None
               52  YIELD_FROM       
               54  SETUP_ASYNC_WITH    120  'to 120'
               56  STORE_FAST               'session'

 L.  75        58  LOAD_FAST                'session'
               60  LOAD_ATTR                get
               62  LOAD_FAST                'url'
               64  CALL_FUNCTION_1       1  '1 positional argument'
               66  BEFORE_ASYNC_WITH
               68  GET_AWAITABLE    
               70  LOAD_CONST               None
               72  YIELD_FROM       
               74  SETUP_ASYNC_WITH    104  'to 104'
               76  STORE_FAST               'response'

 L.  76        78  LOAD_FAST                'response'
               80  LOAD_ATTR                read
               82  CALL_FUNCTION_0       0  '0 positional arguments'
               84  GET_AWAITABLE    
               86  LOAD_CONST               None
               88  YIELD_FROM       
               90  STORE_FAST               'html'

 L.  77        92  LOAD_FAST                '_put'
               94  LOAD_FAST                'html'
               96  CALL_FUNCTION_1       1  '1 positional argument'
               98  POP_TOP          

 L.  78       100  LOAD_FAST                'html'
              102  RETURN_VALUE     
            104_0  COME_FROM_ASYNC_WITH    74  '74'
              104  WITH_CLEANUP_START
              106  GET_AWAITABLE    
              108  LOAD_CONST               None
              110  YIELD_FROM       
              112  WITH_CLEANUP_FINISH
              114  END_FINALLY      
              116  POP_BLOCK        
              118  LOAD_CONST               None
            120_0  COME_FROM_ASYNC_WITH    54  '54'
              120  WITH_CLEANUP_START
              122  GET_AWAITABLE    
              124  LOAD_CONST               None
              126  YIELD_FROM       
              128  WITH_CLEANUP_FINISH
              130  END_FINALLY      

Parse error at or near `WITH_CLEANUP_FINISH' instruction at offset 128