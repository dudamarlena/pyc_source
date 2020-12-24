# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: .\src\bots\console\start.py
# Compiled at: 2020-03-25 09:13:24
# Size of source mod 2**32: 4396 bytes
from urllib.parse import urlparse
from PyInquirer import prompt
from ...core import display
from core.app import App
from core.arguments import get_args
from ...sources import rejected_sources

def start--- This code section failed: ---

 L.  13         0  LOAD_GLOBAL              get_args
                2  CALL_FUNCTION_0       0  ''
                4  STORE_FAST               'args'

 L.  14         6  LOAD_FAST                'args'
                8  LOAD_ATTR                list_sources
               10  POP_JUMP_IF_FALSE    24  'to 24'

 L.  15        12  LOAD_GLOBAL              display
               14  LOAD_METHOD              url_supported_list
               16  CALL_METHOD_0         0  ''
               18  POP_TOP          

 L.  16        20  LOAD_CONST               None
               22  RETURN_VALUE     
             24_0  COME_FROM            10  '10'

 L.  19        24  LOAD_GLOBAL              App
               26  CALL_FUNCTION_0       0  ''
               28  LOAD_FAST                'self'
               30  STORE_ATTR               app

 L.  20        32  LOAD_FAST                'self'
               34  LOAD_ATTR                app
               36  LOAD_METHOD              initialize
               38  CALL_METHOD_0         0  ''
               40  POP_TOP          

 L.  23        42  LOAD_FAST                'args'
               44  LOAD_ATTR                filename
               46  JUMP_IF_TRUE_OR_POP    50  'to 50'
               48  LOAD_STR                 ''
             50_0  COME_FROM            46  '46'
               50  LOAD_METHOD              strip
               52  CALL_METHOD_0         0  ''
               54  LOAD_FAST                'self'
               56  LOAD_ATTR                app
               58  STORE_ATTR               good_file_name

 L.  24        60  LOAD_FAST                'args'
               62  LOAD_ATTR                filename_only
               64  LOAD_FAST                'self'
               66  LOAD_ATTR                app
               68  STORE_ATTR               no_append_after_filename

 L.  27        70  LOAD_FAST                'self'
               72  LOAD_METHOD              get_novel_url
               74  CALL_METHOD_0         0  ''
               76  LOAD_FAST                'self'
               78  LOAD_ATTR                app
               80  STORE_ATTR               user_input

 L.  28        82  SETUP_FINALLY        98  'to 98'

 L.  29        84  LOAD_FAST                'self'
               86  LOAD_ATTR                app
               88  LOAD_METHOD              init_search
               90  CALL_METHOD_0         0  ''
               92  POP_TOP          
               94  POP_BLOCK        
               96  JUMP_FORWARD        198  'to 198'
             98_0  COME_FROM_FINALLY    82  '82'

 L.  30        98  DUP_TOP          
              100  LOAD_GLOBAL              Exception
              102  COMPARE_OP               exception-match
              104  POP_JUMP_IF_FALSE   196  'to 196'
              106  POP_TOP          
              108  POP_TOP          
              110  POP_TOP          

 L.  31       112  LOAD_FAST                'self'
              114  LOAD_ATTR                app
              116  LOAD_ATTR                user_input
              118  LOAD_METHOD              startswith
              120  LOAD_STR                 'http'
              122  CALL_METHOD_1         1  ''
              124  POP_JUMP_IF_FALSE   182  'to 182'

 L.  32       126  LOAD_GLOBAL              urlparse
              128  LOAD_FAST                'self'
              130  LOAD_ATTR                app
              132  LOAD_ATTR                user_input
              134  CALL_FUNCTION_1       1  ''
              136  STORE_FAST               'url'

 L.  33       138  LOAD_STR                 '%s://%s/'
              140  LOAD_FAST                'url'
              142  LOAD_ATTR                scheme
              144  LOAD_FAST                'url'
              146  LOAD_ATTR                hostname
              148  BUILD_TUPLE_2         2 
              150  BINARY_MODULO    
              152  STORE_FAST               'url'

 L.  34       154  LOAD_FAST                'url'
              156  LOAD_GLOBAL              rejected_sources
              158  COMPARE_OP               in
              160  POP_JUMP_IF_FALSE   182  'to 182'

 L.  35       162  LOAD_GLOBAL              display
              164  LOAD_METHOD              url_rejected
              166  LOAD_GLOBAL              rejected_sources
              168  LOAD_FAST                'url'
              170  BINARY_SUBSCR    
              172  CALL_METHOD_1         1  ''
              174  POP_TOP          

 L.  36       176  POP_EXCEPT       
              178  LOAD_CONST               None
              180  RETURN_VALUE     
            182_0  COME_FROM           160  '160'
            182_1  COME_FROM           124  '124'

 L.  39       182  LOAD_GLOBAL              display
              184  LOAD_METHOD              url_not_recognized
              186  CALL_METHOD_0         0  ''
              188  POP_TOP          

 L.  40       190  POP_EXCEPT       
              192  LOAD_CONST               None
              194  RETURN_VALUE     
            196_0  COME_FROM           104  '104'
              196  END_FINALLY      
            198_0  COME_FROM            96  '96'

 L.  44       198  LOAD_FAST                'self'
              200  LOAD_ATTR                app
              202  LOAD_ATTR                crawler
          204_206  POP_JUMP_IF_TRUE    266  'to 266'

 L.  45       208  LOAD_FAST                'self'
              210  LOAD_METHOD              get_crawlers_to_search
              212  CALL_METHOD_0         0  ''
              214  LOAD_FAST                'self'
              216  LOAD_ATTR                app
              218  STORE_ATTR               crawler_links

 L.  46       220  LOAD_FAST                'self'
              222  LOAD_ATTR                app
              224  LOAD_METHOD              search_novel
              226  CALL_METHOD_0         0  ''
              228  POP_TOP          

 L.  48       230  LOAD_FAST                'self'
              232  LOAD_METHOD              choose_a_novel
              234  CALL_METHOD_0         0  ''
              236  STORE_FAST               'novel_url'

 L.  49       238  LOAD_FAST                'self'
              240  LOAD_ATTR                log
              242  LOAD_METHOD              info
              244  LOAD_STR                 'Selected novel: %s'
              246  LOAD_FAST                'novel_url'
              248  BINARY_MODULO    
              250  CALL_METHOD_1         1  ''
              252  POP_TOP          

 L.  50       254  LOAD_FAST                'self'
              256  LOAD_ATTR                app
              258  LOAD_METHOD              init_crawler
              260  LOAD_FAST                'novel_url'
              262  CALL_METHOD_1         1  ''
              264  POP_TOP          
            266_0  COME_FROM           204  '204'

 L.  53       266  LOAD_FAST                'self'
              268  LOAD_ATTR                app
              270  LOAD_METHOD              can_do
              272  LOAD_STR                 'login'
              274  CALL_METHOD_1         1  ''
          276_278  POP_JUMP_IF_FALSE   292  'to 292'

 L.  54       280  LOAD_FAST                'self'
              282  LOAD_METHOD              get_login_info
              284  CALL_METHOD_0         0  ''
              286  LOAD_FAST                'self'
              288  LOAD_ATTR                app
              290  STORE_ATTR               login_data
            292_0  COME_FROM           276  '276'

 L.  57       292  LOAD_FAST                'self'
              294  LOAD_ATTR                app
              296  LOAD_METHOD              get_novel_info
              298  CALL_METHOD_0         0  ''
              300  POP_TOP          

 L.  59       302  LOAD_FAST                'self'
              304  LOAD_METHOD              get_output_path
              306  CALL_METHOD_0         0  ''
              308  LOAD_FAST                'self'
              310  LOAD_ATTR                app
              312  STORE_ATTR               output_path

 L.  60       314  LOAD_FAST                'self'
              316  LOAD_METHOD              process_chapter_range
              318  CALL_METHOD_0         0  ''
              320  LOAD_FAST                'self'
              322  LOAD_ATTR                app
              324  STORE_ATTR               chapters

 L.  62       326  LOAD_FAST                'self'
              328  LOAD_METHOD              get_output_formats
              330  CALL_METHOD_0         0  ''
              332  LOAD_FAST                'self'
              334  LOAD_ATTR                app
              336  STORE_ATTR               output_formats

 L.  63       338  LOAD_FAST                'self'
              340  LOAD_METHOD              should_pack_by_volume
              342  CALL_METHOD_0         0  ''
              344  LOAD_FAST                'self'
              346  LOAD_ATTR                app
              348  STORE_ATTR               pack_by_volume

 L.  65       350  LOAD_FAST                'self'
              352  LOAD_ATTR                app
              354  LOAD_METHOD              start_download
              356  CALL_METHOD_0         0  ''
              358  POP_TOP          

 L.  66       360  LOAD_FAST                'self'
              362  LOAD_ATTR                app
              364  LOAD_METHOD              bind_books
              366  CALL_METHOD_0         0  ''
              368  POP_TOP          

 L.  67       370  LOAD_FAST                'self'
              372  LOAD_ATTR                app
              374  LOAD_METHOD              compress_books
              376  CALL_METHOD_0         0  ''
              378  POP_TOP          

 L.  69       380  LOAD_FAST                'self'
              382  LOAD_ATTR                app
              384  LOAD_METHOD              destroy
              386  CALL_METHOD_0         0  ''
              388  POP_TOP          

 L.  70       390  LOAD_GLOBAL              display
              392  LOAD_METHOD              app_complete
              394  CALL_METHOD_0         0  ''
              396  POP_TOP          

 L.  72       398  LOAD_FAST                'self'
              400  LOAD_METHOD              open_folder
              402  CALL_METHOD_0         0  ''
          404_406  POP_JUMP_IF_FALSE   452  'to 452'

 L.  73       408  LOAD_CONST               0
              410  LOAD_CONST               None
              412  IMPORT_NAME              pathlib
              414  STORE_FAST               'pathlib'

 L.  74       416  LOAD_CONST               0
              418  LOAD_CONST               None
              420  IMPORT_NAME              webbrowser
              422  STORE_FAST               'webbrowser'

 L.  75       424  LOAD_FAST                'pathlib'
              426  LOAD_METHOD              Path
              428  LOAD_FAST                'self'
              430  LOAD_ATTR                app
              432  LOAD_ATTR                output_path
              434  CALL_METHOD_1         1  ''
              436  LOAD_METHOD              as_uri
              438  CALL_METHOD_0         0  ''
              440  STORE_FAST               'url'

 L.  76       442  LOAD_FAST                'webbrowser'
              444  LOAD_METHOD              open_new
              446  LOAD_FAST                'url'
              448  CALL_METHOD_1         1  ''
              450  POP_TOP          
            452_0  COME_FROM           404  '404'

