# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/reg/src/zimscraperlib/src/zimscraperlib/i18n.py
# Compiled at: 2020-05-07 07:54:34
# Size of source mod 2**32: 2713 bytes
import locale, gettext, iso639

class Locale:
    short = 'en'
    name = 'en_US.UTF-8'
    locale_dir = None
    domain = 'messages'
    translation = gettext.translation('messages', fallback=True)

    @classmethod
    def setup(cls, locale_dir, locale_name):
        cls.name = locale_name
        cls.locale_dir = str(locale_dir)
        if '.' in locale_name:
            cls.lang, cls.encoding = locale_name.split('.')
        else:
            cls.lang, cls.encoding = locale_name, 'UTF-8'
        computed = locale.setlocale(locale.LC_ALL, (cls.lang, cls.encoding))
        gettext.bindtextdomain(cls.domain, cls.locale_dir)
        gettext.textdomain(cls.domain)
        cls.translation = gettext.translation((cls.domain),
          (cls.locale_dir), languages=[cls.lang], fallback=True)
        return computed


def _(text):
    """ translates text according to setup'd locale """
    return Locale.translation.gettext(text)


def setlocale(root_dir, locale_name):
    """ set the desired locale for gettext.

        call this early """
    return Locale.setup(root_dir / 'locale', locale_name)


def get_language_details--- This code section failed: ---

 L.  55         0  LOAD_STR                 'zh-Hans'

 L.  56         2  LOAD_STR                 'zh'

 L.  57         4  LOAD_STR                 'Simplified Chinese'

 L.  58         6  LOAD_STR                 '简化字'

 L.  54         8  LOAD_CONST               ('code', 'iso-639-1', 'english', 'native')
               10  BUILD_CONST_KEY_MAP_4     4 

 L.  61        12  LOAD_STR                 'zh-Hant'

 L.  62        14  LOAD_STR                 'zh'

 L.  63        16  LOAD_STR                 'Traditional Chinese'

 L.  64        18  LOAD_STR                 '正體字'

 L.  60        20  LOAD_CONST               ('code', 'iso-639-1', 'english', 'native')
               22  BUILD_CONST_KEY_MAP_4     4 

 L.  66        24  LOAD_STR                 'iw'
               26  LOAD_STR                 'he'
               28  LOAD_STR                 'Hebrew'
               30  LOAD_STR                 'עברית'
               32  LOAD_CONST               ('code', 'iso-639-1', 'english', 'native')
               34  BUILD_CONST_KEY_MAP_4     4 

 L.  68        36  LOAD_STR                 'es-419'

 L.  69        38  LOAD_STR                 'es-419'

 L.  70        40  LOAD_STR                 'Spanish'

 L.  71        42  LOAD_STR                 'Español'

 L.  67        44  LOAD_CONST               ('code', 'iso-639-1', 'english', 'native')
               46  BUILD_CONST_KEY_MAP_4     4 

 L.  74        48  LOAD_STR                 'mul'

 L.  75        50  LOAD_STR                 'en'

 L.  76        52  LOAD_STR                 'Multiple Languages'

 L.  77        54  LOAD_STR                 'Multiple Languages'

 L.  73        56  LOAD_CONST               ('code', 'iso-639-1', 'english', 'native')
               58  BUILD_CONST_KEY_MAP_4     4 

 L.  53        60  LOAD_CONST               ('zh-Hans', 'zh-Hant', 'iw', 'es-419', 'multi')
               62  BUILD_CONST_KEY_MAP_5     5 
               64  STORE_FAST               'non_iso_langs'

 L.  81        66  SETUP_FINALLY       124  'to 124'

 L.  84        68  LOAD_FAST                'iso_639_3'
               70  LOAD_FAST                'non_iso_langs'
               72  LOAD_METHOD              keys
               74  CALL_METHOD_0         0  ''
               76  COMPARE_OP               in

 L.  83        78  POP_JUMP_IF_FALSE    90  'to 90'
               80  LOAD_FAST                'non_iso_langs'
               82  LOAD_METHOD              get
               84  LOAD_FAST                'iso_639_3'
               86  CALL_METHOD_1         1  ''
               88  JUMP_FORWARD        120  'to 120'
             90_0  COME_FROM            78  '78'

 L.  86        90  LOAD_FAST                'iso_639_3'

 L.  87        92  LOAD_GLOBAL              iso639
               94  LOAD_METHOD              to_iso639_1
               96  LOAD_FAST                'iso_639_3'
               98  CALL_METHOD_1         1  ''

 L.  88       100  LOAD_GLOBAL              iso639
              102  LOAD_METHOD              to_name
              104  LOAD_FAST                'iso_639_3'
              106  CALL_METHOD_1         1  ''

 L.  89       108  LOAD_GLOBAL              iso639
              110  LOAD_METHOD              to_native
              112  LOAD_FAST                'iso_639_3'
              114  CALL_METHOD_1         1  ''

 L.  85       116  LOAD_CONST               ('code', 'iso-639-1', 'english', 'native')
              118  BUILD_CONST_KEY_MAP_4     4 
            120_0  COME_FROM            88  '88'

 L.  82       120  POP_BLOCK        
              122  RETURN_VALUE     
            124_0  COME_FROM_FINALLY    66  '66'

 L.  92       124  DUP_TOP          
              126  LOAD_GLOBAL              iso639
              128  LOAD_ATTR                NonExistentLanguageError
              130  COMPARE_OP               exception-match
              132  POP_JUMP_IF_FALSE   158  'to 158'
              134  POP_TOP          
              136  POP_TOP          
              138  POP_TOP          

 L.  94       140  LOAD_FAST                'iso_639_3'

 L.  95       142  LOAD_FAST                'iso_639_3'

 L.  96       144  LOAD_FAST                'iso_639_3'

 L.  97       146  LOAD_FAST                'iso_639_3'

 L.  93       148  LOAD_CONST               ('code', 'iso-639-1', 'english', 'native')
              150  BUILD_CONST_KEY_MAP_4     4 
              152  ROT_FOUR         
              154  POP_EXCEPT       
              156  RETURN_VALUE     
            158_0  COME_FROM           132  '132'
              158  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 136