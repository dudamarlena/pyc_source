# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: .\src\sources\noveluniverse.py
# Compiled at: 2020-03-25 09:13:24
# Size of source mod 2**32: 3709 bytes
import re, logging
from concurrent import futures
from utils.crawler import Crawler
logger = logging.getLogger('NOVEL_UNIVERSE')
novel_info_url = 'https://www.noveluniverse.com/index/novel/info/id/%s.html'
chapter_page_url = '%s?id=%s&page_c=%d'

class NovelUniverseCrawler(Crawler):
    base_url = 'https://www.noveluniverse.com/'

    def read_novel_info--- This code section failed: ---

 L.  17         0  LOAD_DEREF               'self'
                2  LOAD_ATTR                novel_url
                4  LOAD_METHOD              split
                6  LOAD_STR                 '/'
                8  CALL_METHOD_1         1  ''
               10  LOAD_CONST               -1
               12  BINARY_SUBSCR    
               14  LOAD_METHOD              split
               16  LOAD_STR                 '.'
               18  CALL_METHOD_1         1  ''
               20  LOAD_CONST               0
               22  BINARY_SUBSCR    
               24  LOAD_DEREF               'self'
               26  STORE_ATTR               novel_id

 L.  18        28  LOAD_GLOBAL              logger
               30  LOAD_METHOD              info
               32  LOAD_STR                 'Novel Id: %s'
               34  LOAD_DEREF               'self'
               36  LOAD_ATTR                novel_id
               38  CALL_METHOD_2         2  ''
               40  POP_TOP          

 L.  20        42  LOAD_GLOBAL              novel_info_url
               44  LOAD_DEREF               'self'
               46  LOAD_ATTR                novel_id
               48  BINARY_MODULO    
               50  LOAD_DEREF               'self'
               52  STORE_ATTR               novel_url

 L.  21        54  LOAD_GLOBAL              logger
               56  LOAD_METHOD              info
               58  LOAD_STR                 'Visiting %s'
               60  LOAD_DEREF               'self'
               62  LOAD_ATTR                novel_url
               64  CALL_METHOD_2         2  ''
               66  POP_TOP          

 L.  22        68  LOAD_DEREF               'self'
               70  LOAD_METHOD              get_soup
               72  LOAD_DEREF               'self'
               74  LOAD_ATTR                novel_url
               76  CALL_METHOD_1         1  ''
               78  STORE_FAST               'soup'

 L.  24        80  LOAD_FAST                'soup'
               82  LOAD_METHOD              select_one
               84  LOAD_STR                 '.book_info'
               86  CALL_METHOD_1         1  ''
               88  STORE_FAST               'book_info'

 L.  25        90  LOAD_FAST                'book_info'
               92  POP_JUMP_IF_TRUE    102  'to 102'

 L.  26        94  LOAD_GLOBAL              Exception
               96  LOAD_STR                 'Invalid content'
               98  CALL_FUNCTION_1       1  ''
              100  RAISE_VARARGS_1       1  'exception instance'
            102_0  COME_FROM            92  '92'

 L.  29       102  LOAD_FAST                'book_info'
              104  LOAD_METHOD              select_one
              106  LOAD_STR                 'h1.books_name'
              108  CALL_METHOD_1         1  ''
              110  LOAD_ATTR                text
              112  LOAD_METHOD              strip
              114  CALL_METHOD_0         0  ''
              116  LOAD_DEREF               'self'
              118  STORE_ATTR               novel_title

 L.  30       120  LOAD_GLOBAL              logger
              122  LOAD_METHOD              info
              124  LOAD_STR                 'Title: %s'
              126  LOAD_DEREF               'self'
              128  LOAD_ATTR                novel_title
              130  CALL_METHOD_2         2  ''
              132  POP_TOP          

 L.  32       134  BUILD_LIST_0          0 
              136  LOAD_DEREF               'self'
              138  STORE_ATTR               novel_author

 L.  33       140  LOAD_FAST                'book_info'
              142  LOAD_METHOD              select_one
              144  LOAD_STR                 '.info_more'
              146  CALL_METHOD_1         1  ''
              148  GET_ITER         
            150_0  COME_FROM           174  '174'
            150_1  COME_FROM           158  '158'
              150  FOR_ITER            194  'to 194'
              152  STORE_FAST               'tag'

 L.  34       154  LOAD_FAST                'tag'
              156  LOAD_ATTR                name
              158  POP_JUMP_IF_TRUE    150  'to 150'
              160  LOAD_GLOBAL              len
              162  LOAD_GLOBAL              str
              164  LOAD_FAST                'tag'
              166  CALL_FUNCTION_1       1  ''
              168  LOAD_METHOD              strip
              170  CALL_METHOD_0         0  ''
              172  CALL_FUNCTION_1       1  ''
              174  POP_JUMP_IF_FALSE   150  'to 150'

 L.  35       176  LOAD_DEREF               'self'
              178  LOAD_ATTR                novel_author
              180  LOAD_METHOD              append
              182  LOAD_GLOBAL              str
              184  LOAD_FAST                'tag'
              186  CALL_FUNCTION_1       1  ''
              188  CALL_METHOD_1         1  ''
              190  POP_TOP          
              192  JUMP_BACK           150  'to 150'

 L.  38       194  LOAD_STR                 ', '
              196  LOAD_METHOD              join
              198  LOAD_DEREF               'self'
              200  LOAD_ATTR                novel_author
              202  CALL_METHOD_1         1  ''
              204  LOAD_METHOD              strip
              206  CALL_METHOD_0         0  ''
              208  LOAD_DEREF               'self'
              210  STORE_ATTR               novel_author

 L.  39       212  LOAD_GLOBAL              logger
              214  LOAD_METHOD              info
              216  LOAD_DEREF               'self'
              218  LOAD_ATTR                novel_author
              220  CALL_METHOD_1         1  ''
              222  POP_TOP          

 L.  41       224  LOAD_DEREF               'self'
              226  LOAD_METHOD              absolute_url

 L.  42       228  LOAD_FAST                'book_info'
              230  LOAD_METHOD              select_one
              232  LOAD_STR                 '.img img'
              234  CALL_METHOD_1         1  ''
              236  LOAD_STR                 'src'
              238  BINARY_SUBSCR    

 L.  41       240  CALL_METHOD_1         1  ''
              242  LOAD_DEREF               'self'
              244  STORE_ATTR               novel_cover

 L.  43       246  LOAD_GLOBAL              logger
              248  LOAD_METHOD              info
              250  LOAD_STR                 'Cover: %s'
              252  LOAD_DEREF               'self'
              254  LOAD_ATTR                novel_cover
              256  CALL_METHOD_2         2  ''
              258  POP_TOP          

 L.  45       260  LOAD_FAST                'soup'
              262  LOAD_METHOD              select
              264  LOAD_STR                 '.allPagesStyle a'
              266  CALL_METHOD_1         1  ''
              268  STORE_FAST               'max_page'

 L.  46       270  LOAD_GLOBAL              len
              272  LOAD_FAST                'max_page'
              274  CALL_FUNCTION_1       1  ''
              276  LOAD_CONST               1
              278  COMPARE_OP               >
          280_282  POP_JUMP_IF_FALSE   300  'to 300'

 L.  47       284  LOAD_GLOBAL              int
              286  LOAD_FAST                'max_page'
              288  LOAD_CONST               -2
              290  BINARY_SUBSCR    
              292  LOAD_ATTR                text
              294  CALL_FUNCTION_1       1  ''
              296  STORE_FAST               'max_page'
              298  JUMP_FORWARD        304  'to 304'
            300_0  COME_FROM           280  '280'

 L.  49       300  LOAD_CONST               1
              302  STORE_FAST               'max_page'
            304_0  COME_FROM           298  '298'

 L.  51       304  LOAD_GLOBAL              logger
              306  LOAD_METHOD              info
              308  LOAD_STR                 'Pagination length: %d'
              310  LOAD_FAST                'max_page'
              312  CALL_METHOD_2         2  ''
              314  POP_TOP          

 L.  53       316  LOAD_CLOSURE             'self'
              318  BUILD_TUPLE_1         1 
              320  LOAD_DICTCOMP            '<code_object <dictcomp>>'
              322  LOAD_STR                 'NovelUniverseCrawler.read_novel_info.<locals>.<dictcomp>'
              324  MAKE_FUNCTION_8          'closure'

 L.  58       326  LOAD_GLOBAL              range
              328  LOAD_CONST               1
              330  LOAD_FAST                'max_page'
              332  LOAD_CONST               1
              334  BINARY_ADD       
              336  CALL_FUNCTION_2       2  ''

 L.  53       338  GET_ITER         
              340  CALL_FUNCTION_1       1  ''
              342  STORE_FAST               'tasks'

 L.  60       344  LOAD_LISTCOMP            '<code_object <listcomp>>'
              346  LOAD_STR                 'NovelUniverseCrawler.read_novel_info.<locals>.<listcomp>'
              348  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              350  LOAD_GLOBAL              futures
              352  LOAD_METHOD              as_completed
              354  LOAD_FAST                'tasks'
              356  CALL_METHOD_1         1  ''
              358  GET_ITER         
              360  CALL_FUNCTION_1       1  ''
              362  POP_TOP          

 L.  62       364  LOAD_DEREF               'self'
              366  LOAD_ATTR                chapters
              368  LOAD_ATTR                sort
              370  LOAD_LAMBDA              '<code_object <lambda>>'
              372  LOAD_STR                 'NovelUniverseCrawler.read_novel_info.<locals>.<lambda>'
              374  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              376  LOAD_CONST               ('key',)
              378  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              380  POP_TOP          

 L.  63       382  LOAD_LISTCOMP            '<code_object <listcomp>>'
              384  LOAD_STR                 'NovelUniverseCrawler.read_novel_info.<locals>.<listcomp>'
              386  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L.  65       388  LOAD_GLOBAL              set
              390  LOAD_DEREF               'self'
              392  LOAD_ATTR                volumes
              394  CALL_FUNCTION_1       1  ''

 L.  63       396  GET_ITER         
              398  CALL_FUNCTION_1       1  ''
              400  LOAD_DEREF               'self'
              402  STORE_ATTR               volumes

 L.  68       404  LOAD_GLOBAL              logger
              406  LOAD_METHOD              info
              408  LOAD_STR                 '%d chapters and %d volumes found'

 L.  69       410  LOAD_GLOBAL              len
              412  LOAD_DEREF               'self'
              414  LOAD_ATTR                chapters
              416  CALL_FUNCTION_1       1  ''

 L.  69       418  LOAD_GLOBAL              len
              420  LOAD_DEREF               'self'
              422  LOAD_ATTR                volumes
              424  CALL_FUNCTION_1       1  ''

 L.  68       426  CALL_METHOD_3         3  ''
              428  POP_TOP          

Parse error at or near `LOAD_DICTCOMP' instruction at offset 320

    def get_chapter_list(self, url):
        logger.info'Visiting %s'url
        soup = self.get_soup(url)
        for a in soup.select('ul#chapters li a'):
            chapter_id = a.select_one('span').text
            chapter_id = int([x for x in re.findall'\\d+'chapter_id][0])
            volume_id = 1 + (chapter_id - 1) // 100
            chapter_title = ' '.join([str(x).strip for x in a.contents if not x.name if str(x).strip]).strip
            chapter_title = 'Chapter %d: %s' % (chapter_id, chapter_title)
            self.volumes.append(volume_id)
            self.chapters.append({'id':chapter_id, 
             'url':self.absolute_url(a['href']), 
             'title':chapter_title, 
             'volume':volume_id})

    def download_chapter_body(self, chapter):
        logger.info'Visiting %s'chapter['url']
        soup = self.get_soup(chapter['url'])
        body = []
        for p in soup.select('div#content .overHide p.data-discuss'):
            para = ' '.join(self.extract_contents(p))
            if len(para):
                body.append(para)
            return '<p>%s</p>' % '</p><p>'.join(body)