Parse error at or near `LOAD_CONST' instruction at offset 178


def process_chapter_range(self):
    chapters = []
    res = self.get_range_selection
    args = get_args
    if res == 'all':
        chapters = self.app.crawler.chapters[:]
    else:
        if res == 'first':
            n = args.first or 10
            chapters = self.app.crawler.chapters[:n]
        else:
            if res == 'last':
                n = args.last or 10
                chapters = self.app.crawler.chapters[-n:]
            else:
                if res == 'page':
                    start, stop = self.get_range_using_urls
                    chapters = self.app.crawler.chapters[start:stop + 1]
                else:
                    if res == 'range':
                        start, stop = self.get_range_using_index
                        chapters = self.app.crawler.chapters[start:stop + 1]
                    else:
                        if res == 'volumes':
                            selected = self.get_range_from_volumes
                            chapters = [chap for chap in self.app.crawler.chapters if selected.countchap['volume'] > 0]
                        else:
                            if res == 'chapters':
                                selected = self.get_range_from_chapters
                                chapters = [chap for chap in self.app.crawler.chapters if selected.countchap['id'] > 0]
                            else:
                                if len(chapters) == 0:
                                    raise Exception('No chapters to download')
                                self.log.debug'Selected chapters:'
                                self.log.debugchapters
                                if not args.suppress:
                                    answer = prompt([
                                     {'type':'list', 
                                      'name':'continue', 
                                      'message':'%d chapters selected' % len(chapters), 
                                      'choices':[
                                       'Continue',
                                       'Change selection']}])
                                    if answer['continue'] == 'Change selection':
                                        return self.process_chapter_range
                            self.log.info('%d chapters to be downloaded', len(chapters))
                            return chapters


def open_folder(self):
    args = get_args
    if args.suppress:
        return False
    answer = prompt([
     {'type':'confirm', 
      'name':'exit', 
      'message':'Open the output folder?', 
      'default':True}])
    return answer['exit']