# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: .\src\sources\novelfull.py
# Compiled at: 2020-05-04 18:02:29
# Size of source mod 2**32: 4517 bytes
import re, logging
from concurrent import futures
from utils.crawler import Crawler
logger = logging.getLogger('NOVEL_FULL')
search_url = 'https://novelfull.com/search?keyword=%s'

class NovelFullCrawler(Crawler):
    base_url = [
     'http://novelfull.com/',
     'https://novelfull.com/']

    def search_novel(self, query):
        """Gets a list of (title, url) matching the given query"""
        query = query.strip().lower().replace(' ', '+')
        soup = self.get_soup(search_url % query)
        results = []
        for div in soup.select('#list-page .archive .list-truyen > .row'):
            a = div.select_one('.truyen-title a')
            info = div.select_one('.text-info a .chapter-text')
            results.append({'title':a.text.strip(), 
             'url':self.absolute_url(a['href']), 
             'info':info.text.strip() if info else ''})
        else:
            return results

    def read_novel_info--- This code section failed: ---

 L.  38         0  LOAD_GLOBAL              logger
                2  LOAD_METHOD              debug
                4  LOAD_STR                 'Visiting %s'
                6  LOAD_DEREF               'self'
                8  LOAD_ATTR                novel_url
               10  CALL_METHOD_2         2  ''
               12  POP_TOP          

 L.  39        14  LOAD_DEREF               'self'
               16  LOAD_METHOD              get_soup
               18  LOAD_DEREF               'self'
               20  LOAD_ATTR                novel_url
               22  CALL_METHOD_1         1  ''
               24  STORE_FAST               'soup'

 L.  41        26  LOAD_FAST                'soup'
               28  LOAD_METHOD              select_one
               30  LOAD_STR                 '.info-holder .book img'
               32  CALL_METHOD_1         1  ''
               34  STORE_FAST               'image'

 L.  42        36  LOAD_FAST                'image'
               38  LOAD_STR                 'alt'
               40  BINARY_SUBSCR    
               42  LOAD_DEREF               'self'
               44  STORE_ATTR               novel_title

 L.  43        46  LOAD_GLOBAL              logger
               48  LOAD_METHOD              info
               50  LOAD_STR                 'Novel title: %s'
               52  LOAD_DEREF               'self'
               54  LOAD_ATTR                novel_title
               56  CALL_METHOD_2         2  ''
               58  POP_TOP          

 L.  45        60  LOAD_DEREF               'self'
               62  LOAD_METHOD              absolute_url
               64  LOAD_FAST                'image'
               66  LOAD_STR                 'src'
               68  BINARY_SUBSCR    
               70  CALL_METHOD_1         1  ''
               72  LOAD_DEREF               'self'
               74  STORE_ATTR               novel_cover

 L.  46        76  LOAD_GLOBAL              logger
               78  LOAD_METHOD              info
               80  LOAD_STR                 'Novel cover: %s'
               82  LOAD_DEREF               'self'
               84  LOAD_ATTR                novel_cover
               86  CALL_METHOD_2         2  ''
               88  POP_TOP          

 L.  48        90  BUILD_LIST_0          0 
               92  STORE_FAST               'authors'

 L.  49        94  LOAD_FAST                'soup'
               96  LOAD_METHOD              select
               98  LOAD_STR                 '.info-holder .info a'
              100  CALL_METHOD_1         1  ''
              102  GET_ITER         
            104_0  COME_FROM           120  '120'
              104  FOR_ITER            140  'to 140'
              106  STORE_FAST               'a'

 L.  50       108  LOAD_FAST                'a'
              110  LOAD_STR                 'href'
              112  BINARY_SUBSCR    
              114  LOAD_METHOD              startswith
              116  LOAD_STR                 '/author/'
              118  CALL_METHOD_1         1  ''
              120  POP_JUMP_IF_FALSE   104  'to 104'

 L.  51       122  LOAD_FAST                'authors'
              124  LOAD_METHOD              append
              126  LOAD_FAST                'a'
              128  LOAD_ATTR                text
              130  LOAD_METHOD              strip
              132  CALL_METHOD_0         0  ''
              134  CALL_METHOD_1         1  ''
              136  POP_TOP          
              138  JUMP_BACK           104  'to 104'

 L.  54       140  LOAD_STR                 ', '
              142  LOAD_METHOD              join
              144  LOAD_FAST                'authors'
              146  CALL_METHOD_1         1  ''
              148  LOAD_DEREF               'self'
              150  STORE_ATTR               novel_author

 L.  55       152  LOAD_GLOBAL              logger
              154  LOAD_METHOD              info
              156  LOAD_STR                 'Novel author: %s'
              158  LOAD_DEREF               'self'
              160  LOAD_ATTR                novel_author
              162  CALL_METHOD_2         2  ''
              164  POP_TOP          

 L.  57       166  LOAD_FAST                'soup'
              168  LOAD_METHOD              select_one
              170  LOAD_STR                 '#list-chapter .pagination .last a'
              172  CALL_METHOD_1         1  ''
              174  STORE_FAST               'pagination_link'

 L.  58       176  LOAD_FAST                'pagination_link'
              178  POP_JUMP_IF_FALSE   192  'to 192'
              180  LOAD_GLOBAL              int
              182  LOAD_FAST                'pagination_link'
              184  LOAD_STR                 'data-page'
              186  BINARY_SUBSCR    
              188  CALL_FUNCTION_1       1  ''
              190  JUMP_FORWARD        194  'to 194'
            192_0  COME_FROM           178  '178'
              192  LOAD_CONST               0
            194_0  COME_FROM           190  '190'
              194  STORE_FAST               'page_count'

 L.  59       196  LOAD_GLOBAL              logger
              198  LOAD_METHOD              info
              200  LOAD_STR                 'Chapter list pages: %d'
              202  LOAD_FAST                'page_count'
              204  BINARY_MODULO    
              206  CALL_METHOD_1         1  ''
              208  POP_TOP          

 L.  61       210  LOAD_GLOBAL              logger
              212  LOAD_METHOD              info
              214  LOAD_STR                 'Getting chapters...'
              216  CALL_METHOD_1         1  ''
              218  POP_TOP          

 L.  62       220  LOAD_CLOSURE             'self'
              222  BUILD_TUPLE_1         1 
              224  LOAD_DICTCOMP            '<code_object <dictcomp>>'
              226  LOAD_STR                 'NovelFullCrawler.read_novel_info.<locals>.<dictcomp>'
              228  MAKE_FUNCTION_8          'closure'

 L.  67       230  LOAD_GLOBAL              range
              232  LOAD_FAST                'page_count'
              234  LOAD_CONST               1
              236  BINARY_ADD       
              238  CALL_FUNCTION_1       1  ''

 L.  62       240  GET_ITER         
              242  CALL_FUNCTION_1       1  ''
              244  STORE_FAST               'futures_to_check'

 L.  69       246  LOAD_LISTCOMP            '<code_object <listcomp>>'
              248  LOAD_STR                 'NovelFullCrawler.read_novel_info.<locals>.<listcomp>'
              250  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              252  LOAD_GLOBAL              futures
              254  LOAD_METHOD              as_completed
              256  LOAD_FAST                'futures_to_check'
              258  CALL_METHOD_1         1  ''
              260  GET_ITER         
              262  CALL_FUNCTION_1       1  ''
              264  POP_TOP          

 L.  71       266  LOAD_GLOBAL              logger
              268  LOAD_METHOD              info
              270  LOAD_STR                 'Sorting chapters...'
              272  CALL_METHOD_1         1  ''
              274  POP_TOP          

 L.  72       276  LOAD_DEREF               'self'
              278  LOAD_ATTR                chapters
              280  LOAD_ATTR                sort
              282  LOAD_LAMBDA              '<code_object <lambda>>'
              284  LOAD_STR                 'NovelFullCrawler.read_novel_info.<locals>.<lambda>'
              286  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              288  LOAD_CONST               ('key',)
              290  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              292  POP_TOP          

 L.  74       294  LOAD_GLOBAL              logger
              296  LOAD_METHOD              info
              298  LOAD_STR                 'Adding volumes...'
              300  CALL_METHOD_1         1  ''
              302  POP_TOP          

 L.  75       304  LOAD_DEREF               'self'
              306  LOAD_ATTR                chapters
              308  LOAD_CONST               0
              310  BINARY_SUBSCR    
              312  LOAD_STR                 'volume'
              314  BINARY_SUBSCR    
              316  STORE_FAST               'mini'

 L.  76       318  LOAD_DEREF               'self'
              320  LOAD_ATTR                chapters
              322  LOAD_CONST               -1
              324  BINARY_SUBSCR    
              326  LOAD_STR                 'volume'
              328  BINARY_SUBSCR    
              330  STORE_FAST               'maxi'

 L.  77       332  LOAD_GLOBAL              range
              334  LOAD_FAST                'mini'
              336  LOAD_FAST                'maxi'
              338  LOAD_CONST               1
              340  BINARY_ADD       
              342  CALL_FUNCTION_2       2  ''
              344  GET_ITER         
              346  FOR_ITER            382  'to 382'
              348  STORE_FAST               'i'

 L.  78       350  LOAD_DEREF               'self'
              352  LOAD_ATTR                volumes
              354  LOAD_METHOD              append

 L.  79       356  LOAD_FAST                'i'

 L.  80       358  LOAD_STR                 'Volume %d'
              360  LOAD_FAST                'i'
              362  BINARY_MODULO    

 L.  81       364  LOAD_GLOBAL              str
              366  LOAD_FAST                'i'
              368  CALL_FUNCTION_1       1  ''

 L.  78       370  LOAD_CONST               ('id', 'title', 'volume')
              372  BUILD_CONST_KEY_MAP_3     3 
              374  CALL_METHOD_1         1  ''
              376  POP_TOP          
          378_380  JUMP_BACK           346  'to 346'

