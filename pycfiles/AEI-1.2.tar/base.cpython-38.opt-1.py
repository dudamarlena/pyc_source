# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /aehostd/base.py
# Compiled at: 2019-11-15 11:20:52
# Size of source mod 2**32: 2115 bytes
__doc__ = '\naehostd.base - very basic stuff\n'
import os, logging

def dict_del(dct, key):
    """
    removes a dictionary element given by `key' but without failing if it
    does not exist
    """
    try:
        del dct[key]
    except KeyError:
        pass


class IdempotentFile:
    """IdempotentFile"""

    def __init__(self, path):
        self.path = path

    def __repr__(self):
        return '%s.%s(%r)' % (self.__class__.__module__, self.__class__.__name__, self.path)

    def read--- This code section failed: ---

 L.  36         0  SETUP_FINALLY        38  'to 38'

 L.  37         2  LOAD_GLOBAL              open
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                path
                8  LOAD_STR                 'rb'
               10  CALL_FUNCTION_2       2  ''
               12  SETUP_WITH           28  'to 28'
               14  STORE_FAST               'fileobj'

 L.  38        16  LOAD_FAST                'fileobj'
               18  LOAD_METHOD              read
               20  CALL_METHOD_0         0  ''
               22  STORE_FAST               'content'
               24  POP_BLOCK        
               26  BEGIN_FINALLY    
             28_0  COME_FROM_WITH       12  '12'
               28  WITH_CLEANUP_START
               30  WITH_CLEANUP_FINISH
               32  END_FINALLY      
               34  POP_BLOCK        
               36  JUMP_FORWARD         92  'to 92'
             38_0  COME_FROM_FINALLY     0  '0'

 L.  39        38  DUP_TOP          
               40  LOAD_GLOBAL              Exception
               42  COMPARE_OP               exception-match
               44  POP_JUMP_IF_FALSE    90  'to 90'
               46  POP_TOP          
               48  STORE_FAST               'err'
               50  POP_TOP          
               52  SETUP_FINALLY        78  'to 78'

 L.  40        54  LOAD_CONST               None
               56  STORE_FAST               'content'

 L.  41        58  LOAD_GLOBAL              logging
               60  LOAD_METHOD              warning
               62  LOAD_STR                 'Error reading file %r: %s'
               64  LOAD_FAST                'self'
               66  LOAD_ATTR                path
               68  LOAD_FAST                'err'
               70  CALL_METHOD_3         3  ''
               72  POP_TOP          
               74  POP_BLOCK        
               76  BEGIN_FINALLY    
             78_0  COME_FROM_FINALLY    52  '52'
               78  LOAD_CONST               None
               80  STORE_FAST               'err'
               82  DELETE_FAST              'err'
               84  END_FINALLY      
               86  POP_EXCEPT       
               88  JUMP_FORWARD         92  'to 92'
             90_0  COME_FROM            44  '44'
               90  END_FINALLY      
             92_0  COME_FROM            88  '88'
             92_1  COME_FROM            36  '36'

 L.  42        92  LOAD_FAST                'content'
               94  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `BEGIN_FINALLY' instruction at offset 26

    def write--- This code section failed: ---

 L.  48         0  LOAD_GLOBAL              os
                2  LOAD_ATTR                path
                4  LOAD_METHOD              exists
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                path
               10  CALL_METHOD_1         1  ''
               12  STORE_FAST               'exists'

 L.  49        14  LOAD_FAST                'exists'
               16  POP_JUMP_IF_FALSE    54  'to 54'
               18  LOAD_FAST                'content'
               20  LOAD_FAST                'self'
               22  LOAD_METHOD              read
               24  CALL_METHOD_0         0  ''
               26  COMPARE_OP               ==
               28  POP_JUMP_IF_FALSE    54  'to 54'

 L.  50        30  LOAD_GLOBAL              logging
               32  LOAD_METHOD              debug

 L.  51        34  LOAD_STR                 'Content of %r (%d bytes) did not change => skip updating'

 L.  52        36  LOAD_FAST                'self'
               38  LOAD_ATTR                path

 L.  53        40  LOAD_GLOBAL              len
               42  LOAD_FAST                'content'
               44  CALL_FUNCTION_1       1  ''

 L.  50        46  CALL_METHOD_3         3  ''
               48  POP_TOP          

 L.  55        50  LOAD_CONST               False
               52  RETURN_VALUE     
             54_0  COME_FROM            28  '28'
             54_1  COME_FROM            16  '16'

 L.  57        54  LOAD_FAST                'exists'
               56  POP_JUMP_IF_FALSE   100  'to 100'
               58  LOAD_FAST                'remove'
               60  POP_JUMP_IF_FALSE   100  'to 100'

 L.  58        62  SETUP_FINALLY        80  'to 80'

 L.  59        64  LOAD_GLOBAL              os
               66  LOAD_METHOD              remove
               68  LOAD_FAST                'self'
               70  LOAD_ATTR                path
               72  CALL_METHOD_1         1  ''
               74  POP_TOP          
               76  POP_BLOCK        
               78  JUMP_FORWARD        100  'to 100'
             80_0  COME_FROM_FINALLY    62  '62'

 L.  60        80  DUP_TOP          
               82  LOAD_GLOBAL              OSError
               84  COMPARE_OP               exception-match
               86  POP_JUMP_IF_FALSE    98  'to 98'
               88  POP_TOP          
               90  POP_TOP          
               92  POP_TOP          

 L.  61        94  POP_EXCEPT       
               96  JUMP_FORWARD        100  'to 100'
             98_0  COME_FROM            86  '86'
               98  END_FINALLY      
            100_0  COME_FROM            96  '96'
            100_1  COME_FROM            78  '78'
            100_2  COME_FROM            60  '60'
            100_3  COME_FROM            56  '56'

 L.  63       100  SETUP_FINALLY       162  'to 162'

 L.  64       102  LOAD_GLOBAL              open
              104  LOAD_FAST                'self'
              106  LOAD_ATTR                path
              108  LOAD_STR                 'wb'
              110  CALL_FUNCTION_2       2  ''
              112  SETUP_WITH          130  'to 130'
              114  STORE_FAST               'fileobj'

 L.  65       116  LOAD_FAST                'fileobj'
              118  LOAD_METHOD              write
              120  LOAD_FAST                'content'
              122  CALL_METHOD_1         1  ''
              124  POP_TOP          
              126  POP_BLOCK        
              128  BEGIN_FINALLY    
            130_0  COME_FROM_WITH      112  '112'
              130  WITH_CLEANUP_START
              132  WITH_CLEANUP_FINISH
              134  END_FINALLY      

 L.  66       136  LOAD_FAST                'mode'
              138  LOAD_CONST               None
              140  COMPARE_OP               is-not
              142  POP_JUMP_IF_FALSE   158  'to 158'

 L.  67       144  LOAD_GLOBAL              os
              146  LOAD_METHOD              chmod
              148  LOAD_FAST                'self'
              150  LOAD_ATTR                path
              152  LOAD_FAST                'mode'
              154  CALL_METHOD_2         2  ''
              156  POP_TOP          
            158_0  COME_FROM           142  '142'
              158  POP_BLOCK        
              160  JUMP_FORWARD        216  'to 216'
            162_0  COME_FROM_FINALLY   100  '100'

 L.  68       162  DUP_TOP          
              164  LOAD_GLOBAL              Exception
              166  COMPARE_OP               exception-match
              168  POP_JUMP_IF_FALSE   214  'to 214'
              170  POP_TOP          
              172  STORE_FAST               'err'
              174  POP_TOP          
              176  SETUP_FINALLY       202  'to 202'

 L.  69       178  LOAD_CONST               False
              180  STORE_FAST               'updated'

 L.  70       182  LOAD_GLOBAL              logging
              184  LOAD_METHOD              error

 L.  71       186  LOAD_STR                 'Error writing content to file %r: %s'

 L.  72       188  LOAD_FAST                'self'
              190  LOAD_ATTR                path

 L.  73       192  LOAD_FAST                'err'

 L.  70       194  CALL_METHOD_3         3  ''
              196  POP_TOP          
              198  POP_BLOCK        
              200  BEGIN_FINALLY    
            202_0  COME_FROM_FINALLY   176  '176'
              202  LOAD_CONST               None
              204  STORE_FAST               'err'
              206  DELETE_FAST              'err'
              208  END_FINALLY      
              210  POP_EXCEPT       
              212  JUMP_FORWARD        240  'to 240'
            214_0  COME_FROM           168  '168'
              214  END_FINALLY      
            216_0  COME_FROM           160  '160'

 L.  76       216  LOAD_CONST               True
              218  STORE_FAST               'updated'

 L.  77       220  LOAD_GLOBAL              logging
              222  LOAD_METHOD              info
              224  LOAD_STR                 'Wrote new content (%d bytes) to file %r'
              226  LOAD_GLOBAL              len
              228  LOAD_FAST                'content'
              230  CALL_FUNCTION_1       1  ''
              232  LOAD_FAST                'self'
              234  LOAD_ATTR                path
              236  CALL_METHOD_3         3  ''
              238  POP_TOP          
            240_0  COME_FROM           212  '212'

 L.  78       240  LOAD_FAST                'updated'
              242  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `BEGIN_FINALLY' instruction at offset 128