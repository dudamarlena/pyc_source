# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: .\src\core\novel_search.py
# Compiled at: 2020-03-25 09:13:24
# Size of source mod 2**32: 2746 bytes
"""
To search for novels in selected sources
"""
import os, logging
from concurrent import futures
from slugify import slugify
from progress.bar import IncrementalBar
from ..sources import crawler_list
logger = logging.getLogger('SEARCH_NOVEL')

def get_search_result--- This code section failed: ---

 L.  18         0  SETUP_FINALLY        72  'to 72'

 L.  19         2  LOAD_GLOBAL              crawler_list
                4  LOAD_FAST                'link'
                6  BINARY_SUBSCR    
                8  STORE_FAST               'crawler'

 L.  20        10  LOAD_FAST                'crawler'
               12  CALL_FUNCTION_0       0  ''
               14  STORE_FAST               'instance'

 L.  21        16  LOAD_FAST                'link'
               18  LOAD_METHOD              strip
               20  LOAD_STR                 '/'
               22  CALL_METHOD_1         1  ''
               24  LOAD_FAST                'instance'
               26  STORE_ATTR               home_url

 L.  22        28  LOAD_FAST                'instance'
               30  LOAD_METHOD              search_novel
               32  LOAD_FAST                'user_input'
               34  CALL_METHOD_1         1  ''
               36  STORE_FAST               'results'

 L.  23        38  LOAD_GLOBAL              logger
               40  LOAD_METHOD              debug
               42  LOAD_FAST                'results'
               44  CALL_METHOD_1         1  ''
               46  POP_TOP          

 L.  24        48  LOAD_GLOBAL              logger
               50  LOAD_METHOD              info
               52  LOAD_STR                 '%d results from %s'
               54  LOAD_GLOBAL              len
               56  LOAD_FAST                'results'
               58  CALL_FUNCTION_1       1  ''
               60  LOAD_FAST                'link'
               62  CALL_METHOD_3         3  ''
               64  POP_TOP          

 L.  25        66  LOAD_FAST                'results'
               68  POP_BLOCK        
               70  RETURN_VALUE     
             72_0  COME_FROM_FINALLY     0  '0'

 L.  26        72  DUP_TOP          
               74  LOAD_GLOBAL              Exception
               76  COMPARE_OP               exception-match
               78  POP_JUMP_IF_FALSE   112  'to 112'
               80  POP_TOP          
               82  POP_TOP          
               84  POP_TOP          

 L.  27        86  LOAD_CONST               0
               88  LOAD_CONST               None
               90  IMPORT_NAME              traceback
               92  STORE_FAST               'traceback'

 L.  28        94  LOAD_GLOBAL              logger
               96  LOAD_METHOD              debug
               98  LOAD_FAST                'traceback'
              100  LOAD_METHOD              format_exc
              102  CALL_METHOD_0         0  ''
              104  CALL_METHOD_1         1  ''
              106  POP_TOP          
              108  POP_EXCEPT       
              110  JUMP_FORWARD        114  'to 114'
            112_0  COME_FROM            78  '78'
              112  END_FINALLY      
            114_0  COME_FROM           110  '110'

 L.  30       114  BUILD_LIST_0          0 
              116  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_TOP' instruction at offset 82


