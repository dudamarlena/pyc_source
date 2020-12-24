# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: .\src\binders\calibre.py
# Compiled at: 2020-03-25 09:13:24
# Size of source mod 2**32: 3051 bytes
import logging, os, subprocess
logger = logging.getLogger('CALIBRE_BINDER')
EBOOK_CONVERT = 'ebook-convert'
CALIBRE_LINK = 'https://calibre-ebook.com/download'

def run_ebook_convert--- This code section failed: ---

 L.  17         0  SETUP_FINALLY        88  'to 88'

 L.  18         2  LOAD_GLOBAL              os
                4  LOAD_METHOD              getenv
                6  LOAD_STR                 'debug_mode'
                8  CALL_METHOD_1         1  ''
               10  LOAD_STR                 'yes'
               12  COMPARE_OP               ==
               14  STORE_FAST               'isdebug'

 L.  19        16  LOAD_GLOBAL              open
               18  LOAD_GLOBAL              os
               20  LOAD_ATTR                devnull
               22  LOAD_STR                 'w'
               24  CALL_FUNCTION_2       2  ''
               26  SETUP_WITH           76  'to 76'
               28  STORE_FAST               'dumper'

 L.  20        30  LOAD_GLOBAL              subprocess
               32  LOAD_ATTR                call

 L.  21        34  LOAD_GLOBAL              EBOOK_CONVERT
               36  BUILD_LIST_1          1 
               38  LOAD_GLOBAL              list
               40  LOAD_FAST                'args'
               42  CALL_FUNCTION_1       1  ''
               44  BINARY_ADD       

 L.  22        46  LOAD_FAST                'isdebug'
               48  POP_JUMP_IF_FALSE    54  'to 54'
               50  LOAD_CONST               None
               52  JUMP_FORWARD         56  'to 56'
             54_0  COME_FROM            48  '48'
               54  LOAD_FAST                'dumper'
             56_0  COME_FROM            52  '52'

 L.  23        56  LOAD_FAST                'isdebug'
               58  POP_JUMP_IF_FALSE    64  'to 64'
               60  LOAD_CONST               None
               62  JUMP_FORWARD         66  'to 66'
             64_0  COME_FROM            58  '58'
               64  LOAD_FAST                'dumper'
             66_0  COME_FROM            62  '62'

 L.  20        66  LOAD_CONST               ('stdout', 'stderr')
               68  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               70  POP_TOP          
               72  POP_BLOCK        
               74  BEGIN_FINALLY    
             76_0  COME_FROM_WITH       26  '26'
               76  WITH_CLEANUP_START
               78  WITH_CLEANUP_FINISH
               80  END_FINALLY      

 L.  26        82  POP_BLOCK        
               84  LOAD_CONST               True
               86  RETURN_VALUE     
             88_0  COME_FROM_FINALLY     0  '0'

 L.  27        88  DUP_TOP          
               90  LOAD_GLOBAL              Exception
               92  COMPARE_OP               exception-match
               94  POP_JUMP_IF_FALSE   130  'to 130'
               96  POP_TOP          
               98  POP_TOP          
              100  POP_TOP          

 L.  28       102  LOAD_CONST               0
              104  LOAD_CONST               None
              106  IMPORT_NAME              traceback
              108  STORE_FAST               'traceback'

 L.  29       110  LOAD_GLOBAL              logger
              112  LOAD_METHOD              debug
              114  LOAD_FAST                'traceback'
              116  LOAD_METHOD              format_exc
              118  CALL_METHOD_0         0  ''
              120  CALL_METHOD_1         1  ''
              122  POP_TOP          

 L.  30       124  POP_EXCEPT       
              126  LOAD_CONST               False
              128  RETURN_VALUE     
            130_0  COME_FROM            94  '94'
              130  END_FINALLY      

Parse error at or near `RETURN_VALUE' instruction at offset 86


def epub_to_calibre(app, epub_file, out_fmt):
    if not os.path.exists(epub_file):
        return
    epub_path = os.path.dirname(epub_file)
    epub_file_name = os.path.basename(epub_file)
    file_name_without_ext = epub_file_name.replace('.epub', '')
    work_path = os.path.dirname(epub_path)
    out_path = os.path.join(work_path, out_fmt)
    out_file_name = file_name_without_ext + '.' + out_fmt
    out_file = os.path.join(out_path, out_file_name)
    os.makedirs(out_path, exist_ok=True)
    logger.debug('Converting "%s" to "%s"', epub_file, out_file)
    args = [
     epub_file,
     out_file,
     '--unsmarten-punctuation',
     '--no-chapters-in-toc',
     '--title', file_name_without_ext,
     '--authors', app.crawler.novel_author,
     '--series', app.crawler.novel_title,
     '--publisher', app.crawler.home_url,
     '--book-producer', 'Lightnovel Crawler',
     '--enable-heuristics', '--disable-renumber-headings']
    if app.book_cover:
        args += ['--cover', app.book_cover]
    if out_fmt == 'pdf':
        args += [
         '--paper-size', 'a4',
         '--pdf-page-numbers',
         '--pdf-hyphenate',
         '--pdf-header-template', '<p style="text-align:center; color:#555; font-size:0.9em">⦗ _TITLE_ &mdash; _SECTION_ ⦘</p>']
    run_ebook_convert(*args)
    if os.path.exists(out_file):
        print('Created: %s' % out_file_name)
        return out_file
    logger.error('[%s] conversion failed: %s', out_fmt, epub_file_name)
    return None


def make_calibres(app, epubs, out_fmt):
    if not out_fmt == 'epub':
        return epubs or epubs
    else:
        run_ebook_convert('--version') or (
         logger.error('Install Calibre to generate %s: %s', out_fmt, CALIBRE_LINK),)
        return
    out_files = []
    for epub in epubs:
        out = epub_to_calibre(app, epub, out_fmt)
        out_files += [out]
    else:
        return out_files