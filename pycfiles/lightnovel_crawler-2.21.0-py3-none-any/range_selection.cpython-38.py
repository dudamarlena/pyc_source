# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: .\src\bots\console\range_selection.py
# Compiled at: 2020-03-25 09:13:24
# Size of source mod 2**32: 6918 bytes
from PyInquirer import prompt
from core.arguments import get_args

def get_range_selection(self):
    """
    Returns a choice of how to select the range of chapters to downloads
    """
    volume_count = len(self.app.crawler.volumes)
    chapter_count = len(self.app.crawler.chapters)
    selections = ['all', 'last', 'first',
     'page', 'range', 'volumes', 'chapters']
    args = get_args()
    for key in selections:
        if args.__getattribute__(key):
            return key
        if args.suppress:
            return selections[0]
        big_list_warn = '(warn: very big list)' if chapter_count > 50 else ''
        choices = [
         'Everything! (%d chapters)' % chapter_count,
         'Last 10 chapters',
         'First 10 chapters',
         'Custom range using URL',
         'Custom range using index',
         'Select specific volumes (%d volumes)' % volume_count,
         'Select specific chapters ' + big_list_warn]
        if chapter_count <= 20:
            choices.pop(1)
            choices.pop(1)
        answer = prompt([
         {'type':'list', 
          'name':'choice', 
          'message':'Which chapters to download?', 
          'choices':choices}])
        return selections[choices.index(answer['choice'])]


def get_range_using_urls(self):
    """Returns a range of chapters using start and end urls as input"""
    args = get_args()
    start_url, stop_url = args.page or (None, None)
    if args.suppress:
        return start_url and stop_url or (
         0, len(self.app.crawler.chapters) - 1)
    if not (start_url and stop_url):

        def validator--- This code section failed: ---

 L.  67         0  SETUP_FINALLY        30  'to 30'

 L.  68         2  LOAD_DEREF               'self'
                4  LOAD_ATTR                app
                6  LOAD_ATTR                crawler
                8  LOAD_METHOD              get_chapter_index_of
               10  LOAD_FAST                'val'
               12  CALL_METHOD_1         1  ''
               14  LOAD_CONST               0
               16  COMPARE_OP               >
               18  POP_JUMP_IF_FALSE    26  'to 26'

 L.  69        20  POP_BLOCK        
               22  LOAD_CONST               True
               24  RETURN_VALUE     
             26_0  COME_FROM            18  '18'
               26  POP_BLOCK        
               28  JUMP_FORWARD         50  'to 50'
             30_0  COME_FROM_FINALLY     0  '0'

 L.  70        30  DUP_TOP          
               32  LOAD_GLOBAL              Exception
               34  COMPARE_OP               exception-match
               36  POP_JUMP_IF_FALSE    48  'to 48'
               38  POP_TOP          
               40  POP_TOP          
               42  POP_TOP          

 L.  71        44  POP_EXCEPT       
               46  JUMP_FORWARD         50  'to 50'
             48_0  COME_FROM            36  '36'
               48  END_FINALLY      
             50_0  COME_FROM            46  '46'
             50_1  COME_FROM            28  '28'

 L.  72        50  LOAD_STR                 'No such chapter found given the url'
               52  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_CONST' instruction at offset 22

        answer = prompt([
         {'type':'input', 
          'name':'start_url', 
          'message':'Enter start url:', 
          'validate':validator},
         {'type':'input', 
          'name':'stop_url', 
          'message':'Enter final url:', 
          'validate':validator}])
        start_url = answer['start_url']
        stop_url = answer['stop_url']
    start = self.app.crawler.get_chapter_index_of(start_url) - 1
    stop = self.app.crawler.get_chapter_index_of(stop_url) - 1
    if start < stop:
        return (start, stop)
    return (stop, start)


