# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/afshari9978/Projects/namaki_backend/avishan/misc/translation.py
# Compiled at: 2020-04-27 02:41:37
# Size of source mod 2**32: 1163 bytes
from avishan.configure import get_avishan_config

class AvishanTranslatable:
    EN = None
    FA = None

    def __init__(self, **kwargs):
        """
        translatable texts
        :param kwargs: keys like: FA, EN
        """
        for key, value in kwargs.items():
            self.__setattr__(key.upper(), value)

    def __str__--- This code section failed: ---

 L.  19         0  LOAD_CONST               0
                2  LOAD_CONST               ('current_request',)
                4  IMPORT_NAME              avishan
                6  IMPORT_FROM              current_request
                8  STORE_FAST               'current_request'
               10  POP_TOP          

 L.  20        12  LOAD_CONST               0
               14  LOAD_CONST               ('ErrorMessageException',)
               16  IMPORT_NAME_ATTR         avishan.exceptions
               18  IMPORT_FROM              ErrorMessageException
               20  STORE_FAST               'ErrorMessageException'
               22  POP_TOP          

 L.  21        24  LOAD_STR                 'language'
               26  LOAD_FAST                'current_request'
               28  LOAD_METHOD              keys
               30  CALL_METHOD_0         0  ''
               32  COMPARE_OP               not-in
               34  POP_JUMP_IF_FALSE    80  'to 80'

 L.  22        36  SETUP_FINALLY        58  'to 58'

 L.  23        38  LOAD_GLOBAL              list
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                __dict__
               44  LOAD_METHOD              values
               46  CALL_METHOD_0         0  ''
               48  CALL_FUNCTION_1       1  ''
               50  LOAD_CONST               0
               52  BINARY_SUBSCR    
               54  POP_BLOCK        
               56  RETURN_VALUE     
             58_0  COME_FROM_FINALLY    36  '36'

 L.  24        58  DUP_TOP          
               60  LOAD_GLOBAL              IndexError
               62  COMPARE_OP               exception-match
               64  POP_JUMP_IF_FALSE    78  'to 78'
               66  POP_TOP          
               68  POP_TOP          
               70  POP_TOP          

 L.  25        72  POP_EXCEPT       
               74  LOAD_STR                 'Not translated string'
               76  RETURN_VALUE     
             78_0  COME_FROM            64  '64'
               78  END_FINALLY      
             80_0  COME_FROM            34  '34'

 L.  27        80  SETUP_FINALLY       154  'to 154'

 L.  28        82  LOAD_FAST                'current_request'
               84  LOAD_STR                 'language'
               86  BINARY_SUBSCR    
               88  LOAD_CONST               None
               90  COMPARE_OP               is
               92  POP_JUMP_IF_FALSE   104  'to 104'

 L.  29        94  LOAD_GLOBAL              get_avishan_config
               96  CALL_FUNCTION_0       0  ''
               98  LOAD_ATTR                LANGUAGE
              100  STORE_FAST               'lang'
              102  JUMP_FORWARD        112  'to 112'
            104_0  COME_FROM            92  '92'

 L.  31       104  LOAD_FAST                'current_request'
              106  LOAD_STR                 'language'
              108  BINARY_SUBSCR    
              110  STORE_FAST               'lang'
            112_0  COME_FROM           102  '102'

 L.  32       112  LOAD_FAST                'self'
              114  LOAD_ATTR                __dict__
              116  LOAD_FAST                'lang'
              118  LOAD_METHOD              upper
              120  CALL_METHOD_0         0  ''
              122  BINARY_SUBSCR    
              124  LOAD_CONST               None
              126  COMPARE_OP               is-not
              128  POP_JUMP_IF_FALSE   146  'to 146'

 L.  33       130  LOAD_FAST                'self'
              132  LOAD_ATTR                __dict__
              134  LOAD_FAST                'lang'
              136  LOAD_METHOD              upper
              138  CALL_METHOD_0         0  ''
              140  BINARY_SUBSCR    
              142  POP_BLOCK        
              144  RETURN_VALUE     
            146_0  COME_FROM           128  '128'

 L.  34       146  LOAD_GLOBAL              ValueError
              148  RAISE_VARARGS_1       1  'exception instance'
              150  POP_BLOCK        
              152  JUMP_FORWARD        196  'to 196'
            154_0  COME_FROM_FINALLY    80  '80'

 L.  35       154  DUP_TOP          
              156  LOAD_GLOBAL              Exception
              158  COMPARE_OP               exception-match
              160  POP_JUMP_IF_FALSE   194  'to 194'
              162  POP_TOP          
              164  STORE_FAST               'e'
              166  POP_TOP          
              168  SETUP_FINALLY       182  'to 182'

 L.  36       170  LOAD_FAST                'ErrorMessageException'
              172  LOAD_STR                 'Not translated string'
              174  CALL_FUNCTION_1       1  ''
              176  RAISE_VARARGS_1       1  'exception instance'
              178  POP_BLOCK        
              180  BEGIN_FINALLY    
            182_0  COME_FROM_FINALLY   168  '168'
              182  LOAD_CONST               None
              184  STORE_FAST               'e'
              186  DELETE_FAST              'e'
              188  END_FINALLY      
              190  POP_EXCEPT       
              192  JUMP_FORWARD        196  'to 196'
            194_0  COME_FROM           160  '160'
              194  END_FINALLY      
            196_0  COME_FROM           192  '192'
            196_1  COME_FROM           152  '152'

Parse error at or near `POP_TOP' instruction at offset 68