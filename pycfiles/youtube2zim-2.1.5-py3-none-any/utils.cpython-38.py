# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/reg/src/youtube/youtube2zim/utils.py
# Compiled at: 2020-02-05 04:05:47
# Size of source mod 2**32: 974 bytes
import json
from slugify import slugify

def get_slug(text, js_safe=True):
    """ slug from text to build URL parts """
    if js_safe:
        return slugify(text, regex_pattern='[^-a-z0-9_]+').replace('-', '_')
    return slugify(text)


def clean_text(text):
    """ cleaned-down version of text as Youtube is very permissive with descriptions """
    return text.strip().replace('\n', ' ').replace('\r', ' ')


def save_json(cache_dir, key, data):
    """ save JSON collection to path """
    with open(cache_dir.joinpath(f"{key}.json"), 'w') as (fp):
        json.dump(data, fp, indent=4)


def load_json--- This code section failed: ---

 L.  30         0  LOAD_FAST                'cache_dir'
                2  LOAD_METHOD              joinpath
                4  LOAD_FAST                'key'
                6  FORMAT_VALUE          0  ''
                8  LOAD_STR                 '.json'
               10  BUILD_STRING_2        2 
               12  CALL_METHOD_1         1  ''
               14  STORE_FAST               'fname'

 L.  31        16  LOAD_FAST                'fname'
               18  LOAD_METHOD              exists
               20  CALL_METHOD_0         0  ''
               22  POP_JUMP_IF_TRUE     28  'to 28'

 L.  32        24  LOAD_CONST               None
               26  RETURN_VALUE     
             28_0  COME_FROM            22  '22'

 L.  33        28  SETUP_FINALLY        76  'to 76'

 L.  34        30  LOAD_GLOBAL              open
               32  LOAD_FAST                'fname'
               34  LOAD_STR                 'r'
               36  CALL_FUNCTION_2       2  ''
               38  SETUP_WITH           66  'to 66'
               40  STORE_FAST               'fp'

 L.  35        42  LOAD_GLOBAL              json
               44  LOAD_METHOD              load
               46  LOAD_FAST                'fp'
               48  CALL_METHOD_1         1  ''
               50  POP_BLOCK        
               52  ROT_TWO          
               54  BEGIN_FINALLY    
               56  WITH_CLEANUP_START
               58  WITH_CLEANUP_FINISH
               60  POP_FINALLY           0  ''
               62  POP_BLOCK        
               64  RETURN_VALUE     
             66_0  COME_FROM_WITH       38  '38'
               66  WITH_CLEANUP_START
               68  WITH_CLEANUP_FINISH
               70  END_FINALLY      
               72  POP_BLOCK        
               74  JUMP_FORWARD         98  'to 98'
             76_0  COME_FROM_FINALLY    28  '28'

 L.  36        76  DUP_TOP          
               78  LOAD_GLOBAL              Exception
               80  COMPARE_OP               exception-match
               82  POP_JUMP_IF_FALSE    96  'to 96'
               84  POP_TOP          
               86  POP_TOP          
               88  POP_TOP          

 L.  37        90  POP_EXCEPT       
               92  LOAD_CONST               None
               94  RETURN_VALUE     
             96_0  COME_FROM            82  '82'
               96  END_FINALLY      
             98_0  COME_FROM            74  '74'

Parse error at or near `ROT_TWO' instruction at offset 52