# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: .\src\core\downloader.py
# Compiled at: 2020-05-04 20:04:35
# Size of source mod 2**32: 5508 bytes
"""
To download chapter bodies
"""
import json, logging, os
from concurrent import futures
from io import BytesIO
from urllib.parse import urlparse
from PIL import Image
from progress.bar import IncrementalBar
from core.arguments import get_args
logger = logging.getLogger('DOWNLOADER')
try:
    from utils.racovimge import random_cover
except ImportError as err:
    try:
        logger.debug(err)
    finally:
        err = None
        del err

else:
    try:
        from cairosvg import svg2png
    except Exception:
        svg2png = None
        logger.info('CairoSVG was not found.Install it to generate random cover image:\n    pip install cairosvg')
    else:

        def download_cover--- This code section failed: ---

 L.  35         0  LOAD_FAST                'app'
                2  LOAD_ATTR                crawler
                4  LOAD_ATTR                novel_cover
                6  POP_JUMP_IF_TRUE     12  'to 12'

 L.  36         8  LOAD_CONST               None
               10  RETURN_VALUE     
             12_0  COME_FROM             6  '6'

 L.  39        12  LOAD_CONST               None
               14  STORE_FAST               'filename'

 L.  40        16  SETUP_FINALLY        56  'to 56'

 L.  41        18  LOAD_GLOBAL              os
               20  LOAD_ATTR                path
               22  LOAD_METHOD              join
               24  LOAD_FAST                'app'
               26  LOAD_ATTR                output_path
               28  LOAD_STR                 'cover.png'
               30  CALL_METHOD_2         2  ''
               32  STORE_FAST               'filename'

 L.  42        34  LOAD_GLOBAL              os
               36  LOAD_ATTR                path
               38  LOAD_METHOD              exists
               40  LOAD_FAST                'filename'
               42  CALL_METHOD_1         1  ''
               44  POP_JUMP_IF_FALSE    52  'to 52'

 L.  43        46  LOAD_FAST                'filename'
               48  POP_BLOCK        
               50  RETURN_VALUE     
             52_0  COME_FROM            44  '44'
               52  POP_BLOCK        
               54  JUMP_FORWARD        122  'to 122'
             56_0  COME_FROM_FINALLY    16  '16'

 L.  45        56  DUP_TOP          
               58  LOAD_GLOBAL              Exception
               60  COMPARE_OP               exception-match
               62  POP_JUMP_IF_FALSE   120  'to 120'
               64  POP_TOP          
               66  STORE_FAST               'ex'
               68  POP_TOP          
               70  SETUP_FINALLY       108  'to 108'

 L.  46        72  LOAD_GLOBAL              logger
               74  LOAD_METHOD              warn
               76  LOAD_STR                 'Failed to locate cover image: %s -> %s (%s)'

 L.  47        78  LOAD_FAST                'app'
               80  LOAD_ATTR                crawler
               82  LOAD_ATTR                novel_cover

 L.  47        84  LOAD_FAST                'app'
               86  LOAD_ATTR                output_path

 L.  47        88  LOAD_GLOBAL              str
               90  LOAD_FAST                'ex'
               92  CALL_FUNCTION_1       1  ''

 L.  46        94  CALL_METHOD_4         4  ''
               96  POP_TOP          

 L.  48        98  POP_BLOCK        
              100  POP_EXCEPT       
              102  CALL_FINALLY        108  'to 108'
              104  LOAD_CONST               None
              106  RETURN_VALUE     
            108_0  COME_FROM           102  '102'
            108_1  COME_FROM_FINALLY    70  '70'
              108  LOAD_CONST               None
              110  STORE_FAST               'ex'
              112  DELETE_FAST              'ex'
              114  END_FINALLY      
              116  POP_EXCEPT       
              118  JUMP_FORWARD        122  'to 122'
            120_0  COME_FROM            62  '62'
              120  END_FINALLY      
            122_0  COME_FROM           118  '118'
            122_1  COME_FROM            54  '54'

 L.  51       122  SETUP_FINALLY       208  'to 208'

 L.  52       124  LOAD_GLOBAL              logger
              126  LOAD_METHOD              info
              128  LOAD_STR                 'Downloading cover image...'
              130  CALL_METHOD_1         1  ''
              132  POP_TOP          

 L.  53       134  LOAD_FAST                'app'
              136  LOAD_ATTR                crawler
              138  LOAD_METHOD              get_response
              140  LOAD_FAST                'app'
              142  LOAD_ATTR                crawler
              144  LOAD_ATTR                novel_cover
              146  CALL_METHOD_1         1  ''
              148  STORE_FAST               'response'

 L.  54       150  LOAD_FAST                'response'
              152  LOAD_ATTR                status_code
              154  LOAD_CONST               200
              156  COMPARE_OP               ==
              158  POP_JUMP_IF_TRUE    164  'to 164'
              160  LOAD_ASSERT              AssertionError
              162  RAISE_VARARGS_1       1  'exception instance'
            164_0  COME_FROM           158  '158'

 L.  55       164  LOAD_GLOBAL              Image
              166  LOAD_METHOD              open
              168  LOAD_GLOBAL              BytesIO
              170  LOAD_FAST                'response'
              172  LOAD_ATTR                content
              174  CALL_FUNCTION_1       1  ''
              176  CALL_METHOD_1         1  ''
              178  STORE_FAST               'img'

 L.  56       180  LOAD_FAST                'img'
              182  LOAD_METHOD              save
              184  LOAD_FAST                'filename'
              186  CALL_METHOD_1         1  ''
              188  POP_TOP          

 L.  57       190  LOAD_GLOBAL              logger
              192  LOAD_METHOD              debug
              194  LOAD_STR                 'Saved cover: %s'
              196  LOAD_FAST                'filename'
              198  CALL_METHOD_2         2  ''
              200  POP_TOP          

 L.  58       202  LOAD_FAST                'filename'
              204  POP_BLOCK        
              206  RETURN_VALUE     
            208_0  COME_FROM_FINALLY   122  '122'

 L.  59       208  DUP_TOP          
              210  LOAD_GLOBAL              Exception
              212  COMPARE_OP               exception-match
          214_216  POP_JUMP_IF_FALSE   272  'to 272'
              218  POP_TOP          
              220  STORE_FAST               'ex'
              222  POP_TOP          
              224  SETUP_FINALLY       260  'to 260'

 L.  60       226  LOAD_GLOBAL              logger
              228  LOAD_METHOD              warn
              230  LOAD_STR                 'Failed to download cover image: %s -> %s (%s)'

 L.  61       232  LOAD_FAST                'app'
              234  LOAD_ATTR                crawler
              236  LOAD_ATTR                novel_cover

 L.  61       238  LOAD_FAST                'filename'

 L.  61       240  LOAD_GLOBAL              str
              242  LOAD_FAST                'ex'
              244  CALL_FUNCTION_1       1  ''

 L.  60       246  CALL_METHOD_4         4  ''
              248  POP_TOP          

 L.  62       250  POP_BLOCK        
              252  POP_EXCEPT       
              254  CALL_FINALLY        260  'to 260'
              256  LOAD_CONST               None
              258  RETURN_VALUE     
            260_0  COME_FROM           254  '254'
            260_1  COME_FROM_FINALLY   224  '224'
              260  LOAD_CONST               None
              262  STORE_FAST               'ex'
              264  DELETE_FAST              'ex'
              266  END_FINALLY      
              268  POP_EXCEPT       
              270  JUMP_FORWARD        274  'to 274'
            272_0  COME_FROM           214  '214'
              272  END_FINALLY      
            274_0  COME_FROM           270  '270'

