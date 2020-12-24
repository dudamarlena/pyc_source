# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nsfw_dl/dl.py
# Compiled at: 2017-09-19 09:41:52
# Size of source mod 2**32: 5925 bytes
"""
Read the license at:
https://github.com/IzunaDevs/nsfw_dl/blob/master/LICENSE
"""
import importlib, io, json
from urllib.parse import quote
import aiohttp
from bs4 import BeautifulSoup
import requests
from .errors import NoLoader, UnsupportedDataFormat
LOADERS = {'danbooru':[
  'DanbooruRandom', 'DanbooruSearch'], 
 'drunkenpumken':[
  'DrunkenpumkenRandom'], 
 'e621':[
  'E621Random', 'E621Search'], 
 'furrybooru':[
  'FurrybooruRandom', 'FurrybooruSearch'], 
 'gelbooru':[
  'GelbooruRandom', 'GelbooruSearch'], 
 'hbrowse':[
  'HbrowseRandom'], 
 'konachan':[
  'KonachanRandom', 'KonachanSearch'], 
 'lolibooru':[
  'LolibooruRandom', 'LolibooruSearch'], 
 'nhentai':[
  'NhentaiRandom'], 
 'rule34':[
  'Rule34Random', 'Rule34Search'], 
 'tbib':[
  'TbibRandom', 'TbibSearch'], 
 'tsumino':[
  'TsuminoRandom'], 
 'xbooru':[
  'XbooruRandom', 'XbooruSearch'], 
 'yandere':[
  'YandereRandom', 'YandereSearch']}

class NSFWDL:
    __doc__ = '\n    Main class.\n    '

    def __init__(self, session=None, loop=None, json_loader=json.loads):
        self.async_ = None
        self.loop = loop
        self.session = session
        self.json_loader = json_loader
        self.loaders = {}
        self.load_default()

    def add_loader(self, name, downloader):
        """
        adds a loader to get images from.
        """
        self.loaders[name] = downloader

    @staticmethod
    def parse_args(args):
        """
        parses args.
        """
        return quote(args)

    async def __aenter__(self):
        if self.async_ is not True:
            if self.async_ is False:
                self.session.close()
            self.session = aiohttp.ClientSession(loop=(self.loop))
        self.async_ = True
        return self

    async def __aexit__(self, *exc):
        pass

    def __enter__(self):
        if self.async_ is not False:
            if self.async_ is True:
                self.session.close()
            self.session = requests.Session()
        self.async_ = False
        return self

    def __exit__(self, *exc):
        pass

    def __del__(self):
        self.session.close()

    def __getattr__(self, item):
        if item in self.loaders:
            return self.loaders[item]

    async def get_async--- This code section failed: ---

 L.  90         0  LOAD_FAST                'self'
                2  LOAD_ATTR                session
                4  LOAD_ATTR                get
                6  LOAD_FAST                'url'
                8  CALL_FUNCTION_1       1  '1 positional argument'
               10  BEFORE_ASYNC_WITH
               12  GET_AWAITABLE    
               14  LOAD_CONST               None
               16  YIELD_FROM       
               18  SETUP_ASYNC_WITH     36  'to 36'
               20  STORE_FAST               'resp'

 L.  91        22  LOAD_FAST                'resp'
               24  LOAD_ATTR                read
               26  CALL_FUNCTION_0       0  '0 positional arguments'
               28  GET_AWAITABLE    
               30  LOAD_CONST               None
               32  YIELD_FROM       
               34  RETURN_VALUE     
             36_0  COME_FROM_ASYNC_WITH    18  '18'
               36  WITH_CLEANUP_START
               38  GET_AWAITABLE    
               40  LOAD_CONST               None
               42  YIELD_FROM       
               44  WITH_CLEANUP_FINISH
               46  END_FINALLY      

