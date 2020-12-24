# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/reg/src/zimscraperlib/src/zimscraperlib/i18n.py
# Compiled at: 2020-02-06 07:31:56
# Size of source mod 2**32: 1950 bytes
import locale, gettext, iso639

def setlocale(root_dir, locale_name):
    """ set the desired locale for gettext.

        call this early """
    computed = locale.setlocale(locale.LC_ALL, (locale_name.split('.')[0], 'UTF-8'))
    gettext.bindtextdomain('messages', str(root_dir.joinpath('locale')))
    gettext.textdomain('messages')
    return computed


def get_language_details--- This code section failed: ---

 L.  25         0  LOAD_STR                 'zh-Hans'

 L.  26         2  LOAD_STR                 'zh'

 L.  27         4  LOAD_STR                 'Simplified Chinese'

 L.  28         6  LOAD_STR                 '简化字'

 L.  24         8  LOAD_CONST               ('code', 'iso-639-1', 'english', 'native')
               10  BUILD_CONST_KEY_MAP_4     4 

 L.  31        12  LOAD_STR                 'zh-Hant'

 L.  32        14  LOAD_STR                 'zh'

 L.  33        16  LOAD_STR                 'Traditional Chinese'

 L.  34        18  LOAD_STR                 '正體字'

 L.  30        20  LOAD_CONST               ('code', 'iso-639-1', 'english', 'native')
               22  BUILD_CONST_KEY_MAP_4     4 

 L.  36        24  LOAD_STR                 'iw'
               26  LOAD_STR                 'he'
               28  LOAD_STR                 'Hebrew'
               30  LOAD_STR                 'עברית'
               32  LOAD_CONST               ('code', 'iso-639-1', 'english', 'native')
               34  BUILD_CONST_KEY_MAP_4     4 

 L.  38        36  LOAD_STR                 'es-419'

 L.  39        38  LOAD_STR                 'es-419'

 L.  40        40  LOAD_STR                 'Spanish'

 L.  41        42  LOAD_STR                 'Español'

 L.  37        44  LOAD_CONST               ('code', 'iso-639-1', 'english', 'native')
               46  BUILD_CONST_KEY_MAP_4     4 

 L.  44        48  LOAD_STR                 'mul'

 L.  45        50  LOAD_STR                 'en'

 L.  46        52  LOAD_STR                 'Multiple Languages'

 L.  47        54  LOAD_STR                 'Multiple Languages'

 L.  43        56  LOAD_CONST               ('code', 'iso-639-1', 'english', 'native')
               58  BUILD_CONST_KEY_MAP_4     4 

 L.  23        60  LOAD_CONST               ('zh-Hans', 'zh-Hant', 'iw', 'es-419', 'multi')
               62  BUILD_CONST_KEY_MAP_5     5 
               64  STORE_FAST               'non_iso_langs'

 L.  51        66  SETUP_FINALLY       124  'to 124'

 L.  54        68  LOAD_FAST                'iso_639_3'
               70  LOAD_FAST                'non_iso_langs'
               72  LOAD_METHOD              keys
               74  CALL_METHOD_0         0  ''
               76  COMPARE_OP               in

 L.  53        78  POP_JUMP_IF_FALSE    90  'to 90'
               80  LOAD_FAST                'non_iso_langs'
               82  LOAD_METHOD              get
               84  LOAD_FAST                'iso_639_3'
               86  CALL_METHOD_1         1  ''
               88  JUMP_FORWARD        120  'to 120'
             90_0  COME_FROM            78  '78'

 L.  56        90  LOAD_FAST                'iso_639_3'

 L.  57        92  LOAD_GLOBAL              iso639
               94  LOAD_METHOD              to_iso639_1
               96  LOAD_FAST                'iso_639_3'
               98  CALL_METHOD_1         1  ''

 L.  58       100  LOAD_GLOBAL              iso639
              102  LOAD_METHOD              to_name
              104  LOAD_FAST                'iso_639_3'
              106  CALL_METHOD_1         1  ''

 L.  59       108  LOAD_GLOBAL              iso639
              110  LOAD_METHOD              to_native
              112  LOAD_FAST                'iso_639_3'
              114  CALL_METHOD_1         1  ''

 L.  55       116  LOAD_CONST               ('code', 'iso-639-1', 'english', 'native')
              118  BUILD_CONST_KEY_MAP_4     4 
            120_0  COME_FROM            88  '88'

 L.  52       120  POP_BLOCK        
              122  RETURN_VALUE     
            124_0  COME_FROM_FINALLY    66  '66'

 L.  62       124  DUP_TOP          
              126  LOAD_GLOBAL              iso639
              128  LOAD_ATTR                NonExistentLanguageError
              130  COMPARE_OP               exception-match
              132  POP_JUMP_IF_FALSE   158  'to 158'
              134  POP_TOP          
              136  POP_TOP          
              138  POP_TOP          

 L.  64       140  LOAD_FAST                'iso_639_3'

 L.  65       142  LOAD_FAST                'iso_639_3'

 L.  66       144  LOAD_FAST                'iso_639_3'

 L.  67       146  LOAD_FAST                'iso_639_3'

 L.  63       148  LOAD_CONST               ('code', 'iso-639-1', 'english', 'native')
              150  BUILD_CONST_KEY_MAP_4     4 
              152  ROT_FOUR         
              154  POP_EXCEPT       
              156  RETURN_VALUE     
            158_0  COME_FROM           132  '132'
              158  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 136