Parse error at or near `CALL_FINALLY' instruction at offset 102


        def generate_cover--- This code section failed: ---

 L.  68         0  LOAD_GLOBAL              logger
                2  LOAD_METHOD              info
                4  LOAD_STR                 'Generating cover image...'
                6  CALL_METHOD_1         1  ''
                8  POP_TOP          

 L.  69        10  LOAD_GLOBAL              svg2png
               12  LOAD_CONST               None
               14  COMPARE_OP               is
               16  POP_JUMP_IF_FALSE    22  'to 22'

 L.  70        18  LOAD_CONST               None
               20  RETURN_VALUE     
             22_0  COME_FROM            16  '16'

 L.  72        22  SETUP_FINALLY       156  'to 156'

 L.  73        24  LOAD_GLOBAL              os
               26  LOAD_ATTR                path
               28  LOAD_METHOD              join
               30  LOAD_FAST                'app'
               32  LOAD_ATTR                output_path
               34  LOAD_STR                 'cover.svg'
               36  CALL_METHOD_2         2  ''
               38  STORE_FAST               'svg_file'

 L.  74        40  LOAD_GLOBAL              random_cover

 L.  75        42  LOAD_FAST                'app'
               44  LOAD_ATTR                crawler
               46  LOAD_ATTR                novel_title

 L.  76        48  LOAD_FAST                'app'
               50  LOAD_ATTR                crawler
               52  LOAD_ATTR                novel_author

 L.  74        54  LOAD_CONST               ('title', 'author')
               56  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               58  STORE_FAST               'svg'

 L.  79        60  LOAD_GLOBAL              open
               62  LOAD_FAST                'svg_file'
               64  LOAD_STR                 'w'
               66  LOAD_STR                 'utf-8'
               68  LOAD_CONST               ('encoding',)
               70  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               72  SETUP_WITH          100  'to 100'
               74  STORE_FAST               'f'

 L.  80        76  LOAD_FAST                'f'
               78  LOAD_METHOD              write
               80  LOAD_FAST                'svg'
               82  CALL_METHOD_1         1  ''
               84  POP_TOP          

 L.  81        86  LOAD_GLOBAL              logger
               88  LOAD_METHOD              debug
               90  LOAD_STR                 'Saved a random cover.svg'
               92  CALL_METHOD_1         1  ''
               94  POP_TOP          
               96  POP_BLOCK        
               98  BEGIN_FINALLY    
            100_0  COME_FROM_WITH       72  '72'
              100  WITH_CLEANUP_START
              102  WITH_CLEANUP_FINISH
              104  END_FINALLY      

 L.  84       106  LOAD_GLOBAL              os
              108  LOAD_ATTR                path
              110  LOAD_METHOD              join
              112  LOAD_FAST                'app'
              114  LOAD_ATTR                output_path
              116  LOAD_STR                 'cover.png'
              118  CALL_METHOD_2         2  ''
              120  STORE_FAST               'png_file'

 L.  85       122  LOAD_GLOBAL              svg2png
              124  LOAD_FAST                'svg'
              126  LOAD_METHOD              encode
              128  LOAD_STR                 'utf-8'
              130  CALL_METHOD_1         1  ''
              132  LOAD_FAST                'png_file'
              134  LOAD_CONST               ('bytestring', 'write_to')
              136  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              138  POP_TOP          

 L.  86       140  LOAD_GLOBAL              logger
              142  LOAD_METHOD              debug
              144  LOAD_STR                 'Converted cover.svg to cover.png'
              146  CALL_METHOD_1         1  ''
              148  POP_TOP          

 L.  88       150  LOAD_FAST                'png_file'
              152  POP_BLOCK        
              154  RETURN_VALUE     
            156_0  COME_FROM_FINALLY    22  '22'

 L.  89       156  DUP_TOP          
              158  LOAD_GLOBAL              Exception
              160  COMPARE_OP               exception-match
              162  POP_JUMP_IF_FALSE   190  'to 190'
              164  POP_TOP          
              166  POP_TOP          
              168  POP_TOP          

 L.  90       170  LOAD_GLOBAL              logger
              172  LOAD_METHOD              exception
              174  LOAD_STR                 'Failed to generate cover image: %s'
              176  LOAD_FAST                'app'
              178  LOAD_ATTR                output_path
              180  CALL_METHOD_2         2  ''
              182  POP_TOP          

 L.  91       184  POP_EXCEPT       
              186  LOAD_CONST               None
              188  RETURN_VALUE     
            190_0  COME_FROM           162  '162'
              190  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 166


        def download_chapter_body(app, chapter):
            result = None
            dir_name = os.path.joinapp.output_path'json'
            if app.pack_by_volume:
                vol_name = 'Volume ' + str(chapter['volume']).rjust2'0'
                dir_name = os.path.joindir_namevol_name
            os.makedirs(dir_name, exist_ok=True)
            chapter_name = str(chapter['id']).rjust5'0'
            file_name = os.path.joindir_name(chapter_name + '.json')
            chapter['body'] = ''
            if os.path.exists(file_name):
                logger.debug'Restoring from %s'file_name
                with open(file_name, 'r', encoding='utf-8') as (file):
                    old_chapter = json.load(file)
                    chapter['body'] = old_chapter['body']
            if len(chapter['body']) == 0:
                body = ''
                try:
                    logger.debug'Downloading to %s'file_name
                    body = app.crawler.download_chapter_body(chapter)
                except Exception:
                    logger.exception('Failed to download chapter body')
                else:
                    if body and len(body) == 0:
                        result = 'Body is empty: ' + chapter['url']
                    else:
                        if not ('body_lock' in chapter and chapter['body_lock']):
                            body = app.crawler.cleanup_text(body)
                        title = chapter['title'].replace'>''&gt;'.replace'<''&lt;'
                        chapter['body'] = '<h1>%s</h1>\n%s' % (title, body)
                        if get_args().add_source_url:
                            chapter['body'] += '<br><p>Source: <a href="%s">%s</a></p>' % (
                             chapter['url'], chapter['url'])
                        with open(file_name, 'w', encoding='utf-8') as (file):
                            file.write(json.dumps(chapter))
            return result


        def download_chapters--- This code section failed: ---

 L. 150         0  LOAD_GLOBAL              download_cover
                2  LOAD_DEREF               'app'
                4  CALL_FUNCTION_1       1  ''
                6  LOAD_DEREF               'app'
                8  STORE_ATTR               book_cover

 L. 151        10  LOAD_DEREF               'app'
               12  LOAD_ATTR                book_cover
               14  POP_JUMP_IF_TRUE     26  'to 26'

 L. 152        16  LOAD_GLOBAL              generate_cover
               18  LOAD_DEREF               'app'
               20  CALL_FUNCTION_1       1  ''
               22  LOAD_DEREF               'app'
               24  STORE_ATTR               book_cover
             26_0  COME_FROM            14  '14'

 L. 154        26  LOAD_DEREF               'app'
               28  LOAD_ATTR                book_cover
               30  POP_JUMP_IF_TRUE     42  'to 42'

 L. 155        32  LOAD_GLOBAL              logger
               34  LOAD_METHOD              warn
               36  LOAD_STR                 'No cover image'
               38  CALL_METHOD_1         1  ''
               40  POP_TOP          
             42_0  COME_FROM            30  '30'

 L. 158        42  LOAD_GLOBAL              IncrementalBar
               44  LOAD_STR                 'Downloading chapters'
               46  LOAD_GLOBAL              len
               48  LOAD_DEREF               'app'
               50  LOAD_ATTR                chapters
               52  CALL_FUNCTION_1       1  ''
               54  LOAD_CONST               ('max',)
               56  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               58  STORE_FAST               'bar'

 L. 159        60  LOAD_FAST                'bar'
               62  LOAD_METHOD              start
               64  CALL_METHOD_0         0  ''
               66  POP_TOP          

 L. 161        68  LOAD_GLOBAL              os
               70  LOAD_METHOD              getenv
               72  LOAD_STR                 'debug_mode'
               74  CALL_METHOD_1         1  ''
               76  LOAD_STR                 'yes'
               78  COMPARE_OP               ==
               80  POP_JUMP_IF_FALSE    92  'to 92'

 L. 162        82  LOAD_LAMBDA              '<code_object <lambda>>'
               84  LOAD_STR                 'download_chapters.<locals>.<lambda>'
               86  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               88  LOAD_FAST                'bar'
               90  STORE_ATTR               next
             92_0  COME_FROM            80  '80'

 L. 165        92  LOAD_CLOSURE             'app'
               94  BUILD_TUPLE_1         1 
               96  LOAD_DICTCOMP            '<code_object <dictcomp>>'
               98  LOAD_STR                 'download_chapters.<locals>.<dictcomp>'
              100  MAKE_FUNCTION_8          'closure'

 L. 171       102  LOAD_DEREF               'app'
              104  LOAD_ATTR                chapters

 L. 165       106  GET_ITER         
              108  CALL_FUNCTION_1       1  ''
              110  STORE_FAST               'futures_to_check'

 L. 174       112  LOAD_CONST               0
              114  LOAD_DEREF               'app'
              116  STORE_ATTR               progress

 L. 175       118  LOAD_GLOBAL              futures
              120  LOAD_METHOD              as_completed
              122  LOAD_FAST                'futures_to_check'
              124  CALL_METHOD_1         1  ''
              126  GET_ITER         
              128  FOR_ITER            186  'to 186'
              130  STORE_FAST               'future'

 L. 176       132  LOAD_FAST                'future'
              134  LOAD_METHOD              result
              136  CALL_METHOD_0         0  ''
              138  STORE_FAST               'result'

 L. 177       140  LOAD_FAST                'result'
              142  POP_JUMP_IF_FALSE   162  'to 162'

 L. 178       144  LOAD_FAST                'bar'
              146  LOAD_METHOD              clearln
              148  CALL_METHOD_0         0  ''
              150  POP_TOP          

 L. 179       152  LOAD_GLOBAL              logger
              154  LOAD_METHOD              error
              156  LOAD_FAST                'result'
              158  CALL_METHOD_1         1  ''
              160  POP_TOP          
            162_0  COME_FROM           142  '142'

 L. 181       162  LOAD_DEREF               'app'
              164  DUP_TOP          
              166  LOAD_ATTR                progress
              168  LOAD_CONST               1
              170  INPLACE_ADD      
              172  ROT_TWO          
              174  STORE_ATTR               progress

 L. 182       176  LOAD_FAST                'bar'
              178  LOAD_METHOD              next
              180  CALL_METHOD_0         0  ''
              182  POP_TOP          
              184  JUMP_BACK           128  'to 128'

 L. 185       186  LOAD_FAST                'bar'
              188  LOAD_METHOD              finish
              190  CALL_METHOD_0         0  ''
              192  POP_TOP          

 L. 186       194  LOAD_GLOBAL              print
              196  LOAD_STR                 'Downloaded %d chapters'
              198  LOAD_GLOBAL              len
              200  LOAD_DEREF               'app'
              202  LOAD_ATTR                chapters
              204  CALL_FUNCTION_1       1  ''
              206  BINARY_MODULO    
              208  CALL_FUNCTION_1       1  ''
              210  POP_TOP          

Parse error at or near `LOAD_DICTCOMP' instruction at offset 96