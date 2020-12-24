# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: .\src\sources\lightnovelonline.py
# Compiled at: 2020-05-04 19:03:04
# Size of source mod 2**32: 3846 bytes
import logging, re
from concurrent import futures
from urllib.parse import urlparse
from utils.crawler import Crawler
logger = logging.getLogger('LIGHT_NOVEL_ONLINE')
search_url = 'https://light-novel.online/search.ajax?query=%s'
novel_page_url = 'https://light-novel.online/%s?page=%d'

class LightNovelOnline(Crawler):
    base_url = 'https://light-novel.online/'

    def search_novel(self, query):
        query = query.lower().replace(' ', '+')
        soup = self.get_soup(search_url % query)
        results = []
        for tr in soup.select('tr'):
            a = tr.select('td a')
            results.append({'title':a[0].text.strip(), 
             'url':self.absolute_url(a[0]['href']), 
             'info':a[1].text.strip()})
        else:
            return results

    def read_novel_info--- This code section failed: ---

 L.  36         0  LOAD_GLOBAL              logger
                2  LOAD_METHOD              debug
                4  LOAD_STR                 'Visiting %s'
                6  LOAD_DEREF               'self'
                8  LOAD_ATTR                novel_url
               10  CALL_METHOD_2         2  ''
               12  POP_TOP          

 L.  37        14  LOAD_DEREF               'self'
               16  LOAD_METHOD              get_soup
               18  LOAD_DEREF               'self'
               20  LOAD_ATTR                novel_url
               22  CALL_METHOD_1         1  ''
               24  STORE_FAST               'soup'

 L.  39        26  LOAD_GLOBAL              urlparse
               28  LOAD_DEREF               'self'
               30  LOAD_ATTR                novel_url
               32  CALL_FUNCTION_1       1  ''
               34  LOAD_ATTR                path
               36  LOAD_METHOD              split
               38  LOAD_STR                 '/'
               40  CALL_METHOD_1         1  ''
               42  LOAD_CONST               1
               44  BINARY_SUBSCR    
               46  LOAD_DEREF               'self'
               48  STORE_ATTR               novel_id

 L.  40        50  LOAD_GLOBAL              logger
               52  LOAD_METHOD              info
               54  LOAD_STR                 'Novel Id: %s'
               56  LOAD_DEREF               'self'
               58  LOAD_ATTR                novel_id
               60  CALL_METHOD_2         2  ''
               62  POP_TOP          

 L.  42        64  LOAD_FAST                'soup'
               66  LOAD_METHOD              select_one

 L.  43        68  LOAD_STR                 '.series-details .series-name a'

 L.  42        70  CALL_METHOD_1         1  ''
               72  LOAD_ATTR                text
               74  LOAD_METHOD              strip
               76  CALL_METHOD_0         0  ''
               78  LOAD_DEREF               'self'
               80  STORE_ATTR               novel_title

 L.  44        82  LOAD_GLOBAL              logger
               84  LOAD_METHOD              info
               86  LOAD_STR                 'Novel title: %s'
               88  LOAD_DEREF               'self'
               90  LOAD_ATTR                novel_title
               92  CALL_METHOD_2         2  ''
               94  POP_TOP          

 L.  46        96  LOAD_DEREF               'self'
               98  LOAD_METHOD              absolute_url

 L.  47       100  LOAD_FAST                'soup'
              102  LOAD_METHOD              select_one
              104  LOAD_STR                 '.series-cover .content'
              106  CALL_METHOD_1         1  ''
              108  LOAD_STR                 'data-src'
              110  BINARY_SUBSCR    

 L.  46       112  CALL_METHOD_1         1  ''
              114  LOAD_DEREF               'self'
              116  STORE_ATTR               novel_cover

 L.  48       118  LOAD_GLOBAL              logger
              120  LOAD_METHOD              info
              122  LOAD_STR                 'Novel cover: %s'
              124  LOAD_DEREF               'self'
              126  LOAD_ATTR                novel_cover
              128  CALL_METHOD_2         2  ''
              130  POP_TOP          

 L.  53       132  LOAD_CONST               1
              134  STORE_FAST               'page_count'

 L.  54       136  SETUP_FINALLY       178  'to 178'

 L.  55       138  LOAD_FAST                'soup'
              140  LOAD_METHOD              select
              142  LOAD_STR                 'ul.pagingnation li a'
              144  CALL_METHOD_1         1  ''
              146  LOAD_CONST               -1
              148  BINARY_SUBSCR    
              150  LOAD_STR                 'title'
              152  BINARY_SUBSCR    
              154  STORE_FAST               'last_page'

 L.  56       156  LOAD_GLOBAL              int
              158  LOAD_FAST                'last_page'
              160  LOAD_METHOD              split
              162  LOAD_STR                 ' '
              164  CALL_METHOD_1         1  ''
              166  LOAD_CONST               -1
              168  BINARY_SUBSCR    
              170  CALL_FUNCTION_1       1  ''
              172  STORE_FAST               'page_count'
              174  POP_BLOCK        
              176  JUMP_FORWARD        226  'to 226'
            178_0  COME_FROM_FINALLY   136  '136'

 L.  57       178  DUP_TOP          
              180  LOAD_GLOBAL              Exception
              182  COMPARE_OP               exception-match
              184  POP_JUMP_IF_FALSE   224  'to 224'
              186  POP_TOP          
              188  STORE_FAST               'err'
              190  POP_TOP          
              192  SETUP_FINALLY       212  'to 212'

 L.  58       194  LOAD_GLOBAL              logger
              196  LOAD_METHOD              exception
              198  LOAD_STR                 'Failed to get page-count: %s'
              200  LOAD_DEREF               'self'
              202  LOAD_ATTR                novel_url
              204  CALL_METHOD_2         2  ''
              206  POP_TOP          
              208  POP_BLOCK        
              210  BEGIN_FINALLY    
            212_0  COME_FROM_FINALLY   192  '192'
              212  LOAD_CONST               None
              214  STORE_FAST               'err'
              216  DELETE_FAST              'err'
              218  END_FINALLY      
              220  POP_EXCEPT       
              222  JUMP_FORWARD        226  'to 226'
            224_0  COME_FROM           184  '184'
              224  END_FINALLY      
            226_0  COME_FROM           222  '222'
            226_1  COME_FROM           176  '176'

 L.  60       226  LOAD_GLOBAL              logger
              228  LOAD_METHOD              info
              230  LOAD_STR                 'Total pages: %d'
              232  LOAD_FAST                'page_count'
              234  CALL_METHOD_2         2  ''
              236  POP_TOP          

 L.  62       238  LOAD_GLOBAL              logger
              240  LOAD_METHOD              info
              242  LOAD_STR                 'Getting chapters...'
              244  CALL_METHOD_1         1  ''
              246  POP_TOP          

 L.  63       248  LOAD_CLOSURE             'self'
              250  BUILD_TUPLE_1         1 
              252  LOAD_DICTCOMP            '<code_object <dictcomp>>'
              254  LOAD_STR                 'LightNovelOnline.read_novel_info.<locals>.<dictcomp>'
              256  MAKE_FUNCTION_8          'closure'

 L.  68       258  LOAD_GLOBAL              range
              260  LOAD_FAST                'page_count'
              262  CALL_FUNCTION_1       1  ''

 L.  63       264  GET_ITER         
              266  CALL_FUNCTION_1       1  ''
              268  STORE_FAST               'futures_to_check'

 L.  70       270  LOAD_GLOBAL              dict
              272  CALL_FUNCTION_0       0  ''
              274  STORE_FAST               'temp_chapters'

 L.  71       276  LOAD_GLOBAL              futures
              278  LOAD_METHOD              as_completed
              280  LOAD_FAST                'futures_to_check'
              282  CALL_METHOD_1         1  ''
              284  GET_ITER         
              286  FOR_ITER            318  'to 318'
              288  STORE_FAST               'future'

 L.  72       290  LOAD_GLOBAL              int
              292  LOAD_FAST                'futures_to_check'
              294  LOAD_FAST                'future'
              296  BINARY_SUBSCR    
              298  CALL_FUNCTION_1       1  ''
              300  STORE_FAST               'page'

 L.  73       302  LOAD_FAST                'future'
              304  LOAD_METHOD              result
              306  CALL_METHOD_0         0  ''
              308  LOAD_FAST                'temp_chapters'
              310  LOAD_FAST                'page'
              312  STORE_SUBSCR     
          314_316  JUMP_BACK           286  'to 286'

 L.  76       318  LOAD_GLOBAL              logger
              320  LOAD_METHOD              info
              322  LOAD_STR                 'Building sorted chapter list...'
              324  CALL_METHOD_1         1  ''
              326  POP_TOP          

 L.  77       328  LOAD_GLOBAL              reversed
              330  LOAD_GLOBAL              sorted
              332  LOAD_FAST                'temp_chapters'
              334  LOAD_METHOD              keys
              336  CALL_METHOD_0         0  ''
              338  CALL_FUNCTION_1       1  ''
              340  CALL_FUNCTION_1       1  ''
              342  GET_ITER         
              344  FOR_ITER            424  'to 424'
              346  STORE_FAST               'page'

 L.  78       348  LOAD_GLOBAL              reversed
              350  LOAD_FAST                'temp_chapters'
              352  LOAD_FAST                'page'
              354  BINARY_SUBSCR    
              356  CALL_FUNCTION_1       1  ''
              358  GET_ITER         
              360  FOR_ITER            420  'to 420'
              362  STORE_FAST               'chap'

 L.  79       364  LOAD_GLOBAL              len
              366  LOAD_DEREF               'self'
              368  LOAD_ATTR                chapters
              370  CALL_FUNCTION_1       1  ''
              372  LOAD_CONST               1
              374  BINARY_ADD       
              376  LOAD_FAST                'chap'
              378  LOAD_STR                 'id'
              380  STORE_SUBSCR     

 L.  80       382  LOAD_GLOBAL              len
              384  LOAD_DEREF               'self'
              386  LOAD_ATTR                chapters
              388  CALL_FUNCTION_1       1  ''
              390  LOAD_CONST               100
              392  BINARY_FLOOR_DIVIDE
              394  LOAD_CONST               1
              396  BINARY_ADD       
              398  LOAD_FAST                'chap'
              400  LOAD_STR                 'volume'
              402  STORE_SUBSCR     

 L.  81       404  LOAD_DEREF               'self'
              406  LOAD_ATTR                chapters
              408  LOAD_METHOD              append
              410  LOAD_FAST                'chap'
              412  CALL_METHOD_1         1  ''
              414  POP_TOP          
          416_418  JUMP_BACK           360  'to 360'
          420_422  JUMP_BACK           344  'to 344'

 L.  85       424  LOAD_LISTCOMP            '<code_object <listcomp>>'
              426  LOAD_STR                 'LightNovelOnline.read_novel_info.<locals>.<listcomp>'
              428  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L.  86       430  LOAD_GLOBAL              range
              432  LOAD_CONST               1
              434  LOAD_GLOBAL              len
              436  LOAD_DEREF               'self'
              438  LOAD_ATTR                chapters
              440  CALL_FUNCTION_1       1  ''
              442  LOAD_CONST               100
              444  BINARY_FLOOR_DIVIDE
              446  BINARY_ADD       
              448  CALL_FUNCTION_1       1  ''

 L.  85       450  GET_ITER         
              452  CALL_FUNCTION_1       1  ''
              454  LOAD_DEREF               'self'
              456  STORE_ATTR               volumes

Parse error at or near `LOAD_DICTCOMP' instruction at offset 252

    def extract_chapter_list(self, page):
        url = novel_page_url % (self.novel_id, page)
        logger.debug('Getting chapter list: %s', url)
        soup = self.get_soup(url)
        temp_list = []
        for a in soup.select('ul.list-chapters .chapter-name a'):
            temp_list.append({'title':a.text.strip(), 
             'url':self.absolute_url('/' + a['href'].strip('/'))})
        else:
            return temp_list

    def download_chapter_body(self, chapter):
        """Download body of a single chapter and return as clean html format."""
        logger.info('Downloading %s', chapter['url'])
        soup = self.get_soup(chapter['url'])
        body = soup.select('#chapter-content p')
        return ''.join([str(p) for p in body if p.text.strip()])