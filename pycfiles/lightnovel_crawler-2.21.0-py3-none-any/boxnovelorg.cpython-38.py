# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: .\src\sources\boxnovelorg.py
# Compiled at: 2020-03-25 09:13:24
# Size of source mod 2**32: 5088 bytes
import logging, re
from concurrent import futures
from utils.crawler import Crawler
logger = logging.getLogger('BOXNOVEL.ORG')
search_url = 'http://boxnovel.org/search?keyword=%s'

class BoxNovelOrgCrawler(Crawler):
    base_url = 'http://boxnovel.org/'

    def search_novel(self, query):
        query = query.lower().replace(' ', '+')
        soup = self.get_soup(search_url % query)
        results = []
        for tab in soup.select('.col-novel-main .list-novel .row'):
            search_title = tab.select_one('.novel-title a')
            latest = tab.select_one('.text-info a').text.strip()
            results.append({'title':search_title.text.strip(), 
             'url':self.absolute_url(tab.select_one('.novel-title a')['href']), 
             'info':'Latest chapter: %s' % latest})
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

 L.  39        26  LOAD_STR                 ' '
               28  LOAD_METHOD              join
               30  LOAD_LISTCOMP            '<code_object <listcomp>>'
               32  LOAD_STR                 'BoxNovelOrgCrawler.read_novel_info.<locals>.<listcomp>'
               34  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L.  41        36  LOAD_FAST                'soup'
               38  LOAD_METHOD              select_one
               40  LOAD_STR                 '.title'
               42  CALL_METHOD_1         1  ''
               44  LOAD_ATTR                contents

 L.  39        46  GET_ITER         
               48  CALL_FUNCTION_1       1  ''
               50  CALL_METHOD_1         1  ''
               52  LOAD_METHOD              strip
               54  CALL_METHOD_0         0  ''
               56  LOAD_DEREF               'self'
               58  STORE_ATTR               novel_title

 L.  44        60  LOAD_GLOBAL              logger
               62  LOAD_METHOD              info
               64  LOAD_STR                 'Novel title: %s'
               66  LOAD_DEREF               'self'
               68  LOAD_ATTR                novel_title
               70  CALL_METHOD_2         2  ''
               72  POP_TOP          

 L.  46        74  LOAD_DEREF               'self'
               76  LOAD_METHOD              absolute_url

 L.  47        78  LOAD_FAST                'soup'
               80  LOAD_METHOD              select_one
               82  LOAD_STR                 '.book img'
               84  CALL_METHOD_1         1  ''
               86  LOAD_STR                 'src'
               88  BINARY_SUBSCR    

 L.  46        90  CALL_METHOD_1         1  ''
               92  LOAD_DEREF               'self'
               94  STORE_ATTR               novel_cover

 L.  48        96  LOAD_GLOBAL              logger
               98  LOAD_METHOD              info
              100  LOAD_STR                 'Novel cover: %s'
              102  LOAD_DEREF               'self'
              104  LOAD_ATTR                novel_cover
              106  CALL_METHOD_2         2  ''
              108  POP_TOP          

 L.  50       110  LOAD_FAST                'soup'
              112  LOAD_ATTR                find_all
              114  LOAD_GLOBAL              re
              116  LOAD_METHOD              compile
              118  LOAD_STR                 'author'
              120  CALL_METHOD_1         1  ''
              122  LOAD_CONST               ('href',)
              124  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              126  STORE_FAST               'author'

 L.  51       128  LOAD_GLOBAL              len
              130  LOAD_FAST                'author'
              132  CALL_FUNCTION_1       1  ''
              134  LOAD_CONST               2
              136  COMPARE_OP               ==
              138  POP_JUMP_IF_FALSE   172  'to 172'

 L.  52       140  LOAD_FAST                'author'
              142  LOAD_CONST               0
              144  BINARY_SUBSCR    
              146  LOAD_ATTR                text
              148  LOAD_STR                 ' ('
              150  BINARY_ADD       
              152  LOAD_FAST                'author'
              154  LOAD_CONST               1
              156  BINARY_SUBSCR    
              158  LOAD_ATTR                text
              160  BINARY_ADD       
              162  LOAD_STR                 ')'
              164  BINARY_ADD       
              166  LOAD_DEREF               'self'
              168  STORE_ATTR               novel_author
              170  JUMP_FORWARD        184  'to 184'
            172_0  COME_FROM           138  '138'

 L.  54       172  LOAD_FAST                'author'
              174  LOAD_CONST               0
              176  BINARY_SUBSCR    
              178  LOAD_ATTR                text
              180  LOAD_DEREF               'self'
              182  STORE_ATTR               novel_author
            184_0  COME_FROM           170  '170'

 L.  55       184  LOAD_GLOBAL              logger
              186  LOAD_METHOD              info
              188  LOAD_STR                 'Novel author: %s'
              190  LOAD_DEREF               'self'
              192  LOAD_ATTR                novel_author
              194  CALL_METHOD_2         2  ''
              196  POP_TOP          

 L.  58       198  LOAD_FAST                'soup'
              200  LOAD_METHOD              select
              202  LOAD_STR                 '.pagination li a'
              204  CALL_METHOD_1         1  ''
              206  STORE_FAST               'pagination_links'

 L.  59       208  BUILD_LIST_0          0 
              210  STORE_FAST               'pagination_page_numbers'

 L.  60       212  LOAD_FAST                'pagination_links'
              214  GET_ITER         
            216_0  COME_FROM           228  '228'
              216  FOR_ITER            248  'to 248'
              218  STORE_FAST               'pagination_link'

 L.  62       220  LOAD_FAST                'pagination_link'
              222  LOAD_ATTR                text
              224  LOAD_METHOD              isdigit
              226  CALL_METHOD_0         0  ''
              228  POP_JUMP_IF_FALSE   216  'to 216'

 L.  63       230  LOAD_FAST                'pagination_page_numbers'
              232  LOAD_METHOD              append
              234  LOAD_GLOBAL              int
              236  LOAD_FAST                'pagination_link'
              238  LOAD_ATTR                text
              240  CALL_FUNCTION_1       1  ''
              242  CALL_METHOD_1         1  ''
              244  POP_TOP          
              246  JUMP_BACK           216  'to 216'

 L.  66       248  LOAD_FAST                'pagination_page_numbers'

 L.  65   250_252  POP_JUMP_IF_FALSE   262  'to 262'
              254  LOAD_GLOBAL              max

 L.  66       256  LOAD_FAST                'pagination_page_numbers'

 L.  65       258  CALL_FUNCTION_1       1  ''
              260  JUMP_FORWARD        264  'to 264'
            262_0  COME_FROM           250  '250'

 L.  66       262  LOAD_CONST               0
            264_0  COME_FROM           260  '260'

 L.  65       264  STORE_FAST               'page_count'

 L.  67       266  LOAD_GLOBAL              logger
              268  LOAD_METHOD              info
              270  LOAD_STR                 'Chapter list pages: %d'
              272  LOAD_FAST                'page_count'
              274  BINARY_MODULO    
              276  CALL_METHOD_1         1  ''
              278  POP_TOP          

 L.  69       280  LOAD_GLOBAL              logger
              282  LOAD_METHOD              info
              284  LOAD_STR                 'Getting chapters...'
              286  CALL_METHOD_1         1  ''
              288  POP_TOP          

 L.  70       290  LOAD_CLOSURE             'self'
              292  BUILD_TUPLE_1         1 
              294  LOAD_DICTCOMP            '<code_object <dictcomp>>'
              296  LOAD_STR                 'BoxNovelOrgCrawler.read_novel_info.<locals>.<dictcomp>'
              298  MAKE_FUNCTION_8          'closure'

 L.  75       300  LOAD_GLOBAL              range
              302  LOAD_FAST                'page_count'
              304  LOAD_CONST               1
              306  BINARY_ADD       
              308  CALL_FUNCTION_1       1  ''

 L.  70       310  GET_ITER         
              312  CALL_FUNCTION_1       1  ''
              314  STORE_FAST               'futures_to_check'

 L.  77       316  LOAD_LISTCOMP            '<code_object <listcomp>>'
              318  LOAD_STR                 'BoxNovelOrgCrawler.read_novel_info.<locals>.<listcomp>'
              320  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              322  LOAD_GLOBAL              futures
              324  LOAD_METHOD              as_completed
              326  LOAD_FAST                'futures_to_check'
              328  CALL_METHOD_1         1  ''
              330  GET_ITER         
              332  CALL_FUNCTION_1       1  ''
              334  POP_TOP          

 L.  80       336  LOAD_GLOBAL              logger
              338  LOAD_METHOD              info
              340  LOAD_STR                 'Sorting chapters...'
              342  CALL_METHOD_1         1  ''
              344  POP_TOP          

 L.  81       346  LOAD_DEREF               'self'
              348  LOAD_ATTR                chapters
              350  LOAD_ATTR                sort
              352  LOAD_LAMBDA              '<code_object <lambda>>'
              354  LOAD_STR                 'BoxNovelOrgCrawler.read_novel_info.<locals>.<lambda>'
              356  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              358  LOAD_CONST               ('key',)
              360  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              362  POP_TOP          

 L.  84       364  LOAD_GLOBAL              logger
              366  LOAD_METHOD              info
              368  LOAD_STR                 'Adding volumes...'
              370  CALL_METHOD_1         1  ''
              372  POP_TOP          

 L.  85       374  LOAD_DEREF               'self'
              376  LOAD_ATTR                chapters
              378  LOAD_CONST               0
              380  BINARY_SUBSCR    
              382  LOAD_STR                 'volume'
              384  BINARY_SUBSCR    
              386  STORE_FAST               'mini'

 L.  86       388  LOAD_DEREF               'self'
              390  LOAD_ATTR                chapters
              392  LOAD_CONST               -1
              394  BINARY_SUBSCR    
              396  LOAD_STR                 'volume'
              398  BINARY_SUBSCR    
              400  STORE_FAST               'maxi'

 L.  87       402  LOAD_GLOBAL              range
              404  LOAD_FAST                'mini'
              406  LOAD_FAST                'maxi'
              408  LOAD_CONST               1
              410  BINARY_ADD       
              412  CALL_FUNCTION_2       2  ''
              414  GET_ITER         
              416  FOR_ITER            452  'to 452'
              418  STORE_FAST               'i'

 L.  88       420  LOAD_DEREF               'self'
              422  LOAD_ATTR                volumes
              424  LOAD_METHOD              append

 L.  89       426  LOAD_FAST                'i'

 L.  90       428  LOAD_STR                 'Volume %d'
              430  LOAD_FAST                'i'
              432  BINARY_MODULO    

 L.  91       434  LOAD_GLOBAL              str
              436  LOAD_FAST                'i'
              438  CALL_FUNCTION_1       1  ''

 L.  88       440  LOAD_CONST               ('id', 'title', 'volume')
              442  BUILD_CONST_KEY_MAP_3     3 
              444  CALL_METHOD_1         1  ''
              446  POP_TOP          
          448_450  JUMP_BACK           416  'to 416'

Parse error at or near `LOAD_DICTCOMP' instruction at offset 294

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
        contents = soup.select_one('div.chr-c')
        return str(contents)