def process_results--- This code section failed: ---

 L.  35         0  LOAD_GLOBAL              dict
                2  CALL_FUNCTION_0       0  ''
                4  STORE_FAST               'combined'

 L.  36         6  LOAD_FAST                'results'
                8  GET_ITER         
               10  FOR_ITER             74  'to 74'
               12  STORE_FAST               'result'

 L.  37        14  LOAD_GLOBAL              slugify
               16  LOAD_FAST                'result'
               18  LOAD_STR                 'title'
               20  BINARY_SUBSCR    
               22  CALL_FUNCTION_1       1  ''
               24  STORE_FAST               'key'

 L.  38        26  LOAD_GLOBAL              len
               28  LOAD_FAST                'key'
               30  CALL_FUNCTION_1       1  ''
               32  LOAD_CONST               1
               34  COMPARE_OP               <=
               36  POP_JUMP_IF_FALSE    42  'to 42'

 L.  39        38  JUMP_BACK            10  'to 10'
               40  JUMP_FORWARD         58  'to 58'
             42_0  COME_FROM            36  '36'

 L.  40        42  LOAD_FAST                'key'
               44  LOAD_FAST                'combined'
               46  COMPARE_OP               not-in
               48  POP_JUMP_IF_FALSE    58  'to 58'

 L.  41        50  BUILD_LIST_0          0 
               52  LOAD_FAST                'combined'
               54  LOAD_FAST                'key'
               56  STORE_SUBSCR     
             58_0  COME_FROM            48  '48'
             58_1  COME_FROM            40  '40'

 L.  43        58  LOAD_FAST                'combined'
               60  LOAD_FAST                'key'
               62  BINARY_SUBSCR    
               64  LOAD_METHOD              append
               66  LOAD_FAST                'result'
               68  CALL_METHOD_1         1  ''
               70  POP_TOP          
               72  JUMP_BACK            10  'to 10'

 L.  46        74  BUILD_LIST_0          0 
               76  STORE_FAST               'processed'

 L.  47        78  LOAD_FAST                'combined'
               80  LOAD_METHOD              items
               82  CALL_METHOD_0         0  ''
               84  GET_ITER         
               86  FOR_ITER            138  'to 138'
               88  UNPACK_SEQUENCE_2     2 
               90  STORE_FAST               'key'
               92  STORE_FAST               'value'

 L.  48        94  LOAD_FAST                'value'
               96  LOAD_ATTR                sort
               98  LOAD_LAMBDA              '<code_object <lambda>>'
              100  LOAD_STR                 'process_results.<locals>.<lambda>'
              102  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              104  LOAD_CONST               ('key',)
              106  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              108  POP_TOP          

 L.  49       110  LOAD_FAST                'processed'
              112  LOAD_METHOD              append

 L.  50       114  LOAD_FAST                'key'

 L.  51       116  LOAD_FAST                'value'
              118  LOAD_CONST               0
              120  BINARY_SUBSCR    
              122  LOAD_STR                 'title'
              124  BINARY_SUBSCR    

 L.  52       126  LOAD_FAST                'value'

 L.  49       128  LOAD_CONST               ('id', 'title', 'novels')
              130  BUILD_CONST_KEY_MAP_3     3 
              132  CALL_METHOD_1         1  ''
              134  POP_TOP          
              136  JUMP_BACK            86  'to 86'

 L.  56       138  LOAD_FAST                'processed'
              140  LOAD_ATTR                sort
              142  LOAD_LAMBDA              '<code_object <lambda>>'
              144  LOAD_STR                 'process_results.<locals>.<lambda>'
              146  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              148  LOAD_CONST               ('key',)
              150  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              152  POP_TOP          

 L.  58       154  LOAD_FAST                'processed'
              156  LOAD_CONST               None
              158  LOAD_CONST               15
              160  BUILD_SLICE_2         2 
              162  BINARY_SUBSCR    
              164  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_FORWARD' instruction at offset 40


def search_novels(app):
    executor = futures.ThreadPoolExecutor(10)
    checked = {}
    futures_to_check = {}
    for link in app.crawler_links:
        crawler = crawler_list[link]
        if crawler in checked:
            logger.info('A crawler for "%s" already exists', link)
        else:
            checked[crawler] = True
            futures_to_check[executor.submitget_search_resultapp.user_inputlink] = str(crawler)
    else:
        bar = IncrementalBar('Searching', max=(len(futures_to_check.keys)))
        bar.start
        if os.getenv('debug_mode') == 'yes':
            bar.next = lambda : None
        app.progress = 0
        combined_results = []
        for future in futures.as_completed(futures_to_check):
            combined_results += future.result
            app.progress += 1
            bar.next
        else:
            app.search_results = process_results(combined_results)
            bar.clearln
            bar.finish
            print('Found %d results' % len(app.search_results))
            executor.shutdown