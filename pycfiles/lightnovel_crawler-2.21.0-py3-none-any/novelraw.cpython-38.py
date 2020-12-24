# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: .\src\sources\novelraw.py
# Compiled at: 2020-05-04 19:43:29
# Size of source mod 2**32: 3461 bytes
import logging, re
from concurrent import futures
from urllib.parse import quote, urlparse
from utils.crawler import Crawler
logger = logging.getLogger('NOVELRAW_BLOGSPOT')
chapter_list_limit = 150
chapter_list_url = 'https://novelraw.blogspot.com/feeds/posts/default/-/%s?alt=json&start-index=%d&max-results=' + str(chapter_list_limit) + '&orderby=published'

class NovelRawCrawler(Crawler):
    base_url = 'https://novelraw.blogspot.com/'

    def read_novel_info--- This code section failed: ---

 L.  21         0  LOAD_GLOBAL              logger
                2  LOAD_METHOD              debug
                4  LOAD_STR                 'Visiting %s'
                6  LOAD_DEREF               'self'
                8  LOAD_ATTR                novel_url
               10  CALL_METHOD_2         2  ''
               12  POP_TOP          

 L.  22        14  LOAD_DEREF               'self'
               16  LOAD_METHOD              get_soup
               18  LOAD_DEREF               'self'
               20  LOAD_ATTR                novel_url
               22  CALL_METHOD_1         1  ''
               24  STORE_FAST               'soup'

 L.  24        26  LOAD_FAST                'soup'
               28  LOAD_METHOD              select
               30  LOAD_STR                 'script[type="text/javaScript"]'
               32  CALL_METHOD_1         1  ''
               34  GET_ITER         
             36_0  COME_FROM            66  '66'
               36  FOR_ITER             88  'to 88'
               38  STORE_FAST               'script'

 L.  25        40  LOAD_GLOBAL              re
               42  LOAD_METHOD              findall
               44  LOAD_STR                 'var label="([^"]+)";'
               46  LOAD_GLOBAL              str
               48  LOAD_FAST                'script'
               50  CALL_FUNCTION_1       1  ''
               52  CALL_METHOD_2         2  ''
               54  STORE_FAST               'text'

 L.  26        56  LOAD_GLOBAL              len
               58  LOAD_FAST                'text'
               60  CALL_FUNCTION_1       1  ''
               62  LOAD_CONST               1
               64  COMPARE_OP               ==
               66  POP_JUMP_IF_FALSE    36  'to 36'

 L.  27        68  LOAD_FAST                'text'
               70  LOAD_CONST               0
               72  BINARY_SUBSCR    
               74  LOAD_METHOD              strip
               76  CALL_METHOD_0         0  ''
               78  LOAD_DEREF               'self'
               80  STORE_ATTR               novel_title

 L.  28        82  POP_TOP          
               84  BREAK_LOOP           88  'to 88'
               86  JUMP_BACK            36  'to 36'

 L.  31        88  LOAD_GLOBAL              logger
               90  LOAD_METHOD              info
               92  LOAD_STR                 'Novel title: %s'
               94  LOAD_DEREF               'self'
               96  LOAD_ATTR                novel_title
               98  CALL_METHOD_2         2  ''
              100  POP_TOP          

 L.  33       102  LOAD_GLOBAL              chapter_list_url
              104  LOAD_DEREF               'self'
              106  LOAD_ATTR                novel_title
              108  LOAD_CONST               1
              110  BUILD_TUPLE_2         2 
              112  BINARY_MODULO    
              114  STORE_FAST               'url'

 L.  34       116  LOAD_GLOBAL              logger
              118  LOAD_METHOD              debug
              120  LOAD_STR                 'Visiting %s'
              122  LOAD_FAST                'url'
              124  CALL_METHOD_2         2  ''
              126  POP_TOP          

 L.  35       128  LOAD_DEREF               'self'
              130  LOAD_METHOD              get_json
              132  LOAD_FAST                'url'
              134  CALL_METHOD_1         1  ''
              136  STORE_FAST               'data'

 L.  36       138  LOAD_STR                 ', '
              140  LOAD_METHOD              join
              142  LOAD_LISTCOMP            '<code_object <listcomp>>'
              144  LOAD_STR                 'NovelRawCrawler.read_novel_info.<locals>.<listcomp>'
              146  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L.  37       148  LOAD_FAST                'data'
              150  LOAD_STR                 'feed'
              152  BINARY_SUBSCR    
              154  LOAD_STR                 'author'
              156  BINARY_SUBSCR    

 L.  36       158  GET_ITER         
              160  CALL_FUNCTION_1       1  ''
              162  CALL_METHOD_1         1  ''
              164  LOAD_DEREF               'self'
              166  STORE_ATTR               novel_author

 L.  39       168  LOAD_GLOBAL              logger
              170  LOAD_METHOD              info
              172  LOAD_STR                 'Novel author: %s'
              174  LOAD_DEREF               'self'
              176  LOAD_ATTR                novel_author
              178  CALL_METHOD_2         2  ''
              180  POP_TOP          

 L.  41       182  LOAD_FAST                'soup'
              184  LOAD_METHOD              select_one
              186  LOAD_STR                 '#tgtPost .separator img'
              188  CALL_METHOD_1         1  ''
              190  LOAD_STR                 'src'
              192  BINARY_SUBSCR    
              194  LOAD_DEREF               'self'
              196  STORE_ATTR               novel_cover

 L.  42       198  LOAD_GLOBAL              logger
              200  LOAD_METHOD              info
              202  LOAD_STR                 'Novel cover: %s'
              204  LOAD_DEREF               'self'
              206  LOAD_ATTR                novel_cover
              208  CALL_METHOD_2         2  ''
              210  POP_TOP          

 L.  44       212  LOAD_GLOBAL              int
              214  LOAD_FAST                'data'
              216  LOAD_STR                 'feed'
              218  BINARY_SUBSCR    
              220  LOAD_STR                 'openSearch$totalResults'
              222  BINARY_SUBSCR    
              224  LOAD_STR                 '$t'
              226  BINARY_SUBSCR    
              228  CALL_FUNCTION_1       1  ''
              230  STORE_FAST               'total_chapters'

 L.  45       232  LOAD_GLOBAL              logger
              234  LOAD_METHOD              info
              236  LOAD_STR                 'Total chapters = %d'
              238  LOAD_FAST                'total_chapters'
              240  CALL_METHOD_2         2  ''
              242  POP_TOP          

 L.  47       244  LOAD_GLOBAL              logger
              246  LOAD_METHOD              info
              248  LOAD_STR                 'Getting chapters...'
              250  CALL_METHOD_1         1  ''
              252  POP_TOP          

 L.  48       254  LOAD_CLOSURE             'self'
              256  BUILD_TUPLE_1         1 
              258  LOAD_DICTCOMP            '<code_object <dictcomp>>'
              260  LOAD_STR                 'NovelRawCrawler.read_novel_info.<locals>.<dictcomp>'
              262  MAKE_FUNCTION_8          'closure'

 L.  53       264  LOAD_GLOBAL              range
              266  LOAD_CONST               1
              268  LOAD_FAST                'total_chapters'
              270  LOAD_CONST               1
              272  BINARY_ADD       
              274  LOAD_GLOBAL              chapter_list_limit
              276  CALL_FUNCTION_3       3  ''

 L.  48       278  GET_ITER         
              280  CALL_FUNCTION_1       1  ''
              282  STORE_FAST               'futures_to_check'

 L.  55       284  LOAD_GLOBAL              dict
              286  CALL_FUNCTION_0       0  ''
              288  STORE_FAST               'all_entry'

 L.  56       290  LOAD_GLOBAL              futures
              292  LOAD_METHOD              as_completed
              294  LOAD_FAST                'futures_to_check'
              296  CALL_METHOD_1         1  ''
              298  GET_ITER         
              300  FOR_ITER            332  'to 332'
              302  STORE_FAST               'future'

 L.  57       304  LOAD_GLOBAL              int
              306  LOAD_FAST                'futures_to_check'
              308  LOAD_FAST                'future'
              310  BINARY_SUBSCR    
              312  CALL_FUNCTION_1       1  ''
              314  STORE_FAST               'page'

 L.  58       316  LOAD_FAST                'future'
              318  LOAD_METHOD              result
              320  CALL_METHOD_0         0  ''
              322  LOAD_FAST                'all_entry'
              324  LOAD_FAST                'page'
              326  STORE_SUBSCR     
          328_330  JUMP_BACK           300  'to 300'

 L.  61       332  LOAD_GLOBAL              reversed
              334  LOAD_GLOBAL              sorted
              336  LOAD_FAST                'all_entry'
              338  LOAD_METHOD              keys
              340  CALL_METHOD_0         0  ''
              342  CALL_FUNCTION_1       1  ''
              344  CALL_FUNCTION_1       1  ''
              346  GET_ITER         
              348  FOR_ITER            466  'to 466'
              350  STORE_FAST               'page'

 L.  62       352  LOAD_GLOBAL              reversed
              354  LOAD_FAST                'all_entry'
              356  LOAD_FAST                'page'
              358  BINARY_SUBSCR    
              360  CALL_FUNCTION_1       1  ''
              362  GET_ITER         
              364  FOR_ITER            462  'to 462'
              366  STORE_FAST               'entry'

 L.  63       368  LOAD_LISTCOMP            '<code_object <listcomp>>'
              370  LOAD_STR                 'NovelRawCrawler.read_novel_info.<locals>.<listcomp>'
              372  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L.  64       374  LOAD_FAST                'entry'
              376  LOAD_STR                 'link'
              378  BINARY_SUBSCR    

 L.  63       380  GET_ITER         
              382  CALL_FUNCTION_1       1  ''
              384  STORE_FAST               'possible_urls'

 L.  66       386  LOAD_GLOBAL              len
              388  LOAD_FAST                'possible_urls'
              390  CALL_FUNCTION_1       1  ''
          392_394  POP_JUMP_IF_TRUE    400  'to 400'

 L.  67   396_398  JUMP_BACK           364  'to 364'
            400_0  COME_FROM           392  '392'

 L.  69       400  LOAD_DEREF               'self'
              402  LOAD_ATTR                chapters
              404  LOAD_METHOD              append

 L.  70       406  LOAD_GLOBAL              len
              408  LOAD_DEREF               'self'
              410  LOAD_ATTR                chapters
              412  CALL_FUNCTION_1       1  ''
              414  LOAD_CONST               1
              416  BINARY_ADD       

 L.  71       418  LOAD_GLOBAL              len
              420  LOAD_DEREF               'self'
              422  LOAD_ATTR                chapters
              424  CALL_FUNCTION_1       1  ''
              426  LOAD_CONST               100
              428  BINARY_FLOOR_DIVIDE
              430  LOAD_CONST               1
              432  BINARY_ADD       

 L.  72       434  LOAD_FAST                'entry'
              436  LOAD_STR                 'title'
              438  BINARY_SUBSCR    
              440  LOAD_STR                 '$t'
              442  BINARY_SUBSCR    

 L.  73       444  LOAD_FAST                'possible_urls'
              446  LOAD_CONST               0
              448  BINARY_SUBSCR    

 L.  69       450  LOAD_CONST               ('id', 'volume', 'title', 'url')
              452  BUILD_CONST_KEY_MAP_4     4 
              454  CALL_METHOD_1         1  ''
              456  POP_TOP          
          458_460  JUMP_BACK           364  'to 364'
          462_464  JUMP_BACK           348  'to 348'

 L.  78       466  LOAD_LISTCOMP            '<code_object <listcomp>>'
              468  LOAD_STR                 'NovelRawCrawler.read_novel_info.<locals>.<listcomp>'
              470  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L.  79       472  LOAD_GLOBAL              range
              474  LOAD_GLOBAL              len
              476  LOAD_DEREF               'self'
              478  LOAD_ATTR                chapters
              480  CALL_FUNCTION_1       1  ''
              482  LOAD_CONST               100
              484  BINARY_FLOOR_DIVIDE
              486  LOAD_CONST               1
              488  BINARY_ADD       
              490  CALL_FUNCTION_1       1  ''

 L.  78       492  GET_ITER         
              494  CALL_FUNCTION_1       1  ''
              496  LOAD_DEREF               'self'
              498  STORE_ATTR               volumes

Parse error at or near `LOAD_DICTCOMP' instruction at offset 258

    def download_chapter_list(self, index):
        url = chapter_list_url % (self.novel_title, index)
        logger.debug'Visiting %s'url
        data = self.get_json(url)
        return data['feed']['entry']

    def download_chapter_body(self, chapter):
        logger.info'Visiting %s'chapter['url']
        soup = self.get_soup(chapter['url'])
        contents = self.extract_contents(soup.select_one('#tgtPost'))
        return '<p>' + '</p><p>'.join(contents) + '</p>'