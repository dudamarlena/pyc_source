# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/sorno/pdfutil.py
# Compiled at: 2020-03-16 00:44:32
# Size of source mod 2**32: 542 bytes
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals
import PyPDF2

def pdf_to_text--- This code section failed: ---

 L.   9         0  LOAD_GLOBAL              open
                2  LOAD_FAST                'filepath'
                4  LOAD_STR                 'rb'
                6  CALL_FUNCTION_2       2  ''
                8  SETUP_WITH           96  'to 96'
               10  STORE_FAST               'file_obj'

 L.  10        12  LOAD_GLOBAL              PyPDF2
               14  LOAD_METHOD              PdfFileReader
               16  LOAD_FAST                'file_obj'
               18  CALL_METHOD_1         1  ''
               20  STORE_FAST               'pdf_reader'

 L.  11        22  LOAD_FAST                'pdf_reader'
               24  LOAD_ATTR                numPages
               26  STORE_FAST               'num_pages'

 L.  13        28  LOAD_CONST               0
               30  STORE_FAST               'count'

 L.  14        32  BUILD_LIST_0          0 
               34  STORE_FAST               'text_segments'

 L.  15        36  LOAD_FAST                'count'
               38  LOAD_FAST                'num_pages'
               40  COMPARE_OP               <
               42  POP_JUMP_IF_FALSE    74  'to 74'

 L.  16        44  LOAD_FAST                'text_segments'
               46  LOAD_METHOD              append
               48  LOAD_FAST                'pdf_reader'
               50  LOAD_METHOD              getPage
               52  LOAD_FAST                'count'
               54  CALL_METHOD_1         1  ''
               56  LOAD_METHOD              extractText
               58  CALL_METHOD_0         0  ''
               60  CALL_METHOD_1         1  ''
               62  POP_TOP          

 L.  17        64  LOAD_FAST                'count'
               66  LOAD_CONST               1
               68  INPLACE_ADD      
               70  STORE_FAST               'count'
               72  JUMP_BACK            36  'to 36'
             74_0  COME_FROM            42  '42'

 L.  19        74  LOAD_STR                 ''
               76  LOAD_METHOD              join
               78  LOAD_FAST                'text_segments'
               80  CALL_METHOD_1         1  ''
               82  POP_BLOCK        
               84  ROT_TWO          
               86  BEGIN_FINALLY    
               88  WITH_CLEANUP_START
               90  WITH_CLEANUP_FINISH
               92  POP_FINALLY           0  ''
               94  RETURN_VALUE     
             96_0  COME_FROM_WITH        8  '8'
               96  WITH_CLEANUP_START
               98  WITH_CLEANUP_FINISH
              100  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 84