def get_range_using_index(self):
    """Returns a range selected using chapter indices"""
    chapter_count = len(self.app.crawler.chapters)
    args = get_args()
    start, stop = args.range or (None, None)
    if args.suppress:
        return start and stop or (
         0, chapter_count - 1)
    elif not (start and stop):

        def validator--- This code section failed: ---

 L. 112         0  SETUP_FINALLY        40  'to 40'

 L. 113         2  LOAD_CONST               1
                4  LOAD_GLOBAL              int
                6  LOAD_FAST                'val'
                8  CALL_FUNCTION_1       1  ''
               10  DUP_TOP          
               12  ROT_THREE        
               14  COMPARE_OP               <=
               16  POP_JUMP_IF_FALSE    26  'to 26'
               18  LOAD_DEREF               'chapter_count'
               20  COMPARE_OP               <=
               22  POP_JUMP_IF_FALSE    36  'to 36'
               24  JUMP_FORWARD         30  'to 30'
             26_0  COME_FROM            16  '16'
               26  POP_TOP          
               28  JUMP_FORWARD         36  'to 36'
             30_0  COME_FROM            24  '24'

 L. 114        30  POP_BLOCK        
               32  LOAD_CONST               True
               34  RETURN_VALUE     
             36_0  COME_FROM            28  '28'
             36_1  COME_FROM            22  '22'
               36  POP_BLOCK        
               38  JUMP_FORWARD         60  'to 60'
             40_0  COME_FROM_FINALLY     0  '0'

 L. 115        40  DUP_TOP          
               42  LOAD_GLOBAL              Exception
               44  COMPARE_OP               exception-match
               46  POP_JUMP_IF_FALSE    58  'to 58'
               48  POP_TOP          
               50  POP_TOP          
               52  POP_TOP          

 L. 116        54  POP_EXCEPT       
               56  JUMP_FORWARD         60  'to 60'
             58_0  COME_FROM            46  '46'
               58  END_FINALLY      
             60_0  COME_FROM            56  '56'
             60_1  COME_FROM            38  '38'

 L. 117        60  LOAD_STR                 'Enter an integer between 1 and %d'
               62  LOAD_DEREF               'chapter_count'
               64  BINARY_MODULO    
               66  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_CONST' instruction at offset 32

        answer = prompt([
         {'type':'input', 
          'name':'start', 
          'message':'Enter start index (1 to %d):' % chapter_count, 
          'validate':validator, 
          'filter':lambda val: int(val)},
         {'type':'input', 
          'name':'stop', 
          'message':'Enter final index (1 to %d):' % chapter_count, 
          'validate':validator, 
          'filter':lambda val: int(val)}])
        start = answer['start'] - 1
        stop = answer['stop'] - 1
    else:
        start = start - 1
        stop = stop - 1
    if start < stop:
        return (start, stop)
    return (stop, start)


def get_range_from_volumes(self, times=0):
    """Returns a range created using volume list"""
    selected = None
    args = get_args()
    if times == 0:
        if args.volumes:
            selected = [int(x) for x in args.volumes]
    if not selected:
        if args.suppress:
            selected = [x['id'] for x in self.app.crawler.volumes]
    if not selected:
        answer = prompt([
         {'type':'checkbox', 
          'name':'volumes', 
          'message':'Choose volumes to download:', 
          'choices':[{'name': '%d - %s (Chapter %d-%d) [%d chapters]' % (
                    vol['id'], vol['title'], vol['start_chapter'],
                    vol['final_chapter'], vol['chapter_count'])} for vol in self.app.crawler.volumes], 
          'validate':lambda ans:           if len(ans) > 0:
True # Avoid dead code: 'You must choose at least one volume.'}])
        selected = [int(val.split(' ')[0]) for val in answer['volumes']]
    if times < 3:
        if len(selected) == 0:
            return self.get_range_from_volumes(times + 1)
    return selected


def get_range_from_chapters(self, times=0):
    """Returns a range created using individual chapters"""
    selected = None
    args = get_args()
    if times == 0:
        if not selected:
            selected = get_args().chapters
    if not selected:
        if args.suppress:
            selected = self.app.crawler.chapters
    elif not selected:
        answer = prompt([
         {'type':'checkbox', 
          'name':'chapters', 
          'message':'Choose chapters to download:', 
          'choices':[{'name': '%d - %s' % (chap['id'], chap['title'])} for chap in self.app.crawler.chapters], 
          'validate':lambda ans:           if len(ans) > 0:
True # Avoid dead code: 'You must choose at least one chapter.'}])
        selected = [int(val.split(' ')[0]) for val in answer['chapters']]
    else:
        selected = [self.app.crawler.get_chapter_index_of(x) for x in selected if x]
    if times < 3:
        if len(selected) == 0:
            return self.get_range_from_chapters(times + 1)
    selected = [x for x in selected if 1 <= x <= len(self.app.crawler.chapters)]
    return selected