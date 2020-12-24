# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: .\src\sources\rewayatclub.py
# Compiled at: 2020-03-25 09:13:24
# Size of source mod 2**32: 2877 bytes
import logging, re
from concurrent import futures
from utils.crawler import Crawler
logger = logging.getLogger('REWAYAT_CLUB')

class RewayatClubCrawler(Crawler):
    base_url = 'https://rewayat.club/'

    def read_novel_info--- This code section failed: ---

 L.  15         0  LOAD_GLOBAL              logger
                2  LOAD_METHOD              debug
                4  LOAD_STR                 'Visiting %s'
                6  LOAD_DEREF               'self'
                8  LOAD_ATTR                novel_url
               10  CALL_METHOD_2         2  ''
               12  POP_TOP          

 L.  16        14  LOAD_DEREF               'self'
               16  LOAD_METHOD              get_soup
               18  LOAD_DEREF               'self'
               20  LOAD_ATTR                novel_url
               22  CALL_METHOD_1         1  ''
               24  STORE_FAST               'soup'

 L.  18        26  LOAD_CONST               True
               28  LOAD_DEREF               'self'
               30  STORE_ATTR               is_rtl

 L.  20        32  LOAD_FAST                'soup'
               34  LOAD_METHOD              select_one
               36  LOAD_STR                 'h1.card-header'
               38  CALL_METHOD_1         1  ''
               40  LOAD_ATTR                text
               42  LOAD_METHOD              strip
               44  CALL_METHOD_0         0  ''
               46  LOAD_DEREF               'self'
               48  STORE_ATTR               novel_title

 L.  21        50  LOAD_GLOBAL              logger
               52  LOAD_METHOD              info
               54  LOAD_STR                 'Novel title: %s'
               56  LOAD_DEREF               'self'
               58  LOAD_ATTR                novel_title
               60  CALL_METHOD_2         2  ''
               62  POP_TOP          

 L.  23        64  LOAD_DEREF               'self'
               66  LOAD_METHOD              absolute_url

 L.  24        68  LOAD_FAST                'soup'
               70  LOAD_METHOD              select_one
               72  LOAD_STR                 '.card-body .align-middle img'
               74  CALL_METHOD_1         1  ''
               76  LOAD_STR                 'src'
               78  BINARY_SUBSCR    

 L.  23        80  CALL_METHOD_1         1  ''
               82  LOAD_DEREF               'self'
               84  STORE_ATTR               novel_cover

 L.  25        86  LOAD_GLOBAL              logger
               88  LOAD_METHOD              info
               90  LOAD_STR                 'Novel cover: %s'
               92  LOAD_DEREF               'self'
               94  LOAD_ATTR                novel_cover
               96  CALL_METHOD_2         2  ''
               98  POP_TOP          

 L.  27       100  LOAD_FAST                'soup'
              102  LOAD_METHOD              select_one

 L.  28       104  LOAD_STR                 '.card-body table td a[href*="/user/"]'

 L.  27       106  CALL_METHOD_1         1  ''
              108  LOAD_ATTR                text
              110  LOAD_METHOD              strip
              112  CALL_METHOD_0         0  ''
              114  LOAD_DEREF               'self'
              116  STORE_ATTR               novel_author

 L.  29       118  LOAD_GLOBAL              logger
              120  LOAD_METHOD              info
              122  LOAD_STR                 'Novel author: %s'
              124  LOAD_DEREF               'self'
              126  LOAD_ATTR                novel_author
              128  CALL_METHOD_2         2  ''
              130  POP_TOP          

 L.  31       132  LOAD_GLOBAL              len
              134  LOAD_FAST                'soup'
              136  LOAD_METHOD              select

 L.  32       138  LOAD_STR                 '.card-footer select.custom-select option'

 L.  31       140  CALL_METHOD_1         1  ''
              142  CALL_FUNCTION_1       1  ''
              144  STORE_FAST               'page_count'

 L.  33       146  LOAD_GLOBAL              logger
              148  LOAD_METHOD              info
              150  LOAD_STR                 'Total pages: %d'
              152  LOAD_FAST                'page_count'
              154  CALL_METHOD_2         2  ''
              156  POP_TOP          

 L.  35       158  LOAD_GLOBAL              logger
              160  LOAD_METHOD              info
              162  LOAD_STR                 'Getting chapters...'
              164  CALL_METHOD_1         1  ''
              166  POP_TOP          

 L.  36       168  LOAD_CLOSURE             'self'
              170  BUILD_TUPLE_1         1 
              172  LOAD_DICTCOMP            '<code_object <dictcomp>>'
              174  LOAD_STR                 'RewayatClubCrawler.read_novel_info.<locals>.<dictcomp>'
              176  MAKE_FUNCTION_8          'closure'

 L.  38       178  LOAD_GLOBAL              range
              180  LOAD_FAST                'page_count'
              182  CALL_FUNCTION_1       1  ''

 L.  36       184  GET_ITER         
              186  CALL_FUNCTION_1       1  ''
              188  STORE_FAST               'futures_to_check'

 L.  40       190  LOAD_GLOBAL              dict
              192  CALL_FUNCTION_0       0  ''
              194  STORE_FAST               'temp_chapters'

 L.  41       196  LOAD_GLOBAL              futures
              198  LOAD_METHOD              as_completed
              200  LOAD_FAST                'futures_to_check'
              202  CALL_METHOD_1         1  ''
              204  GET_ITER         
              206  FOR_ITER            236  'to 236'
              208  STORE_FAST               'future'

 L.  42       210  LOAD_GLOBAL              int
              212  LOAD_FAST                'futures_to_check'
              214  LOAD_FAST                'future'
              216  BINARY_SUBSCR    
              218  CALL_FUNCTION_1       1  ''
              220  STORE_FAST               'page'

 L.  43       222  LOAD_FAST                'future'
              224  LOAD_METHOD              result
              226  CALL_METHOD_0         0  ''
              228  LOAD_FAST                'temp_chapters'
              230  LOAD_FAST                'page'
              232  STORE_SUBSCR     
              234  JUMP_BACK           206  'to 206'

 L.  46       236  LOAD_GLOBAL              logger
              238  LOAD_METHOD              info
              240  LOAD_STR                 'Building sorted chapter list...'
              242  CALL_METHOD_1         1  ''
              244  POP_TOP          

 L.  47       246  LOAD_GLOBAL              set
              248  CALL_FUNCTION_0       0  ''
              250  STORE_FAST               'volumes'

 L.  48       252  LOAD_GLOBAL              sorted
              254  LOAD_FAST                'temp_chapters'
              256  LOAD_METHOD              keys
              258  CALL_METHOD_0         0  ''
              260  CALL_FUNCTION_1       1  ''
              262  GET_ITER         
              264  FOR_ITER            354  'to 354'
              266  STORE_FAST               'page'

 L.  49       268  LOAD_FAST                'temp_chapters'
              270  LOAD_FAST                'page'
              272  BINARY_SUBSCR    
              274  GET_ITER         
              276  FOR_ITER            350  'to 350'
              278  STORE_FAST               'chap'

 L.  50       280  LOAD_CONST               1
              282  LOAD_GLOBAL              len
              284  LOAD_DEREF               'self'
              286  LOAD_ATTR                chapters
              288  CALL_FUNCTION_1       1  ''
              290  BINARY_ADD       
              292  LOAD_FAST                'chap'
              294  LOAD_STR                 'id'
              296  STORE_SUBSCR     

 L.  51       298  LOAD_CONST               1
              300  LOAD_GLOBAL              len
              302  LOAD_DEREF               'self'
              304  LOAD_ATTR                chapters
              306  CALL_FUNCTION_1       1  ''
              308  LOAD_CONST               100
              310  BINARY_FLOOR_DIVIDE
              312  BINARY_ADD       
              314  LOAD_FAST                'chap'
              316  LOAD_STR                 'volume'
              318  STORE_SUBSCR     

 L.  52       320  LOAD_FAST                'volumes'
              322  LOAD_METHOD              add
              324  LOAD_FAST                'chap'
              326  LOAD_STR                 'volume'
              328  BINARY_SUBSCR    
              330  CALL_METHOD_1         1  ''
              332  POP_TOP          

 L.  53       334  LOAD_DEREF               'self'
              336  LOAD_ATTR                chapters
              338  LOAD_METHOD              append
              340  LOAD_FAST                'chap'
              342  CALL_METHOD_1         1  ''
              344  POP_TOP          
          346_348  JUMP_BACK           276  'to 276'
          350_352  JUMP_BACK           264  'to 264'

 L.  57       354  LOAD_LISTCOMP            '<code_object <listcomp>>'
              356  LOAD_STR                 'RewayatClubCrawler.read_novel_info.<locals>.<listcomp>'
              358  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              360  LOAD_FAST                'volumes'
              362  GET_ITER         
              364  CALL_FUNCTION_1       1  ''
              366  LOAD_DEREF               'self'
              368  STORE_ATTR               volumes

Parse error at or near `LOAD_DICTCOMP' instruction at offset 172

    def download_chapter_list(self, page_no):
        chapter_url = self.novel_url + '?page=%d' % page_no
        logger.info'Visiting %s'chapter_url
        soup = self.get_soup(chapter_url)
        chapters = []
        for a in soup.select('.card a[href*="/novel/"]'):
            chapters.append({'url':self.absolute_url(a['href']), 
             'title':a.select_one('div p').text.strip})
        else:
            return chapters

    def download_chapter_body(self, chapter):
        """Download body of a single chapter and return as clean html format."""
        logger.info'Downloading %s'chapter['url']
        soup = self.get_soup(chapter['url'])
        paras = soup.select('.card .card-body p')
        paras = [str(p) for p in paras if p.text.strip]
        return ''.join(paras)