Parse error at or near `COME_FROM_ASYNC_WITH' instruction at offset 36_0

    def get_sync(self, url):
        with self.session.get(url) as (resp):
            return resp.content

    def get(self, url):
        if self.async_:
            return self.get_async(url)
        else:
            return self.get_sync(url)

    async def download_async--- This code section failed: ---

 L. 102         0  LOAD_GLOBAL              getattr
                2  LOAD_FAST                'loader'
                4  LOAD_STR                 'reqtype'
                6  LOAD_CONST               None
                8  CALL_FUNCTION_3       3  '3 positional arguments'
               10  STORE_FAST               'reqtype'

 L. 103        12  LOAD_FAST                'reqtype'
               14  LOAD_CONST               None
               16  COMPARE_OP               is
               18  POP_JUMP_IF_FALSE    24  'to 24'

 L. 104        20  LOAD_STR                 'get'
               22  STORE_FAST               'reqtype'
             24_0  COME_FROM            18  '18'

 L. 105        24  LOAD_GLOBAL              getattr
               26  LOAD_FAST                'self'
               28  LOAD_ATTR                session
               30  LOAD_FAST                'reqtype'
               32  CALL_FUNCTION_2       2  '2 positional arguments'
               34  STORE_FAST               'reqmeth'

 L. 107        36  LOAD_FAST                'reqmeth'
               38  LOAD_FAST                'url'
               40  LOAD_FAST                'data'
               42  LOAD_FAST                'headers'
               44  LOAD_CONST               ('data', 'headers')
               46  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               48  BEFORE_ASYNC_WITH
               50  GET_AWAITABLE    
               52  LOAD_CONST               None
               54  YIELD_FROM       
               56  SETUP_ASYNC_WITH    218  'to 218'
               58  STORE_FAST               'resp'

 L. 108        60  LOAD_CONST               200
               62  LOAD_FAST                'resp'
               64  LOAD_ATTR                status
               66  DUP_TOP          
               68  ROT_THREE        
               70  COMPARE_OP               <=
               72  JUMP_IF_FALSE_OR_POP    80  'to 80'
               74  LOAD_CONST               300
               76  COMPARE_OP               <
               78  JUMP_FORWARD         84  'to 84'
             80_0  COME_FROM            72  '72'
               80  ROT_TWO          
               82  POP_TOP          
             84_0  COME_FROM            78  '78'
               84  POP_JUMP_IF_TRUE     90  'to 90'
               86  LOAD_ASSERT              AssertionError
               88  RAISE_VARARGS_1       1  'exception'
             90_0  COME_FROM            84  '84'

 L. 110        90  LOAD_FAST                'loader'
               92  LOAD_ATTR                data_format
               94  LOAD_STR                 'bs4/html'
               96  COMPARE_OP               ==
               98  POP_JUMP_IF_FALSE   122  'to 122'

 L. 111       100  LOAD_GLOBAL              BeautifulSoup
              102  LOAD_FAST                'resp'
              104  LOAD_ATTR                text
              106  CALL_FUNCTION_0       0  '0 positional arguments'
              108  GET_AWAITABLE    
              110  LOAD_CONST               None
              112  YIELD_FROM       
              114  LOAD_STR                 'html.parser'
              116  CALL_FUNCTION_2       2  '2 positional arguments'
              118  STORE_FAST               'reqdata'
              120  JUMP_FORWARD        214  'to 214'
              122  ELSE                     '214'

 L. 113       122  LOAD_FAST                'loader'
              124  LOAD_ATTR                data_format
              126  LOAD_STR                 'bs4/xml'
              128  COMPARE_OP               ==
              130  POP_JUMP_IF_FALSE   154  'to 154'

 L. 114       132  LOAD_GLOBAL              BeautifulSoup
              134  LOAD_FAST                'resp'
              136  LOAD_ATTR                text
              138  CALL_FUNCTION_0       0  '0 positional arguments'
              140  GET_AWAITABLE    
              142  LOAD_CONST               None
              144  YIELD_FROM       
              146  LOAD_STR                 'lxml'
              148  CALL_FUNCTION_2       2  '2 positional arguments'
              150  STORE_FAST               'reqdata'
              152  JUMP_FORWARD        214  'to 214'
              154  ELSE                     '214'

 L. 116       154  LOAD_FAST                'loader'
              156  LOAD_ATTR                data_format
              158  LOAD_STR                 'json'
              160  COMPARE_OP               ==
              162  POP_JUMP_IF_FALSE   186  'to 186'

 L. 117       164  LOAD_FAST                'resp'
              166  LOAD_ATTR                json
              168  LOAD_FAST                'self'
              170  LOAD_ATTR                json_loader
              172  LOAD_CONST               ('loads',)
              174  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              176  GET_AWAITABLE    
              178  LOAD_CONST               None
              180  YIELD_FROM       
              182  STORE_FAST               'reqdata'
              184  JUMP_FORWARD        214  'to 214'
              186  ELSE                     '214'

 L. 119       186  LOAD_FAST                'loader'
              188  LOAD_ATTR                data_format
              190  LOAD_STR                 'url'
              192  COMPARE_OP               ==
              194  POP_JUMP_IF_FALSE   204  'to 204'

 L. 120       196  LOAD_FAST                'loader'
              198  LOAD_ATTR                data_format
              200  STORE_FAST               'reqdata'
              202  JUMP_FORWARD        214  'to 214'
              204  ELSE                     '214'

 L. 123       204  LOAD_GLOBAL              UnsupportedDataFormat
              206  LOAD_FAST                'loader'
              208  LOAD_ATTR                data_format
              210  CALL_FUNCTION_1       1  '1 positional argument'
              212  RAISE_VARARGS_1       1  'exception'
            214_0  COME_FROM           202  '202'
            214_1  COME_FROM           184  '184'
            214_2  COME_FROM           152  '152'
            214_3  COME_FROM           120  '120'
              214  POP_BLOCK        
              216  LOAD_CONST               None
            218_0  COME_FROM_ASYNC_WITH    56  '56'
              218  WITH_CLEANUP_START
              220  GET_AWAITABLE    
              222  LOAD_CONST               None
              224  YIELD_FROM       
              226  WITH_CLEANUP_FINISH
              228  END_FINALLY      

 L. 125       230  LOAD_FAST                'reqdata'
              232  LOAD_STR                 'url'
              234  COMPARE_OP               ==
              236  POP_JUMP_IF_FALSE   246  'to 246'

 L. 126       238  LOAD_FAST                'resp'
              240  LOAD_ATTR                url
              242  STORE_FAST               'img_url'
              244  JUMP_FORWARD        256  'to 256'
              246  ELSE                     '256'

 L. 129       246  LOAD_FAST                'loader'
              248  LOAD_ATTR                get_image
              250  LOAD_FAST                'reqdata'
              252  CALL_FUNCTION_1       1  '1 positional argument'
              254  STORE_FAST               'img_url'
            256_0  COME_FROM           244  '244'

 L. 131       256  LOAD_FAST                'download'
              258  POP_JUMP_IF_FALSE   350  'to 350'

 L. 132       262  LOAD_FAST                'self'
              264  LOAD_ATTR                session
              266  LOAD_ATTR                get
              268  LOAD_FAST                'img_url'
              270  CALL_FUNCTION_1       1  '1 positional argument'
              272  BEFORE_ASYNC_WITH
              274  GET_AWAITABLE    
              276  LOAD_CONST               None
              278  YIELD_FROM       
              280  SETUP_ASYNC_WITH    338  'to 338'
              282  STORE_FAST               'resp'

 L. 133       284  LOAD_CONST               200
              286  LOAD_FAST                'resp'
              288  LOAD_ATTR                status
              290  DUP_TOP          
              292  ROT_THREE        
              294  COMPARE_OP               <=
              296  JUMP_IF_FALSE_OR_POP   306  'to 306'
              300  LOAD_CONST               300
              302  COMPARE_OP               <
              304  JUMP_FORWARD        310  'to 310'
            306_0  COME_FROM           296  '296'
              306  ROT_TWO          
              308  POP_TOP          
            310_0  COME_FROM           304  '304'
              310  POP_JUMP_IF_TRUE    318  'to 318'
              314  LOAD_ASSERT              AssertionError
              316  RAISE_VARARGS_1       1  'exception'
            318_0  COME_FROM           310  '310'

 L. 134       318  LOAD_GLOBAL              io
              320  LOAD_ATTR                BytesIO
              322  LOAD_FAST                'resp'
              324  LOAD_ATTR                read
              326  CALL_FUNCTION_0       0  '0 positional arguments'
              328  GET_AWAITABLE    
              330  LOAD_CONST               None
              332  YIELD_FROM       
              334  CALL_FUNCTION_1       1  '1 positional argument'
              336  RETURN_VALUE     
            338_0  COME_FROM_ASYNC_WITH   280  '280'
              338  WITH_CLEANUP_START
              340  GET_AWAITABLE    
              342  LOAD_CONST               None
              344  YIELD_FROM       
              346  WITH_CLEANUP_FINISH
              348  END_FINALLY      
            350_0  COME_FROM           258  '258'

 L. 136       350  LOAD_FAST                'img_url'
              352  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM_ASYNC_WITH' instruction at offset 338_0

    def download_sync(self, url, data, headers, loader, download=False):
        """ sync downloader. """
        reqtype = getattrloader'reqtype'None
        if reqtype is None:
            reqtype = 'get'
        else:
            reqmeth = getattr(self.session, reqtype)
            resp = reqmeth(url, data=data, headers=headers)
            assert 200 <= resp.status_code < 300
            if loader.data_format == 'bs4/html':
                reqdata = BeautifulSoup(resp.text, 'html.parser')
            else:
                if loader.data_format == 'bs4/xml':
                    reqdata = BeautifulSoup(resp.text, 'lxml')
                else:
                    if loader.data_format == 'json':
                        reqdata = self.json_loader(resp.text)
                    else:
                        if loader.data_format == 'url':
                            reqdata = loader.data_format
                        else:
                            raise UnsupportedDataFormat(loader.data_format)
            if reqdata == 'url':
                img_url = resp.url
            else:
                img_url = loader.get_image(reqdata)
        if download:
            resp = self.session.get(img_url)
            assert 200 <= resp.status < 300
            return io.BytesIO(resp.content)
        else:
            return img_url

    def download(self, name, args='', download=False):
        """
        downloads or returns the image urls based on the loaders.
        """
        if name not in self.loaders:
            raise NoLoader(f"No loader named {name!r}")
        loader = self.loaders[name]
        args = self.parse_args(args)
        url, data, headers = loader.prepare_url(args=args)
        if self.async_:
            return self.download_async(url, data, headers, loader, download)
        else:
            return self.download_sync(url, data, headers, loader, download)

    def load_default(self):
        """
        loads the loaders.
        """
        for loader, names in LOADERS.items():
            lib = importlib.import_module(f"nsfw_dl.loaders.{loader}")
            for name, loader_class in [(name, getattr(lib, name)) for name in names]:
                load_obj = loader_class()
                self.add_loader(name, load_obj)