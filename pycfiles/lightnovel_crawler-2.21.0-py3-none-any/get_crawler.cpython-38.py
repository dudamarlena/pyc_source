# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: .\src\bots\console\get_crawler.py
# Compiled at: 2020-03-25 09:13:24
# Size of source mod 2**32: 3119 bytes
import re
from PyInquirer import prompt
from ...core import display
from core.arguments import get_args
from ...sources import rejected_sources

def get_novel_url--- This code section failed: ---

 L.  13         0  LOAD_GLOBAL              get_args
                2  CALL_FUNCTION_0       0  ''
                4  STORE_FAST               'args'

 L.  14         6  LOAD_FAST                'args'
                8  LOAD_ATTR                query
               10  POP_JUMP_IF_FALSE    32  'to 32'
               12  LOAD_GLOBAL              len
               14  LOAD_FAST                'args'
               16  LOAD_ATTR                query
               18  CALL_FUNCTION_1       1  ''
               20  LOAD_CONST               1
               22  COMPARE_OP               >
               24  POP_JUMP_IF_FALSE    32  'to 32'

 L.  15        26  LOAD_FAST                'args'
               28  LOAD_ATTR                query
               30  RETURN_VALUE     
             32_0  COME_FROM            24  '24'
             32_1  COME_FROM            10  '10'

 L.  18        32  LOAD_FAST                'args'
               34  LOAD_ATTR                novel_page
               36  STORE_FAST               'url'

 L.  19        38  LOAD_FAST                'url'
               40  POP_JUMP_IF_FALSE    66  'to 66'

 L.  20        42  LOAD_GLOBAL              re
               44  LOAD_METHOD              match
               46  LOAD_STR                 '^https?://.+\\..+$'
               48  LOAD_FAST                'url'
               50  CALL_METHOD_2         2  ''
               52  POP_JUMP_IF_FALSE    58  'to 58'

 L.  21        54  LOAD_FAST                'url'
               56  RETURN_VALUE     
             58_0  COME_FROM            52  '52'

 L.  23        58  LOAD_GLOBAL              Exception
               60  LOAD_STR                 'Invalid URL of novel page'
               62  CALL_FUNCTION_1       1  ''
               64  RAISE_VARARGS_1       1  'exception instance'
             66_0  COME_FROM            40  '40'

 L.  27        66  SETUP_FINALLY       118  'to 118'

 L.  28        68  LOAD_FAST                'args'
               70  LOAD_ATTR                suppress
               72  POP_JUMP_IF_FALSE    80  'to 80'

 L.  29        74  LOAD_GLOBAL              Exception
               76  CALL_FUNCTION_0       0  ''
               78  RAISE_VARARGS_1       1  'exception instance'
             80_0  COME_FROM            72  '72'

 L.  32        80  LOAD_GLOBAL              prompt

 L.  34        82  LOAD_STR                 'input'

 L.  35        84  LOAD_STR                 'novel'

 L.  36        86  LOAD_STR                 'Enter novel page url or query novel:'

 L.  37        88  LOAD_LAMBDA              '<code_object <lambda>>'
               90  LOAD_STR                 'get_novel_url.<locals>.<lambda>'
               92  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L.  33        94  LOAD_CONST               ('type', 'name', 'message', 'validate')
               96  BUILD_CONST_KEY_MAP_4     4 

 L.  32        98  BUILD_LIST_1          1 
              100  CALL_FUNCTION_1       1  ''
              102  STORE_FAST               'answer'

 L.  41       104  LOAD_FAST                'answer'
              106  LOAD_STR                 'novel'
              108  BINARY_SUBSCR    
              110  LOAD_METHOD              strip
              112  CALL_METHOD_0         0  ''
              114  POP_BLOCK        
              116  RETURN_VALUE     
            118_0  COME_FROM_FINALLY    66  '66'

 L.  42       118  DUP_TOP          
              120  LOAD_GLOBAL              Exception
              122  COMPARE_OP               exception-match
              124  POP_JUMP_IF_FALSE   144  'to 144'
              126  POP_TOP          
              128  POP_TOP          
              130  POP_TOP          

 L.  43       132  LOAD_GLOBAL              Exception
              134  LOAD_STR                 'Novel page url or query was not given'
              136  CALL_FUNCTION_1       1  ''
              138  RAISE_VARARGS_1       1  'exception instance'
              140  POP_EXCEPT       
              142  JUMP_FORWARD        146  'to 146'
            144_0  COME_FROM           124  '124'
              144  END_FINALLY      
            146_0  COME_FROM           142  '142'

Parse error at or near `POP_TOP' instruction at offset 128


def get_crawlers_to_search(self):
    """Returns user choice to search the choosen sites for a novel"""
    links = self.app.crawler_links
    if not links:
        return
    else:
        args = get_args
        return args.suppress or args.sources or links
    answer = prompt([
     {'type':'checkbox', 
      'name':'sites', 
      'message':'Where to search?', 
      'choices':[{'name': x} for x in sorted(links)]}])
    selected = answer['sites']
    if len(selected) > 0:
        return selected
    return links


def choose_a_novel(self):
    """Choose a single novel url from the search result"""
    args = get_args
    choices = self.app.search_results
    selected_choice = self.app.search_results[0]
    if len(choices) > 1:
        if not args.suppress:
            answer = prompt([
             {'type':'list', 
              'name':'novel', 
              'message':'Which one is your novel?', 
              'choices':display.format_novel_choices(choices)}])
            index = int(answer['novel'].split('.')[0])
            selected_choice = self.app.search_results[(index - 1)]
    else:
        novels = selected_choice['novels']
        selected_novel = novels[0]
        if len(novels) > 1:
            answer = args.suppress or prompt([
             {'type':'list', 
              'name':'novel', 
              'message':'Choose a source to download?', 
              'choices':[
               '0. Back'] + display.format_source_choices(novels)}])
            index = int(answer['novel'].split('.')[0])
            if index == 0:
                return self.choose_a_novel
            selected_novel = novels[(index - 1)]
    return selected_novel['url']