Parse error at or near `LOAD_DICTCOMP' instruction at offset 224

    def download_chapter_list(self, page):
        """Download list of chapters and volumes."""
        url = self.novel_url.split('?')[0].strip('/')
        url += '?page=%d&per-page=50' % page
        soup = self.get_soup(url)
        for a in soup.select('ul.list-chapter li a'):
            title = a['title'].strip()
            chapter_id = len(self.chapters) + 1
            match = re.findall('ch(apter)? (\\d+)', title, re.IGNORECASE)
            if len(match) == 1:
                chapter_id = int(match[0][1])
            volume_id = 1 + (chapter_id - 1) // 100
            match = re.findall('(book|vol|volume) (\\d+)', title, re.IGNORECASE)
            if len(match) == 1:
                volume_id = int(match[0][1])
            data = {'title':title, 
             'id':chapter_id, 
             'volume':volume_id, 
             'url':self.absolute_url(a['href'])}
            self.chapters.append(data)

    def download_chapter_body(self, chapter):
        """Download body of a single chapter and return as clean html format."""
        logger.info('Downloading %s', chapter['url'])
        soup = self.get_soup(chapter['url'])
        content = soup.select_one('div#chapter-content')
        for ads in content.findAll('div', {'align': 'left'}):
            ads.decompose()
        else:
            for ads in content.findAll('div', {'align': 'center'}):
                ads.decompose()
            else:
                self.clean_contents(content)
                return str(content)